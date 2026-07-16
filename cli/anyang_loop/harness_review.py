from __future__ import annotations

import hashlib
import html
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from .repo_snapshot import repository_identity


SCHEMA_VERSION = 1
SEMANTIC_LIMIT = 50
MAX_SEMANTIC_FILE_BYTES = 256 * 1024
ACTIONS = {"KEEP", "ONE_HOME", "LOAD_LATER", "MAKE_A_CHECK", "PROBATION", "RETIRE"}
EVIDENCE_LABELS = {"VERIFIED", "USER_REPORTED", "INFERRED", "INACCESSIBLE", "NOT_APPLICABLE"}
CONFIDENCE_LEVELS = {"high", "medium", "low"}
STATIONS = (
    "standing-context",
    "routing",
    "selected-context",
    "capabilities-authority",
    "completion-evidence",
)

ROOT_FILES = {
    "README.md",
    "pyproject.toml",
    "analytical-interfaces.yaml",
    "artifact-state.yaml",
    "bounded-agency.yaml",
    "epistemic-state.yaml",
}
GOVERNANCE_DOCS = {
    "docs/governance.md",
    "docs/membranes.md",
    "docs/analytical-interfaces.md",
    "docs/artificial-enlightened-intelligence.md",
    "docs/loops.md",
}
PROJECT_SETUP_NAMES = {
    "README.md",
    "executive-os-install.md",
    "decision-log.md",
    "risk-register.md",
    "operating-review.md",
}
EXCLUDED_AREAS = (
    ".git and Git internals",
    "generated-reviews and cache/build output",
    "finance data",
    "archives, transcripts, source bodies, source notes, and analyses",
    "project files below the top-level setup surface",
    "untracked and ignored files",
)


class HarnessReviewError(RuntimeError):
    pass


def scan_harness(repo: str | Path, output: str | Path | None = None) -> Path:
    root = _repository_root(Path(repo))
    tracked = _git_paths(root, "ls-files", "-z")
    included: list[dict[str, Any]] = []
    skipped_symlinks: list[str] = []

    for relative in sorted(tracked):
        normalized = _portable_path(relative)
        if not _included(normalized):
            continue
        source = root / Path(normalized)
        if source.is_symlink():
            skipped_symlinks.append(normalized)
            continue
        resolved = source.resolve(strict=True)
        _ensure_within(resolved, root)
        if not resolved.is_file():
            continue
        raw = resolved.read_bytes()
        kind, station = _classify(normalized)
        metadata = _metadata(normalized, raw)
        included.append(
            {
                "control_id": _control_id(normalized),
                "path": normalized,
                "label": metadata.pop("label", PurePosixPath(normalized).name),
                "kind": kind,
                "station": station,
                "sha256": _sha256(raw),
                "bytes": len(raw),
                "tracked": True,
                "semantic_eligible": len(raw) <= MAX_SEMANTIC_FILE_BYTES,
                "metadata": metadata,
            }
        )

    if not included:
        raise HarnessReviewError("No tracked AI harness controls matched the repository allowlist.")

    selected_ids = {
        item["control_id"]
        for item in [entry for entry in sorted(included, key=_semantic_priority) if entry["semantic_eligible"]][
            :SEMANTIC_LIMIT
        ]
    }
    for item in included:
        item["semantic_selected"] = item["control_id"] in selected_ids

    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    head = _git(root, "rev-parse", "HEAD")
    branch = _git(root, "branch", "--show-current") or "detached"
    baseline_payload = {
        "head": head,
        "controls": [(item["control_id"], item["path"], item["sha256"]) for item in included],
    }
    baseline_fingerprint = _sha256(_canonical_bytes(baseline_payload))
    scan_id = "scan-" + _sha256(f"{timestamp}:{baseline_fingerprint}".encode("utf-8"))[:16]
    untracked_count = len(_git_paths(root, "ls-files", "--others", "--exclude-standard", "-z"))

    packet = _packet_path(root, output, timestamp, head)
    evidence = packet / ".harness-review"
    packet.mkdir(parents=True)
    evidence.mkdir()

    gaps = [f"Excluded by default: {item}." for item in EXCLUDED_AREAS]
    if skipped_symlinks:
        gaps.append(f"Skipped {len(skipped_symlinks)} tracked symlink(s) without following them.")
    if untracked_count:
        gaps.append(f"Excluded {untracked_count} untracked file(s); paths were not recorded.")
    unselected = sum(1 for item in included if not item["semantic_selected"])
    if unselected:
        gaps.append(f"Inventory includes {unselected} control(s) outside the {SEMANTIC_LIMIT}-file semantic review ceiling.")

    scope = {
        "schema_version": SCHEMA_VERSION,
        "scan_id": scan_id,
        "baseline_fingerprint": baseline_fingerprint,
        "surface": "codex",
        "repository": repository_identity(root),
        "root": ".",
        "head": head,
        "branch": branch,
        "scanned_at": timestamp,
        "tracked_only": True,
        "semantic_limit": SEMANTIC_LIMIT,
        "included_control_count": len(included),
        "semantic_selected_count": len(selected_ids),
        "coverage_gaps": gaps,
    }
    inventory = {
        "schema_version": SCHEMA_VERSION,
        "scan_id": scan_id,
        "baseline_fingerprint": baseline_fingerprint,
        "stations": list(STATIONS),
        "controls": included,
    }
    _write_json(evidence / "00-scope.json", scope)
    _write_json(evidence / "01-inventory.json", inventory)

    receipt = {
        "schema_version": SCHEMA_VERSION,
        "scan_id": scan_id,
        "baseline_fingerprint": baseline_fingerprint,
        "scope_sha256": _file_hash(evidence / "00-scope.json"),
        "inventory_sha256": _file_hash(evidence / "01-inventory.json"),
    }
    _write_json(evidence / "scan-receipt.json", receipt)
    template = {
        "schema_version": SCHEMA_VERSION,
        "scan_id": scan_id,
        "baseline_fingerprint": baseline_fingerprint,
        "run_context": {
            "surface": {"value": "codex", "evidence": "VERIFIED"},
            "model": {"value": "unknown", "evidence": "INACCESSIBLE"},
            "sandbox": {"value": "unknown", "evidence": "INACCESSIBLE"},
            "approval_mode": {"value": "unknown", "evidence": "INACCESSIBLE"},
        },
        "summary": {
            "headline": "Replace with the main plain-English judgment.",
            "what_helps": [],
            "what_gets_in_way": [],
        },
        "decisions": [],
        "unreviewed_control_ids": [item["control_id"] for item in included],
        "coverage_gaps": list(gaps),
    }
    _write_json(evidence / "semantic-review.template.json", template)
    return packet


def render_harness(packet: str | Path, review_path: str | Path) -> Path:
    packet_path, root, scope, inventory = _load_packet(packet)
    _verify_current_baseline(root, scope, inventory)
    review = _read_json(Path(review_path))
    _validate_review(review, scope, inventory)
    proposals = _build_proposals(review, scope)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "scan_id": scope["scan_id"],
        "baseline_fingerprint": scope["baseline_fingerprint"],
        "generated_at": scope["scanned_at"],
        "items": proposals,
    }
    visible = packet_path / "YOUR-AI-SETUP.html"
    evidence = packet_path / ".harness-review"
    for destination in (visible, evidence / "02-semantic-review.json", evidence / "03-proposal-manifest.json", evidence / "EVIDENCE.md"):
        if destination.exists():
            raise HarnessReviewError(f"Refusing to overwrite existing report artifact: {destination.name}")
    _write_json(evidence / "02-semantic-review.json", review)
    _write_json(evidence / "03-proposal-manifest.json", manifest)
    (evidence / "EVIDENCE.md").write_text(_render_evidence(scope, inventory, review, proposals), encoding="utf-8")
    visible.write_text(_render_html(scope, inventory, review, proposals), encoding="utf-8")
    return visible


def record_decisions(
    packet: str | Path,
    approve: list[int] | tuple[int, ...] | None = None,
    reject: list[int] | tuple[int, ...] | None = None,
) -> Path:
    packet_path, root, scope, inventory = _load_packet(packet)
    _verify_current_baseline(root, scope, inventory)
    evidence = packet_path / ".harness-review"
    manifest = _read_json(evidence / "03-proposal-manifest.json")
    _validate_manifest_identity(manifest, scope)
    approved = list(approve or [])
    rejected = list(reject or [])
    if not approved and not rejected:
        raise HarnessReviewError("Record at least one approved or rejected proposal number.")
    if len(set(approved)) != len(approved) or len(set(rejected)) != len(rejected):
        raise HarnessReviewError("Duplicate proposal numbers are ambiguous and are not allowed.")
    overlap = set(approved) & set(rejected)
    if overlap:
        raise HarnessReviewError(f"Proposal numbers cannot be both approved and rejected: {sorted(overlap)}")
    valid = {item["number"] for item in manifest.get("items", [])}
    unknown = (set(approved) | set(rejected)) - valid
    if unknown:
        raise HarnessReviewError(f"Unknown proposal numbers: {sorted(unknown)}")

    result = json.loads(json.dumps(manifest))
    for item in result["items"]:
        if item["number"] in approved:
            item["decision"] = "APPROVED"
        elif item["number"] in rejected:
            item["decision"] = "REJECTED"
        else:
            item["decision"] = "PROPOSED"
    result["recorded_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    destination = evidence / "04-approval-review.json"
    if destination.exists():
        raise HarnessReviewError("Refusing to overwrite an existing approval review.")
    _write_json(destination, result)
    return destination


def _repository_root(path: Path) -> Path:
    candidate = path.resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=candidate,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise HarnessReviewError(result.stderr.strip() or "Target is not inside a Git repository.")
    return Path(result.stdout.strip()).resolve()


def _packet_path(root: Path, output: str | Path | None, timestamp: str, head: str) -> Path:
    allowed_root = (root / "generated-reviews" / "ai-harness").resolve()
    _ensure_within(allowed_root, root)
    if output is None:
        slug = timestamp.replace("-", "").replace(":", "").replace("Z", "Z-") + head[:8]
        packet = allowed_root / slug
    else:
        supplied = Path(output)
        packet = (supplied if supplied.is_absolute() else root / supplied).resolve()
    _ensure_within(packet, allowed_root)
    if packet.exists():
        raise HarnessReviewError("Output packet already exists; choose a new run directory.")
    return packet


def _load_packet(packet: str | Path) -> tuple[Path, Path, dict[str, Any], dict[str, Any]]:
    packet_path = Path(packet).resolve()
    root = _repository_root(packet_path)
    allowed_root = (root / "generated-reviews" / "ai-harness").resolve()
    _ensure_within(allowed_root, root)
    _ensure_within(packet_path, allowed_root)
    evidence = packet_path / ".harness-review"
    scope_path = evidence / "00-scope.json"
    inventory_path = evidence / "01-inventory.json"
    receipt_path = evidence / "scan-receipt.json"
    scope = _read_json(scope_path)
    inventory = _read_json(inventory_path)
    receipt = _read_json(receipt_path)
    if receipt.get("scope_sha256") != _file_hash(scope_path) or receipt.get("inventory_sha256") != _file_hash(inventory_path):
        raise HarnessReviewError("Packet evidence hashes do not match the scan receipt.")
    _validate_manifest_identity(inventory, scope)
    _validate_manifest_identity(receipt, scope)
    return packet_path, root, scope, inventory


def _validate_manifest_identity(value: dict[str, Any], scope: dict[str, Any]) -> None:
    if value.get("schema_version") != SCHEMA_VERSION:
        raise HarnessReviewError("Unsupported harness review schema version.")
    if value.get("scan_id") != scope.get("scan_id"):
        raise HarnessReviewError("Artifact scan identity does not match the packet.")
    if value.get("baseline_fingerprint") != scope.get("baseline_fingerprint"):
        raise HarnessReviewError("Artifact baseline does not match the packet.")


def _validate_review(review: dict[str, Any], scope: dict[str, Any], inventory: dict[str, Any]) -> None:
    if not isinstance(review, dict):
        raise HarnessReviewError("Semantic review must be a JSON object.")
    _validate_manifest_identity(review, scope)
    controls = inventory.get("controls")
    if not isinstance(controls, list):
        raise HarnessReviewError("Inventory controls are missing or invalid.")
    control_by_id = {item.get("control_id"): item for item in controls if isinstance(item, dict)}
    known_ids = set(control_by_id)
    known_paths = {item.get("path") for item in controls}

    run_context = review.get("run_context")
    if not isinstance(run_context, dict):
        raise HarnessReviewError("Semantic review requires run_context.")
    for field in ("surface", "model", "sandbox", "approval_mode"):
        entry = run_context.get(field)
        if not isinstance(entry, dict) or not _nonempty(entry.get("value")) or entry.get("evidence") not in EVIDENCE_LABELS:
            raise HarnessReviewError(f"run_context.{field} requires a value and valid evidence label.")

    summary = review.get("summary")
    if not isinstance(summary, dict) or not _nonempty(summary.get("headline")):
        raise HarnessReviewError("Semantic review requires a non-empty summary headline.")
    for field in ("what_helps", "what_gets_in_way"):
        if not _string_list(summary.get(field)):
            raise HarnessReviewError(f"summary.{field} must be a list of non-empty strings.")

    decisions = review.get("decisions")
    unreviewed = review.get("unreviewed_control_ids")
    if not isinstance(decisions, list) or not isinstance(unreviewed, list):
        raise HarnessReviewError("Semantic review requires decisions and unreviewed_control_ids lists.")
    assigned: list[str] = []
    for index, decision in enumerate(decisions, start=1):
        if not isinstance(decision, dict):
            raise HarnessReviewError(f"Decision {index} must be an object.")
        if decision.get("action") not in ACTIONS:
            raise HarnessReviewError(f"Decision {index} uses an unsupported action.")
        ids = decision.get("control_ids")
        if not isinstance(ids, list) or not ids or any(not isinstance(item, str) for item in ids):
            raise HarnessReviewError(f"Decision {index} requires at least one control ID.")
        assigned.extend(ids)
        for field in ("finding", "user_impact", "proposal", "risk", "approver", "rollback"):
            if not _nonempty(decision.get(field)):
                raise HarnessReviewError(f"Decision {index} requires non-empty {field}.")
        if decision.get("confidence") not in CONFIDENCE_LEVELS:
            raise HarnessReviewError(f"Decision {index} requires high, medium, or low confidence.")
        if not _string_list(decision.get("evidence_paths")):
            raise HarnessReviewError(f"Decision {index} requires evidence_paths.")
        if not _string_list(decision.get("protections")):
            raise HarnessReviewError(f"Decision {index} requires protections.")
        unknown_paths = set(decision["evidence_paths"]) - known_paths
        if unknown_paths:
            raise HarnessReviewError(f"Decision {index} cites paths outside the inventory: {sorted(unknown_paths)}")

    if any(not isinstance(item, str) for item in unreviewed):
        raise HarnessReviewError("Unreviewed control IDs must be strings.")
    all_assignments = assigned + unreviewed
    unknown_ids = set(all_assignments) - known_ids
    if unknown_ids:
        raise HarnessReviewError(f"Semantic review invents unknown control IDs: {sorted(unknown_ids)}")
    duplicates = {item for item in all_assignments if all_assignments.count(item) > 1}
    if duplicates:
        raise HarnessReviewError(f"Controls may be accounted for only once: {sorted(duplicates)}")
    missing = known_ids - set(all_assignments)
    if missing:
        raise HarnessReviewError(f"Semantic review does not account for controls: {sorted(missing)}")
    gaps = review.get("coverage_gaps")
    if not isinstance(gaps, list) or any(not _nonempty(item) for item in gaps):
        raise HarnessReviewError("coverage_gaps must be a list of non-empty strings.")


def _verify_current_baseline(root: Path, scope: dict[str, Any], inventory: dict[str, Any]) -> None:
    if _git(root, "rev-parse", "HEAD") != scope.get("head"):
        raise HarnessReviewError("Repository HEAD changed after the harness scan.")
    tracked = set(_git_paths(root, "ls-files", "-z"))
    for control in inventory.get("controls", []):
        relative = control["path"]
        if relative not in tracked:
            raise HarnessReviewError(f"Reviewed control is no longer tracked: {relative}")
        source = root / Path(relative)
        if source.is_symlink():
            raise HarnessReviewError(f"Reviewed control became a symlink: {relative}")
        try:
            resolved = source.resolve(strict=True)
        except FileNotFoundError as exc:
            raise HarnessReviewError(f"Reviewed control no longer exists: {relative}") from exc
        _ensure_within(resolved, root)
        if _file_hash(resolved) != control["sha256"]:
            raise HarnessReviewError(f"Reviewed control changed after scan: {relative}")


def _build_proposals(review: dict[str, Any], scope: dict[str, Any]) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for decision in review["decisions"]:
        if decision["action"] == "KEEP":
            continue
        identity = {
            "baseline": scope["baseline_fingerprint"],
            "action": decision["action"],
            "control_ids": sorted(decision["control_ids"]),
            "proposal": decision["proposal"],
        }
        proposals.append(
            {
                "proposal_id": "chg-" + _sha256(_canonical_bytes(identity))[:12],
                "action": decision["action"],
                "control_ids": sorted(decision["control_ids"]),
                "finding": decision["finding"],
                "user_impact": decision["user_impact"],
                "proposal": decision["proposal"],
                "risk": decision["risk"],
                "approver": decision["approver"],
                "rollback": decision["rollback"],
                "protections": decision["protections"],
                "confidence": decision["confidence"],
                "decision": "PROPOSED",
            }
        )
    proposals.sort(key=lambda item: item["proposal_id"])
    for number, proposal in enumerate(proposals, start=1):
        proposal["number"] = number
    return proposals


def _render_html(
    scope: dict[str, Any], inventory: dict[str, Any], review: dict[str, Any], proposals: list[dict[str, Any]]
) -> str:
    esc = lambda value: html.escape(str(value), quote=True)
    controls = inventory["controls"]
    station_sections: list[str] = []
    for station in STATIONS:
        rows = [item for item in controls if item["station"] == station]
        items = "".join(
            f"<li><strong>{esc(item['label'])}</strong><span>{esc(item['path'])}</span></li>" for item in rows
        ) or "<li><span>No visible controls in this station.</span></li>"
        station_sections.append(f"<section><h3>{esc(station.replace('-', ' ').title())}</h3><ul>{items}</ul></section>")

    helps = "".join(f"<li>{esc(item)}</li>" for item in review["summary"]["what_helps"])
    friction = "".join(f"<li>{esc(item)}</li>" for item in review["summary"]["what_gets_in_way"])
    proposal_cards = "".join(
        "<article class='proposal'>"
        f"<div class='number'>{item['number']}</div>"
        f"<div><p class='tag'>{esc(item['action'])} · {esc(item['confidence'])} confidence</p>"
        f"<h3>{esc(item['proposal'])}</h3><p>{esc(item['user_impact'])}</p>"
        f"<p><strong>Risk:</strong> {esc(item['risk'])}</p>"
        f"<p><strong>Rollback:</strong> {esc(item['rollback'])}</p></div></article>"
        for item in proposals
    ) or "<p>No changes were proposed in this review.</p>"
    gaps = "".join(f"<li>{esc(item)}</li>" for item in review["coverage_gaps"])
    top = "".join(f"<li>{esc(item['proposal'])}</li>" for item in proposals[:3]) or "<li>No change proposals.</li>"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Your AI Setup</title><style>
:root{{--ink:#17221d;--muted:#5f6d65;--paper:#f5f1e8;--card:#fffdf8;--accent:#1f6b50;--line:#d8d2c4}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,sans-serif}}
main{{max-width:1000px;margin:auto;padding:48px 24px 72px}}h1{{font-size:clamp(2.3rem,6vw,4.8rem);line-height:.95;margin:.2em 0}}
h2{{margin-top:2.4em}}.lede{{font-size:1.25rem;max-width:760px}}.meta,.tag,span{{color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}section,.proposal{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px}}
ul{{padding-left:1.2em}}section li{{margin:.5em 0}}section li span{{display:block;font-size:.88rem;overflow-wrap:anywhere}}
.proposal{{display:grid;grid-template-columns:48px 1fr;gap:14px;margin:14px 0}}.number{{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:var(--accent);color:white;font-weight:700}}
.notice{{border-left:5px solid var(--accent);padding:14px 18px;background:#e9f1eb}}code{{overflow-wrap:anywhere}}
</style></head><body><main>
<p class="meta">Read-only Codex harness review · {esc(scope['scanned_at'])}</p>
<h1>Your AI Setup</h1><p class="lede">{esc(review['summary']['headline'])}</p>
<p class="notice">Nothing in the audited setup was changed. This report can record approvals, but v1 has no apply command.</p>
<h2>What matters most</h2><ol>{top}</ol>
<div class="grid"><section><h2>What helps</h2><ul>{helps}</ul></section><section><h2>What may get in the way</h2><ul>{friction}</ul></section></div>
<h2>Setup map</h2><div class="grid">{''.join(station_sections)}</div>
<h2>Numbered proposals</h2>{proposal_cards}
<h2>What this review could not see</h2><ul>{gaps}</ul>
<p class="meta">Scan {esc(scope['scan_id'])} · baseline {esc(scope['baseline_fingerprint'][:12])} · {len(controls)} tracked controls</p>
</main></body></html>"""


def _render_evidence(
    scope: dict[str, Any], inventory: dict[str, Any], review: dict[str, Any], proposals: list[dict[str, Any]]
) -> str:
    lines = [
        "# Harness Review Evidence",
        "",
        f"- Scan: `{scope['scan_id']}`",
        f"- Baseline: `{scope['baseline_fingerprint']}`",
        f"- Commit: `{scope['head']}`",
        f"- Tracked controls: {len(inventory['controls'])}",
        f"- Semantically selected: {scope['semantic_selected_count']}",
        "- Source mutation: none",
        "",
        "## Decisions",
        "",
    ]
    for decision in review["decisions"]:
        lines.append(f"- **{decision['action']}** — {decision['proposal']} ({', '.join(decision['control_ids'])})")
    if not review["decisions"]:
        lines.append("- No semantic decisions recorded.")
    lines.extend(["", "## Proposals", ""])
    for proposal in proposals:
        lines.append(f"{proposal['number']}. `{proposal['proposal_id']}` — {proposal['proposal']}")
    if not proposals:
        lines.append("No change proposals.")
    lines.extend(["", "## Coverage gaps", ""])
    lines.extend(f"- {gap}" for gap in review["coverage_gaps"])
    return "\n".join(lines) + "\n"


def _included(path: str) -> bool:
    if path in ROOT_FILES or path in GOVERNANCE_DOCS or path == "cli/README.md":
        return True
    parts = PurePosixPath(path).parts
    if len(parts) >= 2 and parts[0] == ".github" and parts[1] == "workflows":
        return path.endswith((".yml", ".yaml"))
    if parts and parts[0] == "skills":
        return path == "skills/README.md" or parts[-1] == "SKILL.md" or tuple(parts[-2:]) == ("agents", "openai.yaml")
    if len(parts) == 2 and parts[0] == "tests" and parts[1].startswith("test_") and parts[1].endswith(".py"):
        return True
    if parts and parts[0] == "projects":
        if len(parts) == 2 and parts[1].endswith(".md"):
            return True
        return len(parts) == 3 and parts[2] in PROJECT_SETUP_NAMES
    return False


def _classify(path: str) -> tuple[str, str]:
    parts = PurePosixPath(path).parts
    if parts[0] == "skills":
        return ("skill-catalog" if path == "skills/README.md" else "skill-route", "routing")
    if parts[0] == "projects":
        return "project-setup", "selected-context"
    if parts[0] in {"tests", ".github"}:
        return ("test" if parts[0] == "tests" else "ci-workflow", "completion-evidence")
    if path == "pyproject.toml" or path == "cli/README.md" or path.endswith(".yaml"):
        return "capability-or-contract", "capabilities-authority"
    return "standing-instruction", "standing-context"


def _metadata(path: str, raw: bytes) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    if path.endswith("SKILL.md"):
        frontmatter = _frontmatter(raw)
        name = frontmatter.get("name")
        description = frontmatter.get("description")
        if isinstance(name, str) and name.strip():
            metadata["label"] = name.strip()
            metadata["declared_name"] = name.strip()
        if isinstance(description, str) and description.strip():
            metadata["description"] = description.strip()[:500]
    elif path.endswith("agents/openai.yaml"):
        data = _safe_yaml(raw)
        policy = data.get("policy") if isinstance(data, dict) else None
        interface = data.get("interface") if isinstance(data, dict) else None
        if isinstance(interface, dict) and isinstance(interface.get("display_name"), str):
            metadata["label"] = interface["display_name"][:100]
        if isinstance(policy, dict) and isinstance(policy.get("allow_implicit_invocation"), bool):
            metadata["allow_implicit_invocation"] = policy["allow_implicit_invocation"]
    return metadata


def _frontmatter(raw: bytes) -> dict[str, Any]:
    text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    data = yaml.safe_load(text[4:end]) or {}
    return data if isinstance(data, dict) else {}


def _safe_yaml(raw: bytes) -> Any:
    try:
        return yaml.safe_load(raw.decode("utf-8", errors="replace")) or {}
    except yaml.YAMLError:
        return {}


def _semantic_priority(item: dict[str, Any]) -> tuple[int, str]:
    priority = {
        "standing-context": 0,
        "routing": 1,
        "capabilities-authority": 2,
        "completion-evidence": 3,
        "selected-context": 4,
    }
    return priority[item["station"]], item["path"]


def _control_id(path: str) -> str:
    return "ctl-" + _sha256(path.encode("utf-8"))[:12]


def _portable_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or not pure.parts or any(part in {"", ".", ".."} for part in pure.parts):
        raise HarnessReviewError(f"Unsafe tracked path: {path}")
    return pure.as_posix()


def _ensure_within(path: Path, root: Path) -> None:
    try:
        os.path.commonpath((str(path), str(root)))
    except ValueError as exc:
        raise HarnessReviewError("Path is outside the permitted review root.") from exc
    if os.path.commonpath((str(path), str(root))) != str(root):
        raise HarnessReviewError("Path is outside the permitted review root.")


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, check=False, text=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode:
        raise HarnessReviewError(result.stderr.decode("utf-8", errors="replace").strip() or "Git command failed.")
    return result.stdout.decode("utf-8", errors="replace").strip("\0\r\n")


def _git_paths(root: Path, *args: str) -> list[str]:
    value = _git(root, *args)
    return [part for part in value.split("\0") if part]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessReviewError(f"Cannot read valid JSON artifact: {path.name}") from exc
    if not isinstance(value, dict):
        raise HarnessReviewError(f"JSON artifact must be an object: {path.name}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _file_hash(path: Path) -> str:
    return _sha256(path.read_bytes())


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_nonempty(item) for item in value)
