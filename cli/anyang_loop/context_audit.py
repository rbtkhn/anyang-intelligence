from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse


@dataclass(frozen=True)
class Finding:
    finding_id: str
    severity: str
    category: str
    path: str
    line: int | None
    claim_or_reference: str
    evidence: str
    recommended_action: str
    human_decision_required: bool

    def as_dict(self) -> dict:
        return asdict(self)


LINK_RE = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
DATE_RE = re.compile(r"\b(?:20\d{2})[-/]\d{2}[-/]\d{2}\b")
AUTH_TERMS = re.compile(r"\b(?:approval|authority|permission|publish|customer.?route|mutation|delete|spend|signing)\b", re.I)
FRESH_TERMS = re.compile(r"\b(?:fresh|stale|review cadence|review date|effective date|as of|owner|superseded|provisional)\b", re.I)
HISTORICAL_TERMS = re.compile(r"\b(?:historical|superseded|provisional|archived|exemplar|template|retired)\b", re.I)


def _is_historical_document(path: Path, text: str) -> bool:
    parts = {part.lower() for part in path.parts}
    if {"archive", "templates"} & parts:
        return True
    if any(term in path.name.lower() for term in ("exemplar", "template", "historical", "superseded")):
        return True
    return bool(HISTORICAL_TERMS.search("\n".join(text.splitlines()[:24])))


def _files(root: Path) -> list[Path]:
    ignored = {".git", ".pytest_cache", "__pycache__", ".venv", "node_modules"}
    return sorted(
        p for p in root.rglob("*")
        if p.is_file()
        and not p.name.startswith("repo-context-integrity-audit-")
        and not any(part in ignored and part != root.name for part in p.relative_to(root).parts)
    )


def _finding(seq: int, severity: str, category: str, path: Path, line: int | None, claim: str, evidence: str, action: str, human: bool = False) -> Finding:
    return Finding(f"CIA-{seq:04d}", severity, category, path.as_posix(), line, claim, evidence, action, human)


def audit_repository(repo: str | Path = ".") -> dict:
    root = Path(repo).resolve()
    files = _files(root)
    findings: list[Finding] = []
    seq = 1

    def add(*args, **kwargs):
        nonlocal seq
        findings.append(_finding(seq, *args, **kwargs))
        seq += 1

    markdown = [p for p in files if p.suffix.lower() in {".md", ".markdown"}]
    authority_positions: list[tuple[Path, str]] = []
    for path in markdown:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for number, line in enumerate(lines, 1):
            for raw in LINK_RE.findall(line):
                target = raw.split("#", 1)[0].strip().strip("<>")
                if not target or urlparse(target).scheme or target.startswith("mailto:"):
                    continue
                decoded = unquote(target)
                if "repo_probe/" in decoded.replace("\\", "/"):
                    decoded = decoded.replace("\\", "/").split("repo_probe/", 1)[1]
                    candidate = (root / decoded).resolve()
                else:
                    candidate = (path.parent / decoded).resolve()
                    if not candidate.exists() and decoded.startswith("../../primitives/") and "/analyses/" in path.as_posix():
                        candidate = (path.parent.parent.parent / decoded.split("../../", 1)[1]).resolve()
                if not candidate.exists():
                    add("error", "broken-link", path.relative_to(root), number, target, "linked target does not exist", "Repair the link or mark the reference intentional")

        text = "\n".join(lines)
        if AUTH_TERMS.search(text):
            authority_positions.append((path, text.lower()))
        if AUTH_TERMS.search(text) and not _is_historical_document(path, text) and not DATE_RE.search(text) and not FRESH_TERMS.search(text):
            add("warning", "freshness-metadata", path.relative_to(root), None, "authority-bearing document", "authority language has no visible date, owner, cadence, or freshness marker", "Add effective date, owner, review trigger, or explicit non-current status", True)

    granting = []
    limiting = []
    for path, text in authority_positions:
        grants = re.search(r"\b(?:grants?|creates?)\s+(?:authority|permission)", text)
        limits = re.search(r"\b(?:never|does not|do not)\s+(?:grant|grants|create|creates)\s+(?:authority|permission)", text)
        # A policy document commonly states both the bounded grant and its
        # non-granting boundary. That is clarification, not a cross-document
        # contradiction.
        if limits:
            limiting.append(path)
        elif grants:
            granting.append(path)
    if granting and limiting:
        add("warning", "authority-conflict", root, None, "granting versus limiting authority language", f"{len(granting)} document(s) describe granting authority while {len(limiting)} describe withholding it", "Review scope, precedence, and whether the statements describe different phases", True)

    tracked_like = [p for p in files if p.suffix.lower() in {".md", ".yaml", ".yml", ".json"}]
    index_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in markdown if p.name.lower() in {"readme.md", "index.md"} or "ledger" in p.name.lower() or "manifest" in p.name.lower())
    for path in tracked_like:
        if path.name == ".gitkeep" or any(part in {"transcripts", "__pycache__"} for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        if path.stat().st_size > 0 and rel not in index_text and path.name not in {"README.md", "index.md"} and path.parent.name not in {"tests", "cli"}:
            add("info", "discoverability", path.relative_to(root), None, rel, "artifact is not named by a README, index, ledger, or manifest scan", "Add an intentional index link or classify the artifact as internal/derived", True)

    for path in files:
        rel = path.relative_to(root).as_posix()
        source_material = path.name.lower().endswith((".md", ".txt", ".markdown")) and (
            "transcript" in path.name.lower() or "transcripts" in rel.split("/")
        )
        if source_material and "archive" not in rel.replace("\\", "/"):
            add("error", "membrane-boundary", path.relative_to(root), None, rel, "transcript-like material is outside the archive path", "Move or redact the source material after rights and membrane review", True)

    for lane in root.glob("operating-substrate/projects/singularity-science/archive/*"):
        if not lane.is_dir():
            continue
        transcripts = {p.stem for p in (lane / "transcripts").glob("*.md")}
        notes = {p.name.replace(".source-note", "") for p in (lane / "source-notes").glob("*.md")}
        analyses = {p.name.replace(".analysis", "") for p in (lane / "analyses").glob("*.md")}
        for stem in sorted(transcripts - notes - analyses):
            add("warning", "archive-linkage", lane.relative_to(root), None, stem, "transcript lacks a matching source note and analysis", "Complete the governed intake packet or record an intentional hold")

    findings.sort(key=lambda item: (item.path, item.line or 0, item.category, item.claim_or_reference))
    findings = [Finding(f"CIA-{i:04d}", item.severity, item.category, item.path, item.line, item.claim_or_reference, item.evidence, item.recommended_action, item.human_decision_required) for i, item in enumerate(findings, 1)]
    counts = Counter(item.severity for item in findings)
    return {"schema_version": 1, "repo": str(root), "read_only": True, "findings": [item.as_dict() for item in findings], "counts": dict(sorted(counts.items())), "non_findings": ["Existing validators remain authoritative for project installs, authority envelopes, epistemic manifests, artifact state, bounded agency, and privacy scans.", "Archive transcripts are not treated as orphaned merely because they are not customer-routed.", "Ordinary findings do not affect command exit status."]}


def render_markdown(report: dict) -> str:
    counts = report["counts"]
    lines = ["# Repository Context-Integrity Audit — 2026-07-23", "", "## Executive judgment", "", "This read-only baseline identifies discoverability, linkage, freshness, broken-reference, and membrane risks. Findings are evidence for review, not proof of operational failure or ROI.", "", f"Findings: {sum(counts.values())} (" + ", ".join(f"{k}: {v}" for k, v in counts.items()) + ")", "", "## Priority queue", ""]
    priority = sorted(report["findings"], key=lambda f: ({"error": 0, "warning": 1, "info": 2}[f["severity"]], f["category"], f["path"]))[:5]
    for item in priority:
        lines.append(f"- **{item['severity'].upper()} {item['category']}** `{item['path']}`: {item['evidence']}. Action: {item['recommended_action']}.")
    lines += ["", "## Findings", "", "| ID | Severity | Category | Path | Line | Evidence | Human decision |", "| --- | --- | --- | --- | ---: | --- | --- |"]
    for item in report["findings"]:
        lines.append(f"| {item['finding_id']} | {item['severity']} | {item['category']} | `{item['path']}` | {item['line'] or ''} | {item['evidence']} | {'yes' if item['human_decision_required'] else 'no'} |")
    lines += ["", "## Non-findings", ""] + [f"- {item}" for item in report["non_findings"]] + ["", "## Boundary", "", "This audit is internal repository evidence. It does not grant authority, approve publication or routing, establish rights or security clearance, or establish customer ROI.", ""]
    return "\n".join(lines)


def write_audit(repo: str | Path, output: str | Path, fmt: str) -> Path:
    report = audit_repository(repo)
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) if fmt == "json" else render_markdown(report), encoding="utf-8")
    return destination
