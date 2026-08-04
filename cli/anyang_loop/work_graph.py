from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path, PurePosixPath
import re
from typing import Any

import yaml

from .privacy_scan import scan_text


DECLARATION_VERSION = "anyang-work-graph/v1"
STATUS_VERSION = "anyang-graph-status/v1"
MAX_PACKET_BYTES = 131_072
MAX_NODES = 100
MAX_TEXT = 500
NODE_KINDS = {"inspection", "workspace-change", "validation", "decision", "action", "artifact"}
ACTION_BOUNDARIES = {
    "read-only",
    "repository-write",
    "commit",
    "push",
    "send",
    "external-action",
    "human-judgment",
}
NODE_STATES = {
    "pending",
    "ready",
    "needs-judgment",
    "in-progress",
    "satisfied",
    "blocked",
    "stale",
    "held",
    "superseded",
    "unknown",
}
RULE_FIELDS = {
    "git-head": ({"type", "expected"}, set()),
    "git-changes-within-scope": ({"type"}, set()),
    "git-commit": ({"type", "commit"}, set()),
    "git-remote-tracking-contains": ({"type", "ref", "commit"}, set()),
    "validation-full-pass": ({"type"}, set()),
    "file-exists": ({"type", "path"}, set()),
    "file-sha256": ({"type", "path", "sha256"}, set()),
    "council-projection": ({"type", "transaction_id"}, {"current_state", "subject_hash"}),
    "council-event-chain": ({"type", "transaction_id"}, set()),
    "explicit-reference": ({"type", "source_ref"}, set()),
}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,79}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
REF_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/@:+#-]{0,299}$")


class WorkGraphError(ValueError):
    pass


def load_work_graph(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        raw = source.read_bytes()
    except OSError as exc:
        raise WorkGraphError(f"Unable to read work graph: {exc}") from exc
    if len(raw) > MAX_PACKET_BYTES:
        raise WorkGraphError("Work graph packet is oversized")
    try:
        packet = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise WorkGraphError(f"Invalid work graph YAML: {exc}") from exc
    if not isinstance(packet, dict):
        raise WorkGraphError("Work graph packet must be an object")
    return packet


def load_graph_status(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        raw = source.read_bytes()
    except OSError as exc:
        raise WorkGraphError(f"Unable to read graph status: {exc}") from exc
    if len(raw) > MAX_PACKET_BYTES * 4:
        raise WorkGraphError("Graph status packet is oversized")
    try:
        packet = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkGraphError(f"Invalid graph status JSON: {exc}") from exc
    if not isinstance(packet, dict):
        raise WorkGraphError("Graph status packet must be an object")
    return packet


def validate_work_graph(packet: dict[str, Any], repo_root: str | Path | None = None) -> dict[str, Any]:
    _exact_fields(
        packet,
        {"contract_version", "graph_id", "objective", "objective_ref", "scope", "nodes"},
        set(),
        "work graph",
    )
    if packet["contract_version"] != DECLARATION_VERSION:
        raise WorkGraphError(f"Unsupported contract_version: {packet['contract_version']!r}")
    _identifier(packet["graph_id"], "graph_id")
    _safe_text(packet["objective"], "objective")
    _safe_ref(packet["objective_ref"], "objective_ref")
    scope = packet["scope"]
    if not isinstance(scope, dict):
        raise WorkGraphError("scope must be an object")
    _exact_fields(scope, {"repository", "permitted_paths"}, {"tenant", "excluded_paths"}, "scope")
    _safe_text(scope["repository"], "scope.repository", limit=100)
    if "tenant" in scope:
        _identifier(scope["tenant"], "scope.tenant")
    permitted = _path_list(scope["permitted_paths"], "scope.permitted_paths", allow_empty=False)
    excluded = _path_list(scope.get("excluded_paths", []), "scope.excluded_paths", allow_empty=True)
    if set(permitted) & set(excluded):
        raise WorkGraphError("A path cannot be both permitted and excluded")
    nodes = packet["nodes"]
    if not isinstance(nodes, list) or not nodes or len(nodes) > MAX_NODES:
        raise WorkGraphError(f"nodes must contain 1-{MAX_NODES} entries")
    identifiers: set[str] = set()
    for index, node in enumerate(nodes):
        _validate_node(node, index)
        if node["id"] in identifiers:
            raise WorkGraphError(f"Duplicate node ID: {node['id']}")
        identifiers.add(node["id"])
    for node in nodes:
        for dependency in node.get("depends_on", []):
            if dependency not in identifiers:
                raise WorkGraphError(f"Node {node['id']} has unknown dependency {dependency}")
            if dependency == node["id"]:
                raise WorkGraphError(f"Node {node['id']} cannot depend on itself")
        superseding = node.get("superseded_by")
        if superseding is not None and superseding not in identifiers:
            raise WorkGraphError(f"Node {node['id']} has unknown superseded_by target {superseding}")
    _reject_cycles(nodes)
    if repo_root is not None:
        _validate_resolved_paths(packet, Path(repo_root).resolve())
    findings = scan_text(json.dumps(packet, sort_keys=True, ensure_ascii=False))
    if findings:
        raise WorkGraphError(f"Work graph failed privacy scan: {', '.join(sorted(findings))}")
    return packet


def evaluate_work_graph(
    packet: dict[str, Any],
    evidence: dict[str, Any],
    *,
    as_of: str,
) -> dict[str, Any]:
    validate_work_graph(packet)
    normalized_as_of = _rfc3339(as_of)
    node_map = {node["id"]: node for node in packet["nodes"]}
    states: dict[str, str] = {}

    def state_for(identifier: str) -> str:
        if identifier in states:
            return states[identifier]
        node = node_map[identifier]
        superseding = node.get("superseded_by")
        if superseding and state_for(superseding) == "satisfied":
            states[identifier] = "superseded"
            return "superseded"
        dependency_states = [state_for(item) for item in node.get("depends_on", [])]
        if any(item in {"held", "blocked", "stale", "unknown"} for item in dependency_states):
            states[identifier] = "blocked"
            return "blocked"
        if any(item not in {"satisfied", "superseded"} for item in dependency_states):
            states[identifier] = "pending"
            return "pending"
        results = evidence["nodes"].get(identifier, [])
        statuses = [item["status"] for item in results]
        if "held" in statuses:
            derived = "held"
        elif "stale" in statuses:
            derived = "stale"
        elif "unknown" in statuses:
            derived = "unknown"
        elif statuses and all(item == "satisfied" for item in statuses):
            derived = "satisfied"
        elif "satisfied" in statuses or "present" in statuses:
            derived = "in-progress"
        elif _requires_judgment(node):
            derived = "needs-judgment"
        else:
            derived = "ready"
        states[identifier] = derived
        return derived

    projected_nodes: list[dict[str, Any]] = []
    attention: list[dict[str, Any]] = []
    next_actions: list[dict[str, Any]] = []
    for identifier in sorted(node_map):
        node = node_map[identifier]
        state = state_for(identifier)
        node_evidence = evidence["nodes"].get(identifier, [])
        boundary = node.get("action_boundary", "read-only")
        authority_status = "referenced" if node.get("authority_ref") else "Missing"
        projected_nodes.append(
            {
                "id": identifier,
                "kind": node["kind"],
                "summary": node["summary"],
                "state": state,
                "depends_on": sorted(node.get("depends_on", [])),
                "action_boundary": boundary,
                "authority_status": authority_status,
                "authority_ref": node.get("authority_ref", "Missing"),
                "evidence": node_evidence,
                "optional": bool(node.get("optional", False)),
            }
        )
        if state == "held":
            attention.append(_flag(0, "evidence-integrity-hold", identifier, "hold → node → resolve evidence or membrane failure"))
        elif state in {"blocked", "stale", "unknown"}:
            attention.append(_flag(1, f"node-{state}", identifier, "inspect → evidence → restore a verifiable path"))
        elif state == "needs-judgment":
            attention.append(_flag(2, "judgment-required", identifier, "judge → node → permit or stop the bounded action"))
            next_actions.append(_next_action(node, state))
        elif state == "ready":
            attention.append(_flag(3, "node-ready", identifier, "advance → node → produce declared evidence"))
            next_actions.append(_next_action(node, state))
        if state == "satisfied" and boundary != "read-only" and authority_status == "Missing":
            attention.append(_flag(1, "authority-lineage-missing", identifier, "reconcile → authority reference → preserve action lineage"))
    required = [node for node in projected_nodes if not node["optional"]]
    required_states = {node["state"] for node in required}
    if "held" in required_states or any(item["priority"] == 0 for item in attention):
        disposition = "hold"
    elif required and all(node["state"] in {"satisfied", "superseded"} for node in required):
        disposition = "complete"
    elif "needs-judgment" in required_states:
        disposition = "needs-judgment"
    elif required_states & {"blocked", "stale", "unknown"}:
        disposition = "blocked"
    else:
        disposition = "ready"
    changed = set(evidence["source_snapshot"].get("changed_paths", []))
    exclusions = [
        {
            "path": path,
            "changed": any(
                item == path.rstrip("/") or item.startswith(path.rstrip("/") + "/")
                for item in changed
            ),
        }
        for path in sorted(packet["scope"].get("excluded_paths", []))
    ]
    projection: dict[str, Any] = {
        "contract_version": STATUS_VERSION,
        "authority_effect": "none",
        "as_of": normalized_as_of,
        "graph": {
            "graph_id": packet["graph_id"],
            "objective": packet["objective"],
            "objective_ref": packet["objective_ref"],
            "scope": packet["scope"],
            "declaration_digest": _hash(packet),
        },
        "source_snapshot": evidence["source_snapshot"],
        "disposition": disposition,
        "nodes": projected_nodes,
        "edges": [
            {"from": dependency, "to": node["id"], "state": _edge_state(states[dependency], states[node["id"]])}
            for node in sorted(packet["nodes"], key=lambda item: item["id"])
            for dependency in sorted(node.get("depends_on", []))
        ],
        "human_gates": [
            {
                "node_id": node["id"],
                "action_boundary": node["action_boundary"],
                "state": node["state"],
                "authority_status": node["authority_status"],
            }
            for node in projected_nodes
            if node["action_boundary"] != "read-only"
        ],
        "attention_flags": sorted(attention, key=lambda item: (item["priority"], item["node_id"], item["code"])),
        "next_permissible_actions": sorted(next_actions, key=lambda item: item["node_id"]),
        "scope_exclusions": exclusions,
        "lineage": [
            {
                "node_id": node["id"],
                "evidence_refs": sorted({ref for item in node["evidence"] for ref in item.get("refs", [])}),
            }
            for node in projected_nodes
        ],
    }
    projection["projection_hash"] = _hash(projection)
    return projection


def verify_graph_status(packet: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    if not isinstance(packet, dict):
        return {"ok": False, "issues": [{"code": "invalid-packet", "message": "Status packet must be an object"}]}
    required = {
        "contract_version", "authority_effect", "as_of", "graph", "source_snapshot",
        "disposition", "nodes", "edges", "human_gates", "attention_flags",
        "next_permissible_actions", "scope_exclusions", "lineage", "projection_hash",
    }
    missing = sorted(required - set(packet))
    unknown = sorted(set(packet) - required)
    if missing:
        issues.append({"code": "missing-fields", "message": ", ".join(missing)})
    if unknown:
        issues.append({"code": "unknown-fields", "message": ", ".join(unknown)})
    if packet.get("contract_version") != STATUS_VERSION:
        issues.append({"code": "unknown-contract-version", "message": str(packet.get("contract_version"))})
    if packet.get("authority_effect") != "none":
        issues.append({"code": "authority-expansion", "message": "authority_effect must be none"})
    try:
        _rfc3339(packet.get("as_of"))
    except WorkGraphError as exc:
        issues.append({"code": "invalid-as-of", "message": str(exc)})
    nodes = packet.get("nodes")
    node_ids: set[str] = set()
    if not isinstance(nodes, list):
        issues.append({"code": "invalid-nodes", "message": "nodes must be a list"})
    else:
        for node in nodes:
            if not isinstance(node, dict) or node.get("state") not in NODE_STATES:
                issues.append({"code": "invalid-node-state", "message": "A node has an unsupported state"})
                break
            identifier = node.get("id")
            if not isinstance(identifier, str) or not ID_RE.fullmatch(identifier) or identifier in node_ids:
                issues.append({"code": "invalid-node-id", "message": "Node IDs must be unique stable identifiers"})
                break
            node_ids.add(identifier)
            if node.get("action_boundary") not in ACTION_BOUNDARIES:
                issues.append({"code": "invalid-action-boundary", "message": f"Node {identifier} has an unsupported boundary"})
            if not isinstance(node.get("evidence"), list):
                issues.append({"code": "invalid-node-evidence", "message": f"Node {identifier} evidence must be a list"})
    if packet.get("disposition") not in {"complete", "ready", "needs-judgment", "blocked", "hold"}:
        issues.append({"code": "invalid-disposition", "message": "Unsupported graph disposition"})
    for key in ("edges", "human_gates", "attention_flags", "next_permissible_actions", "scope_exclusions", "lineage"):
        if not isinstance(packet.get(key), list):
            issues.append({"code": f"invalid-{key}", "message": f"{key} must be a list"})
    if not isinstance(packet.get("graph"), dict) or not isinstance(packet.get("source_snapshot"), dict):
        issues.append({"code": "invalid-projection", "message": "graph and source_snapshot must be objects"})
    if isinstance(packet.get("edges"), list):
        for edge in packet["edges"]:
            if not isinstance(edge, dict) or edge.get("from") not in node_ids or edge.get("to") not in node_ids:
                issues.append({"code": "invalid-edge", "message": "An edge references an unknown node"})
                break
    if isinstance(packet.get("lineage"), list):
        lineage_ids = {
            item.get("node_id") for item in packet["lineage"] if isinstance(item, dict)
        }
        if lineage_ids != node_ids or len(packet["lineage"]) != len(node_ids):
            issues.append({"code": "invalid-lineage", "message": "Lineage must cover every node exactly once"})
    findings = scan_text(json.dumps(packet, sort_keys=True, ensure_ascii=False))
    if findings:
        issues.append({"code": "privacy-failure", "message": ", ".join(sorted(findings))})
    supplied = packet.get("projection_hash")
    body = dict(packet)
    body.pop("projection_hash", None)
    if not isinstance(supplied, str) or not HASH_RE.fullmatch(supplied) or supplied != _hash(body):
        issues.append({"code": "projection-hash-mismatch", "message": "Projection content differs from its hash"})
    return {"ok": not issues, "contract_version": STATUS_VERSION, "issues": issues, "authority_effect": "none"}


def render_graph_json(projection: dict[str, Any]) -> str:
    return json.dumps(projection, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def render_graph_markdown(projection: dict[str, Any]) -> str:
    graph = projection["graph"]
    lines = [
        f"# Work Graph Status: {graph['graph_id']}",
        "",
        f"- Objective: {graph['objective']}",
        f"- Disposition: `{projection['disposition']}`",
        f"- As of: `{projection['as_of']}`",
        "- Authority effect: `none`",
        f"- Projection hash: `{projection['projection_hash']}`",
        "",
        "## Nodes",
        "",
        "| Node | State | Boundary | Authority |",
        "| --- | --- | --- | --- |",
    ]
    for node in projection["nodes"]:
        lines.append(f"| `{node['id']}` | `{node['state']}` | `{node['action_boundary']}` | `{node['authority_status']}` |")
    lines.extend(("", "## Attention", ""))
    if projection["attention_flags"]:
        for item in projection["attention_flags"]:
            lines.append(f"- P{item['priority']} `{item['code']}` / `{item['node_id']}`: {item['message']}")
    else:
        lines.append("- None.")
    lines.extend(("", "## Next Permissible Actions", ""))
    if projection["next_permissible_actions"]:
        for item in projection["next_permissible_actions"]:
            lines.append(f"- `{item['node_id']}` [{item['action_boundary']}]: {item['summary']}")
    else:
        lines.append("- None.")
    lines.extend(("", "## Scope Exclusions", ""))
    if projection["scope_exclusions"]:
        for item in projection["scope_exclusions"]:
            lines.append(f"- `{item['path']}`: {'changed and excluded' if item['changed'] else 'excluded'}")
    else:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def _validate_node(node: Any, index: int) -> None:
    if not isinstance(node, dict):
        raise WorkGraphError(f"nodes[{index}] must be an object")
    _exact_fields(
        node,
        {"id", "kind", "summary"},
        {"depends_on", "completion", "action_boundary", "human_gate", "authority_ref", "optional", "superseded_by"},
        f"nodes[{index}]",
    )
    _identifier(node["id"], f"nodes[{index}].id")
    if node["kind"] not in NODE_KINDS:
        raise WorkGraphError(f"nodes[{index}].kind is unsupported")
    _safe_text(node["summary"], f"nodes[{index}].summary")
    dependencies = node.get("depends_on", [])
    if not isinstance(dependencies, list) or len(dependencies) != len(set(dependencies)):
        raise WorkGraphError(f"nodes[{index}].depends_on must be a unique list")
    for dependency in dependencies:
        _identifier(dependency, f"nodes[{index}].depends_on")
    completion = node.get("completion", [])
    if not isinstance(completion, list) or len(completion) > 20:
        raise WorkGraphError(f"nodes[{index}].completion must be a bounded list")
    for rule_index, rule in enumerate(completion):
        _validate_rule(rule, f"nodes[{index}].completion[{rule_index}]")
    boundary = node.get("action_boundary", "read-only")
    if boundary not in ACTION_BOUNDARIES:
        raise WorkGraphError(f"nodes[{index}].action_boundary is unsupported")
    human_gate = node.get("human_gate", "none")
    if human_gate not in {"none", "required"}:
        raise WorkGraphError(f"nodes[{index}].human_gate must be none or required")
    if boundary != "read-only" and human_gate != "required":
        raise WorkGraphError(f"nodes[{index}] mutation boundary requires human_gate: required")
    if "authority_ref" in node:
        _safe_ref(node["authority_ref"], f"nodes[{index}].authority_ref")
    if "optional" in node and not isinstance(node["optional"], bool):
        raise WorkGraphError(f"nodes[{index}].optional must be boolean")
    if "superseded_by" in node:
        _identifier(node["superseded_by"], f"nodes[{index}].superseded_by")


def _validate_rule(rule: Any, label: str) -> None:
    if not isinstance(rule, dict) or not isinstance(rule.get("type"), str):
        raise WorkGraphError(f"{label} must name an evidence type")
    kind = rule["type"]
    if kind not in RULE_FIELDS:
        raise WorkGraphError(f"{label}.type is unsupported: {kind!r}")
    required, optional = RULE_FIELDS[kind]
    _exact_fields(rule, required, optional, label)
    for key, value in rule.items():
        if key == "type":
            continue
        if key in {"path"}:
            _relative_path(value, f"{label}.{key}")
        elif key in {"sha256", "subject_hash"}:
            if not isinstance(value, str) or not HASH_RE.fullmatch(value):
                raise WorkGraphError(f"{label}.{key} must be a lowercase SHA-256 digest")
        elif key in {"commit", "expected"}:
            if not isinstance(value, str) or not COMMIT_RE.fullmatch(value):
                raise WorkGraphError(f"{label}.{key} must be an exact lowercase Git commit ID")
        else:
            _safe_ref(value, f"{label}.{key}")


def _reject_cycles(nodes: list[dict[str, Any]]) -> None:
    graph = {
        node["id"]: [
            *node.get("depends_on", []),
            *([node["superseded_by"]] if node.get("superseded_by") else []),
        ]
        for node in nodes
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            raise WorkGraphError(f"Dependency cycle includes {identifier}")
        if identifier in visited:
            return
        visiting.add(identifier)
        for dependency in graph[identifier]:
            visit(dependency)
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in sorted(graph):
        visit(identifier)


def _validate_resolved_paths(packet: dict[str, Any], root: Path) -> None:
    for label, paths in (
        ("permitted", packet["scope"]["permitted_paths"]),
        ("excluded", packet["scope"].get("excluded_paths", [])),
    ):
        for relative in paths:
            _inside_root(root, relative, f"{label} path")
    for node in packet["nodes"]:
        for rule in node.get("completion", []):
            if "path" in rule:
                resolved = _inside_root(root, rule["path"], "evidence path")
                if not any(_path_contains(root / prefix, resolved) for prefix in packet["scope"]["permitted_paths"]):
                    raise WorkGraphError(f"Evidence path is outside permitted scope: {rule['path']}")


def _inside_root(root: Path, relative: str, label: str) -> Path:
    resolved = (root / relative).resolve()
    if not _path_contains(root, resolved):
        raise WorkGraphError(f"{label} escapes the repository: {relative}")
    return resolved


def _path_contains(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _path_list(value: Any, label: str, *, allow_empty: bool) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty) or len(value) > 100:
        raise WorkGraphError(f"{label} must be a bounded list")
    paths = [_relative_path(item, label) for item in value]
    if len(paths) != len(set(paths)):
        raise WorkGraphError(f"{label} contains duplicates")
    return paths


def _relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 300:
        raise WorkGraphError(f"{label} must be a bounded relative path")
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        raise WorkGraphError(f"{label} must remain repository-relative")
    if normalized != path.as_posix() or normalized in {"", "."}:
        raise WorkGraphError(f"{label} is not normalized")
    return normalized


def _exact_fields(value: dict[str, Any], required: set[str], optional: set[str], label: str) -> None:
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - required - optional)
    if missing:
        raise WorkGraphError(f"{label} is missing fields: {', '.join(missing)}")
    if unknown:
        raise WorkGraphError(f"{label} has unknown fields: {', '.join(unknown)}")


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        raise WorkGraphError(f"{label} must be a stable lowercase identifier")
    return value


def _safe_text(value: Any, label: str, *, limit: int = MAX_TEXT) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit or any(ord(char) < 32 and char not in "\t\n" for char in value):
        raise WorkGraphError(f"{label} must be bounded text")
    return value


def _safe_ref(value: Any, label: str) -> str:
    if not isinstance(value, str) or not REF_RE.fullmatch(value):
        raise WorkGraphError(f"{label} must be a bounded source reference")
    return value


def _rfc3339(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise WorkGraphError("as_of must be an RFC3339 timestamp")
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise WorkGraphError("as_of must be an RFC3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise WorkGraphError("as_of must include a timezone")
    return value


def _requires_judgment(node: dict[str, Any]) -> bool:
    return node.get("human_gate", "none") == "required" or node.get("action_boundary", "read-only") != "read-only"


def _edge_state(source: str, target: str) -> str:
    if source in {"satisfied", "superseded"}:
        return "satisfied" if target == "satisfied" else "eligible"
    if source == "held":
        return "held"
    return "blocked"


def _flag(priority: int, code: str, node_id: str, message: str) -> dict[str, Any]:
    return {"priority": priority, "code": code, "node_id": node_id, "message": message}


def _next_action(node: dict[str, Any], state: str) -> dict[str, Any]:
    boundary = node.get("action_boundary", "read-only")
    return {
        "node_id": node["id"],
        "state": state,
        "action_boundary": boundary,
        "summary": f"advance → {node['summary']} → produce declared evidence",
        "requires_explicit_authority": boundary != "read-only",
    }


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()
