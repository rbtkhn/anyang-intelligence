from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any

import yaml

from .ops_service import MutationResult, OpsError, now_utc, tenant_id
from .privacy_scan import scan_text


CHOICE_ROLES = ("recommended", "alternative", "overlooked", "pause-or-deepen")
ELICITATION_INTERACTION_TYPES = ("decision-navigation", "neutral-evidence")
ELICITATION_ACTION_VERBS = ("Execute", "Commit", "Push", "Send")
CONSEQUENCE_LEVELS = ("ordinary", "consequential", "authority-sensitive")
CHOICE_CLASSIFICATION_VERSION = "LFC-CONTINUITY-v0.2"
CHOICE_PATTERN_KEYS = (
    "gather-evidence",
    "design-next-move",
    "execute-bounded",
    "explore-adjacent",
    "seek-authority",
    "pause-preserve",
)
CHOICE_ACTION_BOUNDARIES = (
    "read-only",
    "workspace-mutation",
    "external-action",
    "authority-decision",
    "stop",
)
CLASSIFICATION_FIELDS = (
    "classification_version",
    "pattern_key",
    "action_boundary",
    "comparability_key",
)
EVENT_TYPES = (
    "outcome_recorded",
    "review_deferred",
    "corrected",
    "superseded",
)
OUTCOME_RESULTS = (
    "successful",
    "mixed",
    "unsuccessful",
    "no_action",
    "not_observable",
)
COGNITIVE_LOAD = ("lower", "same", "higher", "Missing")
MOMENTUM = ("advanced", "neutral", "stalled", "Missing")
DISCOVERY_VALUE = (
    "new-useful-path",
    "confirmed-known-path",
    "not-useful",
    "Missing",
)
TERMINAL_RESULTS = set(OUTCOME_RESULTS)
MAX_TEXT = 500
MAX_JSON = 24000
CHOICE_GUIDANCE_POLICIES = (
    {
        "id": "LFC-CAL-2026-07-30-01",
        "tenant": "anyang-internal",
        "workspace_id": "anyang-intelligence",
        "lane": "repository",
        "guidance_mode": "diagnostic-only",
        "cohort_learning_ref": "LFC-CAL-2026-07-30-01",
        "effective_at": "2026-07-30T06:00:00Z",
        "observation_ends_at": "2026-08-06T06:00:00Z",
        "freeze_until_explicit_disposition": True,
        "source_ref": (
            "repo:docs/learn-from-choices-calibration-pilot-2026-07-30.md"
        ),
    },
)
CHOICE_COMPARABILITY_POLICIES = (
    {
        "id": "repository-authorized-push-v1",
        "status": "diagnostic-only",
        "tenant": "anyang-internal",
        "workspace_id": "anyang-intelligence",
        "lane": "repository",
        "choice_kind": "next-action",
        "consequence_levels": ("ordinary", "consequential"),
        "pattern_key": "execute-bounded",
        "action_boundary": "external-action",
        "minimum_resolved": 3,
        "minimum_consistent": 2,
        "source_ref": (
            "repo:docs/learn-from-choices-continuity-contract-v0.2.md"
        ),
    },
)


def validate_elicitation_surface(surface: dict[str, Any]) -> dict[str, Any]:
    """Validate a low-load decision menu or neutral evidence question."""
    if not isinstance(surface, dict):
        raise OpsError("Elicitation surface must be a mapping")
    interaction_type = _text(surface.get("interaction_type"))
    if interaction_type not in ELICITATION_INTERACTION_TYPES:
        raise OpsError(f"Unsupported elicitation interaction type: {interaction_type}")
    question = _bounded(surface.get("question"), "elicitation question", required=True)
    options = surface.get("options")
    minimum = 3 if interaction_type == "decision-navigation" else 2
    if not isinstance(options, list) or not minimum <= len(options) <= 4:
        expected = "3-4" if interaction_type == "decision-navigation" else "2-4"
        raise OpsError(f"{interaction_type} elicitation requires {expected} options")

    normalized_options: list[dict[str, str]] = []
    seen_keys: set[str] = set()
    seen_labels: set[str] = set()
    seen_roles: set[str] = set()
    for index, option in enumerate(options, start=1):
        if not isinstance(option, dict):
            raise OpsError(f"Elicitation option {index} must be a mapping")
        key = _bounded(
            option.get("key"), f"elicitation option {index} key", required=True, maximum=120
        )
        label = _bounded(
            option.get("label"), f"elicitation option {index} label", required=True
        )
        if key in seen_keys:
            raise OpsError(f"Duplicate elicitation option key: {key}")
        if label.casefold() in seen_labels:
            raise OpsError(f"Duplicate elicitation option label: {label}")
        seen_keys.add(key)
        seen_labels.add(label.casefold())

        normalized = {"key": key, "label": label}
        if interaction_type == "decision-navigation":
            role = _bounded(
                option.get("role"),
                f"elicitation option {index} role",
                required=True,
                maximum=40,
            )
            if role not in CHOICE_ROLES:
                raise OpsError(f"Invalid elicitation option role: {role}")
            if role in seen_roles:
                raise OpsError(f"Duplicate elicitation option role: {role}")
            seen_roles.add(role)
            normalized["role"] = role
        else:
            if "role" in option or "recommendation_key" in surface:
                raise OpsError(
                    "Neutral evidence intake cannot assign recommendation roles"
                )
            if _elicitation_action(label):
                raise OpsError(
                    "Neutral evidence intake cannot present an action-authorizing label"
                )
        normalized_options.append(normalized)

    if interaction_type == "decision-navigation":
        for role in ("recommended", "alternative"):
            if role not in seen_roles:
                raise OpsError(f"Decision menu requires the {role} role")
        if not ({"overlooked", "pause-or-deepen"} & seen_roles):
            raise OpsError(
                "Decision menu requires an overlooked or pause-or-deepen possibility"
            )

    return {
        "interaction_type": interaction_type,
        "question": question,
        "options": normalized_options,
        "authority_effect": "none",
    }


def interpret_elicitation_response(
    options: list[dict[str, Any]], response: str
) -> dict[str, Any]:
    """Interpret a single, compound, or ranked decision-menu response.

    This function does not execute work or write a choice receipt. It returns
    the exact ordered branch and action semantics an orchestration layer must
    honor when it performs those separate operations.
    """
    surface = validate_elicitation_surface(
        {
            "interaction_type": "decision-navigation",
            "question": "Interpret the presented decision menu",
            "options": options,
        }
    )
    raw_response = _bounded(
        response, "elicitation response", required=True, maximum=80
    )
    has_compound = "," in raw_response
    has_ranking = ">" in raw_response
    if has_compound and has_ranking:
        raise OpsError("Elicitation response cannot mix compound and ranking syntax")

    delimiter = ">" if has_ranking else "," if has_compound else None
    tokens = (
        [token.strip().upper() for token in raw_response.split(delimiter)]
        if delimiter
        else [raw_response.strip().upper()]
    )
    if any(not token for token in tokens):
        raise OpsError("Elicitation response contains an empty selection")
    if len(set(tokens)) != len(tokens):
        raise OpsError("Elicitation response contains duplicate selections")

    option_by_letter = {
        chr(ord("A") + index): option
        for index, option in enumerate(surface["options"])
    }
    unknown = [token for token in tokens if token not in option_by_letter]
    if unknown:
        raise OpsError(
            "Unknown elicitation selection: " + ", ".join(unknown)
        )
    if has_ranking and len(tokens) < 2:
        raise OpsError("A ranked elicitation response requires at least two options")

    branches = [
        _elicitation_branch(token, option_by_letter[token]) for token in tokens
    ]
    if has_compound and len(branches) < 2:
        raise OpsError("A compound elicitation response requires at least two options")
    if has_compound and any(
        branch["role"] == "pause-or-deepen" for branch in branches
    ):
        raise OpsError(
            "pause-or-deepen cannot be combined with another selected branch"
        )

    if has_ranking:
        return {
            "schema_version": 1,
            "mode": "ranked",
            "authority_effect": "none",
            "selected_branches": [],
            "preference_order": branches,
            "top_preference": branches[0],
            "receipt_count": 0,
            "execute_nothing": True,
            "next_step": "Use the top preference to shape read-only exploration or the next menu",
        }

    return {
        "schema_version": 1,
        "mode": "compound" if has_compound else "single",
        "authority_effect": "none",
        "selected_branches": branches,
        "preference_order": [],
        "receipt_count": len(branches),
        "shared_option_set_identity": len(branches) > 1,
        "execute_in_order": True,
        "stop_on_failure": True,
    }


def _elicitation_branch(letter: str, option: dict[str, str]) -> dict[str, Any]:
    action = _elicitation_action(option["label"])
    return {
        "letter": letter,
        "option_key": option["key"],
        "role": option["role"],
        "label": option["label"],
        "action_authorization": {
            "authorized": action is not None,
            "verb": action,
            "bounded_action": option["label"] if action else None,
        },
    }


def _elicitation_action(label: str) -> str | None:
    match = re.match(
        r"^(Execute|Commit|Push|Send)(?=$|[\s:—–-])",
        label.strip(),
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    return next(
        verb for verb in ELICITATION_ACTION_VERBS if verb.casefold() == match.group(1).casefold()
    )


def load_choice_packet(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    value = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise OpsError(f"Choice packet must be a YAML mapping: {source}")
    return _normalize_yaml_dates(value)


def validate_choice_selection_packet(
    packet: dict[str, Any], tenant: str
) -> dict[str, Any]:
    normalized = _validate_selection_packet(packet)
    _validate_selection_classification_scope(normalized, tenant)
    return {key: value for key, value in normalized.items() if key != "option_by_key"}


def validate_choice_event_packet(packet: dict[str, Any]) -> dict[str, Any]:
    event_type = _text(packet.get("event_type"))
    if event_type not in EVENT_TYPES:
        raise OpsError(f"Unsupported choice event type: {event_type}")
    payload = packet.get("payload")
    if not isinstance(payload, dict):
        raise OpsError("Choice event payload must be a mapping")
    normalized = dict(packet)
    normalized["payload"] = _validate_event_payload(event_type, payload)
    _privacy_safe(normalized["payload"], "choice event payload")
    return normalized


def record_choice_selection(
    connection: sqlite3.Connection,
    tenant: str,
    packet: dict[str, Any],
) -> MutationResult:
    normalized = _validate_selection_packet(packet)
    _validate_selection_classification_scope(normalized, tenant)
    tid = tenant_id(connection, tenant)
    _validate_actor(connection, tid, normalized["actor_id"])
    prompt_values = {
        "id": normalized["id"],
        "tenant_id": tid,
        "workspace_id": normalized["workspace_id"],
        "lane": normalized["lane"],
        "choice_kind": normalized["choice_kind"],
        "consequence_level": normalized["consequence_level"],
        "decision_summary": normalized["decision_summary"],
        "options_json": _canonical_json(normalized["options"]),
        "recommendation_key": normalized["recommendation_key"],
        "learning_refs_json": _canonical_json(normalized["learning_refs"]),
        "success_signal": normalized["success_signal"],
        "risk_signal": normalized["risk_signal"],
        "source_ref": normalized["source_ref"],
        "presented_at": normalized["presented_at"],
        "option_set_hash": _hash(normalized["options"]),
        "learning_context_hash": _hash(normalized["learning_context"]),
        "created_at": normalized["recorded_at"],
    }
    selection_payload = {
        "selected_option_key": normalized["selected_option_key"],
        "selected_option_role": normalized["option_by_key"][
            normalized["selected_option_key"]
        ]["role"],
        "review_after": normalized["review_after"],
        "authority_effect": "none",
    }
    event_id = str(
        uuid.uuid5(uuid.NAMESPACE_URL, f"anyang:choice:{normalized['id']}:selection")
    )
    event_values = {
        "id": event_id,
        "choice_id": normalized["id"],
        "tenant_id": tid,
        "event_key": "selection",
        "sequence": 1,
        "event_type": "branch_selected",
        "actor_id": normalized["actor_id"],
        "actor_label": normalized["selected_by"],
        "action_summary": f"Navigate into {normalized['selected_option_key']}",
        "occurred_at": normalized["selected_at"],
        "recorded_at": normalized["recorded_at"],
        "evidence_ref": normalized["evidence_ref"],
        "payload_json": _canonical_json(selection_payload),
        "prior_hash": "",
    }
    event_values["event_hash"] = _event_hash(event_values)

    existing = connection.execute(
        "SELECT * FROM choice_prompt WHERE id = ?", (normalized["id"],)
    ).fetchone()
    if existing:
        comparable = tuple(key for key in prompt_values if key != "created_at")
        if not all(existing[key] == prompt_values[key] for key in comparable):
            raise OpsError(f"Choice prompt conflicts with existing record: {normalized['id']}")
        event = connection.execute(
            "SELECT * FROM choice_event WHERE choice_id = ? AND event_key = 'selection'",
            (normalized["id"],),
        ).fetchone()
        if event and all(event[key] == value for key, value in event_values.items()):
            return MutationResult(
                "choice_selection_exists",
                normalized["id"],
                {"idempotent": True, "selected_option_key": normalized["selected_option_key"]},
            )
        raise OpsError(f"Choice selection conflicts with existing record: {normalized['id']}")

    try:
        connection.execute(
            """INSERT INTO choice_prompt(
                id, tenant_id, workspace_id, lane, choice_kind, consequence_level,
                decision_summary, options_json, recommendation_key, learning_refs_json,
                success_signal, risk_signal, source_ref, presented_at, option_set_hash,
                learning_context_hash, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            tuple(prompt_values.values()),
        )
        connection.execute(
            """INSERT INTO choice_event(
                id, choice_id, tenant_id, event_key, sequence, event_type,
                actor_id, actor_label, action_summary, occurred_at, recorded_at,
                evidence_ref, payload_json, prior_hash, event_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            tuple(event_values.values()),
        )
        connection.commit()
    except sqlite3.IntegrityError as exc:
        connection.rollback()
        raise OpsError(f"Choice selection is invalid: {exc}") from exc
    return MutationResult(
        "choice_branch_selected",
        normalized["id"],
        {
            "idempotent": False,
            "selected_option_key": normalized["selected_option_key"],
            "authority_effect": "none",
        },
    )


def record_choice_event(
    connection: sqlite3.Connection,
    choice_id: str,
    packet: dict[str, Any],
) -> MutationResult:
    prompt = _prompt(connection, choice_id)
    event_type = _text(packet.get("event_type"))
    if event_type not in EVENT_TYPES:
        raise OpsError(f"Unsupported choice event type: {event_type}")
    event_key = _bounded(packet.get("event_key"), "event_key", required=True, maximum=200)
    actor_label = _bounded(packet.get("recorded_by"), "recorded_by", required=True)
    actor_id = _nullable_bounded(packet.get("actor_id"), "actor_id", maximum=200)
    _validate_actor(connection, prompt["tenant_id"], actor_id)
    summary = _bounded(packet.get("action_summary"), "action_summary", required=True)
    evidence_ref = _nullable_bounded(packet.get("evidence_ref"), "evidence_ref") or ""
    occurred_at = _nullable_bounded(packet.get("occurred_at"), "occurred_at", maximum=100)
    recorded_at = _nullable_bounded(packet.get("recorded_at"), "recorded_at", maximum=100) or now_utc()
    payload = packet.get("payload")
    if not isinstance(payload, dict):
        raise OpsError("Choice event payload must be a mapping")
    payload = _validate_event_payload(event_type, payload)
    _privacy_safe(payload, "choice event payload")
    if event_type == "corrected" and payload.get("classification_correction"):
        _validate_new_classification_correction(connection, prompt, payload)
    payload_json = _canonical_json(payload)

    existing = connection.execute(
        "SELECT * FROM choice_event WHERE choice_id = ? AND event_key = ?",
        (choice_id, event_key),
    ).fetchone()
    semantic = {
        "event_type": event_type,
        "actor_id": actor_id,
        "actor_label": actor_label,
        "action_summary": summary,
        "occurred_at": occurred_at,
        "evidence_ref": evidence_ref,
        "payload_json": payload_json,
    }
    if existing:
        if all(existing[key] == value for key, value in semantic.items()):
            return MutationResult(
                "choice_event_exists", existing["id"], {"idempotent": True}
            )
        raise OpsError(f"Choice event key conflicts: {choice_id}/{event_key}")

    prior = connection.execute(
        """SELECT sequence, event_hash FROM choice_event
        WHERE choice_id = ? ORDER BY sequence DESC LIMIT 1""",
        (choice_id,),
    ).fetchone()
    sequence = int(prior["sequence"]) + 1 if prior else 1
    prior_hash = str(prior["event_hash"]) if prior else ""
    event_id = _nullable_bounded(packet.get("id"), "id", maximum=200) or str(uuid.uuid4())
    values = {
        "id": event_id,
        "choice_id": choice_id,
        "tenant_id": prompt["tenant_id"],
        "event_key": event_key,
        "sequence": sequence,
        **semantic,
        "recorded_at": recorded_at,
        "prior_hash": prior_hash,
    }
    values["event_hash"] = _event_hash(values)
    try:
        connection.execute(
            """INSERT INTO choice_event(
                id, choice_id, tenant_id, event_key, sequence, event_type,
                actor_id, actor_label, action_summary, occurred_at, evidence_ref,
                payload_json, recorded_at, prior_hash, event_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            tuple(values.values()),
        )
        connection.commit()
    except sqlite3.IntegrityError as exc:
        connection.rollback()
        raise OpsError(f"Choice event is invalid: {exc}") from exc
    return MutationResult(
        "choice_event_recorded",
        event_id,
        {"choice_id": choice_id, "event_type": event_type, "sequence": sequence},
    )


def verify_choice(connection: sqlite3.Connection, choice_id: str) -> dict[str, Any]:
    prompt = _prompt(connection, choice_id)
    events = connection.execute(
        "SELECT * FROM choice_event WHERE choice_id = ? ORDER BY sequence", (choice_id,)
    ).fetchall()
    semantic_issues = _semantic_choice_issues(connection, prompt, events)
    integrity_issues: list[dict[str, str]] = []
    prior_hash = ""
    for expected, event in enumerate(events, start=1):
        if event["sequence"] != expected:
            integrity_issues.append(
                {"code": "sequence-gap", "message": f"Expected event {expected}."}
            )
        if event["tenant_id"] != prompt["tenant_id"]:
            integrity_issues.append(
                {
                    "code": "tenant-mismatch",
                    "message": f"Event {event['id']} crosses tenant.",
                }
            )
        if event["prior_hash"] != prior_hash:
            integrity_issues.append(
                {
                    "code": "prior-hash-mismatch",
                    "message": f"Event {event['id']} has a broken link.",
                }
            )
        values = {key: event[key] for key in _event_hash_fields()}
        if _event_hash(values) != event["event_hash"]:
            integrity_issues.append(
                {
                    "code": "event-hash-mismatch",
                    "message": f"Event {event['id']} failed hashing.",
                }
            )
        prior_hash = event["event_hash"]
    issues = [*semantic_issues, *integrity_issues]
    return {
        "choice_id": choice_id,
        "verification_profile": "choice-semantic-v2",
        "integrity_ok": not integrity_issues,
        "semantics_ok": not semantic_issues,
        "ok": not issues,
        "event_count": len(events),
        "head_hash": prior_hash,
        "issues": issues,
    }


def assert_choice_scope(
    connection: sqlite3.Connection,
    choice_id: str,
    tenant: str,
    workspace_id: str,
    lane: str,
) -> None:
    try:
        tid = tenant_id(connection, tenant)
    except OpsError as exc:
        raise OpsError("Choice was not found in the requested scope.") from exc
    row = connection.execute(
        """SELECT 1 FROM choice_prompt
        WHERE id = ? AND tenant_id = ? AND workspace_id = ? AND lane = ?""",
        (choice_id, tid, workspace_id, lane),
    ).fetchone()
    if not row:
        raise OpsError("Choice was not found in the requested scope.")


def choice_projection(connection: sqlite3.Connection, choice_id: str) -> dict[str, Any]:
    prompt = _prompt(connection, choice_id)
    rows = connection.execute(
        "SELECT * FROM choice_event WHERE choice_id = ? ORDER BY sequence", (choice_id,)
    ).fetchall()
    events = [_event_dict(row) for row in rows]
    selected = next(
        (event for event in events if event["event_type"] == "branch_selected"), None
    )
    outcome = None
    state = "selected" if selected else "invalid"
    review_after = selected["payload"].get("review_after") if selected else None
    for event in events:
        if event["event_type"] == "outcome_recorded":
            outcome = event
            state = (
                "outcome_observed"
                if event["payload"].get("result") in TERMINAL_RESULTS
                else "outcome_pending"
            )
        elif event["event_type"] == "review_deferred":
            review_after = event["payload"]["review_after"]
            state = "review_deferred"
        elif event["event_type"] == "corrected":
            if isinstance(event["payload"].get("replacement_outcome"), dict):
                state = "corrected"
                outcome = {**event, "payload": event["payload"]["replacement_outcome"]}
            elif not event["payload"].get("classification_correction"):
                state = "corrected"
        elif event["event_type"] == "superseded":
            state = "superseded"
    verification = verify_choice(connection, choice_id)
    options = json.loads(prompt["options_json"])
    classifications = _derive_classifications(connection, prompt, list(rows))
    selected_key = (
        selected["payload"]["selected_option_key"] if selected else ""
    )
    original_classification = classifications["original"].get(
        selected_key,
        _project_option_classification({}),
    )
    effective_classification = classifications["effective"].get(
        selected_key,
        dict(original_classification),
    )
    comparability_key = effective_classification["comparability_key"]
    comparability_policy = (
        _comparability_policy(comparability_key)
        if comparability_key != "Missing"
        else None
    )
    exclusions: list[str] = []
    if effective_classification["pattern_key"] == "unclassified":
        exclusions.append("unclassified-option")
    if comparability_key == "Missing":
        exclusions.append("missing-comparability-policy")
    if classifications["issues"]:
        exclusions.append("invalid-classification")
    if not verification["ok"]:
        exclusions.append("choice-verification-failed")
    if not outcome or outcome["payload"].get("result") not in TERMINAL_RESULTS:
        exclusions.append("outcome-unresolved")
    elif not outcome.get("evidence_ref"):
        exclusions.append("outcome-evidence-missing")
    if state == "superseded":
        exclusions.append("choice-superseded")
    learning_eligibility = {
        "eligible": not exclusions,
        "exclusion_reasons": exclusions,
        "recommendation_effect": (
            comparability_policy["status"]
            if comparability_policy and not exclusions
            else "none"
        ),
    }
    return {
        "schema_version": 2,
        "choice": {
            key: prompt[key]
            for key in (
                "id",
                "tenant_id",
                "workspace_id",
                "lane",
                "choice_kind",
                "consequence_level",
                "decision_summary",
                "recommendation_key",
                "success_signal",
                "risk_signal",
                "source_ref",
                "presented_at",
                "created_at",
            )
        },
        "options": options,
        "learning_refs": json.loads(prompt["learning_refs_json"]),
        "selection": selected,
        "outcome": outcome,
        "current_state": state,
        "review_after": review_after,
        "original_classification": original_classification,
        "effective_classification": effective_classification,
        "classification_corrections": classifications["corrections"],
        "classification_verified": not classifications["issues"],
        "learning_eligibility": learning_eligibility,
        "comparability_policy": comparability_policy,
        "attention_flags": _attention_flags(prompt, state, outcome, verification),
        "events": events,
        "lineage": {
            "option_set_hash": prompt["option_set_hash"],
            "learning_context_hash": prompt["learning_context_hash"],
            "event_count": verification["event_count"],
            "head_hash": verification["head_hash"],
            "chain_verified": verification["ok"],
            "authority_effect": "none",
        },
    }


def choice_guardrails(
    connection: sqlite3.Connection,
    tenant: str,
    workspace_id: str,
    lane: str,
    choice_kind: str,
) -> list[dict[str, str]]:
    """Read current authority or membrane incidents without review-state inspection."""
    tid = tenant_id(connection, tenant)
    rows = connection.execute(
        """SELECT DISTINCT p.id
        FROM choice_prompt p
        JOIN choice_event e ON e.choice_id = p.id
        WHERE p.tenant_id = ? AND p.workspace_id = ? AND p.lane = ?
          AND p.choice_kind = ?
          AND e.event_type IN ('outcome_recorded', 'corrected')
        ORDER BY p.created_at, p.id""",
        (tid, workspace_id, lane, choice_kind),
    ).fetchall()
    guardrails: list[dict[str, str]] = []
    for row in rows:
        projection = choice_projection(connection, row["id"])
        outcome = projection["outcome"]
        if not outcome or outcome["payload"].get("result") not in TERMINAL_RESULTS:
            continue
        guardrail = _projection_guardrail(projection)
        if guardrail:
            guardrails.append(guardrail)
    return guardrails


def choice_context(
    connection: sqlite3.Connection,
    tenant: str,
    workspace_id: str,
    lane: str,
    choice_kind: str,
    as_of: str | None = None,
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    rows = connection.execute(
        """SELECT id FROM choice_prompt
        WHERE tenant_id = ? AND workspace_id = ? AND lane = ? AND choice_kind = ?
        ORDER BY created_at, id""",
        (tid, workspace_id, lane, choice_kind),
    ).fetchall()
    projections = [choice_projection(connection, row["id"]) for row in rows]
    resolved = [
        projection
        for projection in projections
        if projection["outcome"]
        and projection["outcome"]["payload"].get("result") in TERMINAL_RESULTS
    ]
    patterns: dict[str, dict[str, Any]] = {}
    cohort_buckets: dict[str, dict[str, Any]] = {}
    diversity_counts = {key: 0 for key in CHOICE_PATTERN_KEYS}
    unclassified_count = 0
    classified_count = 0
    guardrails: list[dict[str, str]] = []
    learning_refs: set[str] = set()
    for projection in projections:
        learning_refs.update(projection["learning_refs"])
        effective_classifications = _projection_effective_classifications(
            projection
        )
        for classification in effective_classifications.values():
            pattern_key = classification["pattern_key"]
            if pattern_key == "unclassified":
                unclassified_count += 1
            else:
                classified_count += 1
                diversity_counts[pattern_key] += 1
    for projection in resolved:
        selected_key = projection["selection"]["payload"]["selected_option_key"]
        result = projection["outcome"]["payload"]["result"]
        bucket = patterns.setdefault(
            selected_key,
            {
                "option_key": selected_key,
                "resolved": 0,
                "successful": 0,
                "mixed": 0,
                "unsuccessful": 0,
                "no_action": 0,
                "not_observable": 0,
                "evidence_tier": "descriptive-only",
                "recommendation_effect": "none",
            },
        )
        bucket["resolved"] += 1
        bucket[result] += 1
        eligibility = projection["learning_eligibility"]
        if eligibility["eligible"]:
            comparability_key = projection["effective_classification"][
                "comparability_key"
            ]
            policy = projection["comparability_policy"]
            cohort = cohort_buckets.setdefault(
                comparability_key,
                {
                    "comparability_key": comparability_key,
                    "policy_status": policy["status"],
                    "resolved": 0,
                    "successful": 0,
                    "mixed": 0,
                    "unsuccessful": 0,
                    "no_action": 0,
                    "not_observable": 0,
                    "choice_ids": [],
                    "evidence_tier": "thin",
                    "recommendation_effect": "none",
                },
            )
            cohort["resolved"] += 1
            cohort[result] += 1
            cohort["choice_ids"].append(projection["choice"]["id"])
        guardrail = _projection_guardrail(projection)
        if guardrail:
            guardrails.append(guardrail)
    pattern_rows = []
    for key in sorted(patterns):
        bucket = patterns[key]
        pattern_rows.append(bucket)
    comparability_cohorts = []
    diagnostic_favored: list[str] = []
    diagnostic_demoted: list[str] = []
    active_favored: list[str] = []
    active_demoted: list[str] = []
    for key in sorted(cohort_buckets):
        cohort = cohort_buckets[key]
        policy = _comparability_policy(key)
        minimum_resolved = int(policy["minimum_resolved"])
        minimum_consistent = int(policy["minimum_consistent"])
        direction = ""
        if cohort["resolved"] >= minimum_resolved:
            if (
                cohort["successful"] >= minimum_consistent
                and cohort["unsuccessful"] == 0
            ):
                direction = "favored"
            elif (
                cohort["unsuccessful"] >= minimum_consistent
                and cohort["successful"] == 0
            ):
                direction = "demoted"
        if direction:
            cohort["evidence_tier"] = "pattern"
            cohort["diagnostic_direction"] = direction
            if direction == "favored":
                diagnostic_favored.append(key)
            else:
                diagnostic_demoted.append(key)
            if policy["status"] == "active":
                cohort["recommendation_effect"] = direction
                if direction == "favored":
                    active_favored.append(key)
                else:
                    active_demoted.append(key)
        comparability_cohorts.append(cohort)
    policy = _choice_guidance_policy(
        tenant,
        workspace_id,
        lane,
        as_of or now_utc(),
    )
    if policy and policy["ordering_frozen"]:
        active_favored = []
        active_demoted = []
        for cohort in comparability_cohorts:
            cohort["recommendation_effect"] = "none"
    due_review = choice_review(connection, tenant, workspace_id, as_of)
    rationale = _guidance_rationale(
        len(resolved), guardrails, diagnostic_favored, diagnostic_demoted
    )
    if policy and policy["ordering_frozen"] and not guardrails:
        rationale = (
            f"Outcome patterns are diagnostic only under {policy['id']}; "
            "recommendation ordering is frozen pending explicit disposition."
        )
    return {
        "schema_version": 2,
        "tenant": tenant,
        "workspace_id": workspace_id,
        "lane": lane,
        "choice_kind": choice_kind,
        "as_of": as_of or now_utc(),
        "resolved_outcome_count": len(resolved),
        "outcome_patterns": pattern_rows,
        "diversity_diagnostics": {
            "classified_option_count": classified_count,
            "unclassified_option_count": unclassified_count,
            "pattern_counts": diversity_counts,
            "selection_frequency_used": False,
            "recommendation_effect": "none",
        },
        "comparability_cohorts": comparability_cohorts,
        "guardrails": guardrails,
        "learning_refs": sorted(learning_refs),
        "guidance_policy": policy,
        "recommendation_guidance": {
            "favored_option_keys": [],
            "demoted_option_keys": [],
            "option_key_guidance_deprecated": True,
            "favored_comparability_keys": active_favored,
            "demoted_comparability_keys": active_demoted,
            "diagnostic_favored_comparability_keys": diagnostic_favored,
            "diagnostic_demoted_comparability_keys": diagnostic_demoted,
            "ordering_frozen": bool(policy and policy["ordering_frozen"]),
            "selection_frequency_used": False,
            "option_key_learning_used": False,
            "preserve_overlooked_possibility": True,
            "rationale": rationale,
        },
        "due_outcome_review": due_review["choices"][:1],
        "ledger_fallback": False,
    }


def choice_review(
    connection: sqlite3.Connection,
    tenant: str,
    workspace_id: str,
    as_of: str | None = None,
) -> dict[str, Any]:
    tid = tenant_id(connection, tenant)
    reference = as_of or now_utc()
    rows = connection.execute(
        """SELECT id FROM choice_prompt
        WHERE tenant_id = ? AND workspace_id = ? ORDER BY created_at, id""",
        (tid, workspace_id),
    ).fetchall()
    due: list[dict[str, Any]] = []
    resolved: list[dict[str, Any]] = []
    for row in rows:
        projection = choice_projection(connection, row["id"])
        if projection["current_state"] == "superseded":
            continue
        outcome = projection["outcome"]
        if outcome and outcome["payload"].get("result") in TERMINAL_RESULTS:
            resolved.append(projection)
            continue
        review_after = projection["review_after"]
        if review_after and _timestamp(review_after) > _timestamp(reference):
            continue
        due.append(
            {
                "choice_id": projection["choice"]["id"],
                "decision_summary": projection["choice"]["decision_summary"],
                "consequence_level": projection["choice"]["consequence_level"],
                "selected_option_key": projection["selection"]["payload"][
                    "selected_option_key"
                ],
                "selected_option_label": _selected_label(projection),
                "review_after": review_after,
                "current_state": projection["current_state"],
            }
        )
    rank = {"authority-sensitive": 0, "consequential": 1, "ordinary": 2}
    due.sort(
        key=lambda item: (
            rank[item["consequence_level"]],
            item["review_after"] or "",
            item["choice_id"],
        )
    )
    return {
        "schema_version": 1,
        "tenant": tenant,
        "workspace_id": workspace_id,
        "as_of": reference,
        "due_count": len(due),
        "choices": due,
        "resolved_count": len(resolved),
        "reflection_sample_ready": len(resolved) >= 5,
        "five_selection_review": _five_selection_scorecard(resolved),
        "coffee_limit": 1,
        "human_authority": "Outcome review informs future navigation and grants no action authority.",
    }


def render_choice_markdown(data: dict[str, Any]) -> str:
    lines = [
        f"# {data['choice']['decision_summary']}",
        "",
        f"Choice: `{data['choice']['id']}`",
        f"State: `{data['current_state']}`",
        f"Lane: `{data['choice']['lane']}`",
        "",
        "## Possibilities",
        "",
    ]
    selected_key = (
        data["selection"]["payload"]["selected_option_key"] if data["selection"] else ""
    )
    for option in data["options"]:
        marker = " — selected" if option["key"] == selected_key else ""
        lines.append(
            f"- **{option['label']}** (`{option['role']}`){marker}: {option['tradeoff']}"
        )
    classification = data["effective_classification"]
    eligibility = data["learning_eligibility"]
    lines.extend(
        [
            "",
            "## Continuity Classification",
            "",
            f"- Pattern: `{classification['pattern_key']}`",
            f"- Action boundary: `{classification['action_boundary']}`",
            f"- Comparability key: `{classification['comparability_key']}`",
            f"- Classification verified: {data['classification_verified']}",
            f"- Learning eligible: {eligibility['eligible']}",
        ]
    )
    if eligibility["exclusion_reasons"]:
        lines.append(
            "- Eligibility exclusions: "
            + ", ".join(
                f"`{item}`" for item in eligibility["exclusion_reasons"]
            )
        )
    lines.extend(["", "## Outcome", ""])
    if data["outcome"]:
        payload = data["outcome"]["payload"]
        lines.append(f"- Result: `{payload.get('result', 'Missing')}`")
        lines.append(f"- Cognitive load: `{payload.get('cognitive_load', 'Missing')}`")
        lines.append(f"- Momentum: `{payload.get('momentum', 'Missing')}`")
        lines.append(f"- Discovery value: `{payload.get('discovery_value', 'Missing')}`")
    else:
        lines.append("- Missing")
    lines.extend(
        [
            "",
            "## Lineage",
            "",
            f"- Chain verified: {data['lineage']['chain_verified']}",
            f"- Head hash: `{data['lineage']['head_hash']}`",
            "- Authority effect: `none`",
            "",
        ]
    )
    return "\n".join(lines)


def render_choice_context_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Choice Learning Context",
        "",
        f"Lane: `{data['lane']}`",
        f"Kind: `{data['choice_kind']}`",
        f"Resolved outcomes: {data['resolved_outcome_count']}",
        "",
        f"Recommendation rationale: {data['recommendation_guidance']['rationale']}",
        "",
        "## Outcome Patterns",
        "",
    ]
    if not data["outcome_patterns"]:
        lines.append("- No resolved option-key outcomes.")
    for pattern in data["outcome_patterns"]:
        lines.append(
            f"- `{pattern['option_key']}`: descriptive only across "
            f"{pattern['resolved']} outcome(s)."
        )
    diversity = data["diversity_diagnostics"]
    lines.extend(
        [
            "",
            "## Diversity Diagnostics",
            "",
            (
                f"- Classified options: {diversity['classified_option_count']}; "
                f"unclassified options: {diversity['unclassified_option_count']}."
            ),
        ]
    )
    for key, count in diversity["pattern_counts"].items():
        if count:
            lines.append(f"- `{key}`: {count}")
    lines.extend(["", "## Comparability Cohorts", ""])
    if not data["comparability_cohorts"]:
        lines.append("- No eligible explicit comparability cohorts.")
    for cohort in data["comparability_cohorts"]:
        lines.append(
            f"- `{cohort['comparability_key']}`: {cohort['evidence_tier']} "
            f"across {cohort['resolved']} outcome(s); recommendation effect "
            f"`{cohort['recommendation_effect']}`."
        )
    lines.extend(["", "## Guardrails", ""])
    if not data["guardrails"]:
        lines.append("- No outcome-derived authority or membrane guardrails.")
    for guardrail in data["guardrails"]:
        lines.append(f"- `{guardrail['option_key']}`: {guardrail['reason']}")
    lines.append("")
    return "\n".join(lines)


def render_choice_review_markdown(data: dict[str, Any]) -> str:
    scorecard = data["five_selection_review"]
    lines = [
        "# Choice Outcome Review",
        "",
        f"Due outcomes: {data['due_count']}",
        f"Resolved outcomes: {data['resolved_count']}",
        "",
    ]
    for item in data["choices"]:
        lines.append(
            f"- **{item['decision_summary']}** → {item['selected_option_label']} "
            f"(`{item['choice_id']}`)"
        )
    if not data["choices"]:
        lines.append("- No outcome review is due.")
    lines.extend(
        [
            "",
            "## Five-Selection Navigation Review",
            "",
            f"Cohort: {scorecard['cohort_size']} / {scorecard['required_size']} resolved selections",
        ]
    )
    if not scorecard["sample_ready"]:
        lines.append(
            f"- Pending: {scorecard['remaining']} more resolved selection(s) required."
        )
    else:
        metrics = scorecard["primary_metrics"]
        lines.extend(
            [
                (
                    f"- Lower cognitive load: "
                    f"{metrics['lower_cognitive_load']['favorable']} / "
                    f"{metrics['lower_cognitive_load']['observed']} observed"
                ),
                (
                    f"- Advanced momentum: "
                    f"{metrics['advanced_momentum']['favorable']} / "
                    f"{metrics['advanced_momentum']['observed']} observed"
                ),
                (
                    f"- New useful paths: "
                    f"{metrics['new_useful_path']['favorable']} / "
                    f"{metrics['new_useful_path']['observed']} observed"
                ),
                (
                    "- Authority or membrane incidents: "
                    f"{scorecard['guardrails']['authority_or_membrane_incidents']}"
                ),
                "- Selection frequency used: no",
                f"- Assessment: `{scorecard['assessment']}`",
                f"- Rationale: {scorecard['rationale']}",
            ]
        )
    lines.extend(["", f"Authority boundary: {data['human_authority']}", ""])
    return "\n".join(lines)


def _five_selection_scorecard(
    resolved: list[dict[str, Any]],
) -> dict[str, Any]:
    required_size = 5
    cohort = resolved[:required_size]
    base = {
        "cohort_rule": "earliest-five-resolved-non-superseded",
        "required_size": required_size,
        "cohort_size": len(cohort),
        "remaining": max(0, required_size - len(cohort)),
        "sample_ready": len(cohort) == required_size,
        "choice_ids": [item["choice"]["id"] for item in cohort],
        "selection_frequency_used": False,
        "recommendation_effect": (
            "Descriptive pilot evidence only; comparable-outcome thresholds remain controlling."
        ),
    }
    if len(cohort) < required_size:
        return {
            **base,
            "primary_metrics": {},
            "supporting_evidence": {},
            "guardrails": {
                "authority_or_membrane_incidents": 0,
                "incident_choice_ids": [],
                "selection_frequency_used": False,
            },
            "assessment": "pending",
            "rationale": "Five resolved, non-superseded selections are required.",
        }

    payloads = [item["outcome"]["payload"] for item in cohort]
    cognitive = _pilot_metric(
        payloads,
        field="cognitive_load",
        favorable="lower",
        target=3,
    )
    momentum = _pilot_metric(
        payloads,
        field="momentum",
        favorable="advanced",
        target=3,
    )
    discovery = _pilot_metric(
        payloads,
        field="discovery_value",
        favorable="new-useful-path",
        target=1,
    )
    primary = {
        "lower_cognitive_load": cognitive,
        "advanced_momentum": momentum,
        "new_useful_path": discovery,
    }
    incidents = [
        item["choice"]["id"]
        for item in cohort
        if item["outcome"]["payload"].get("authority_issue")
        or item["outcome"]["payload"].get("membrane_issue")
    ]
    negative_choices = [
        item["choice"]["id"]
        for item in cohort
        if item["outcome"]["payload"].get("cognitive_load") == "higher"
        or item["outcome"]["payload"].get("momentum") == "stalled"
        or item["outcome"]["payload"].get("discovery_value") == "not-useful"
    ]
    result_counts = {result: 0 for result in OUTCOME_RESULTS}
    for payload in payloads:
        result_counts[payload["result"]] += 1
    rework_values = [
        float(payload["rework_minutes"])
        for payload in payloads
        if payload.get("rework_minutes") is not None
    ]
    observed_dimensions = [metric["observed"] for metric in primary.values()]
    positive_signals = sum(metric["signal_met"] for metric in primary.values())

    if incidents:
        assessment = "hold"
        rationale = "An authority or membrane incident overrides positive outcome signals."
    elif any(observed < 3 for observed in observed_dimensions):
        assessment = "extend-to-ten"
        rationale = "At least one primary dimension has fewer than three observations."
    elif len(negative_choices) >= 2:
        assessment = "adjust"
        rationale = "At least two selections recorded higher load, stalled momentum, or not-useful discovery."
    elif positive_signals >= 2:
        assessment = "continue"
        rationale = "At least two primary measures met their pilot signal with no guardrail incident."
    else:
        assessment = "adjust"
        rationale = "Observable evidence did not meet the two-measure continuation threshold."

    return {
        **base,
        "primary_metrics": primary,
        "supporting_evidence": {
            "result_counts": result_counts,
            "negative_experience_count": len(negative_choices),
            "negative_experience_choice_ids": negative_choices,
            "rework_minutes": {
                "observed": len(rework_values),
                "total": round(sum(rework_values), 2),
                "median": round(float(median(rework_values)), 2)
                if rework_values
                else None,
            },
        },
        "guardrails": {
            "authority_or_membrane_incidents": len(incidents),
            "incident_choice_ids": incidents,
            "selection_frequency_used": False,
        },
        "assessment": assessment,
        "rationale": rationale,
    }


def _pilot_metric(
    payloads: list[dict[str, Any]],
    *,
    field: str,
    favorable: str,
    target: int,
) -> dict[str, Any]:
    observed = [payload[field] for payload in payloads if payload[field] != "Missing"]
    favorable_count = sum(value == favorable for value in observed)
    return {
        "favorable_value": favorable,
        "favorable": favorable_count,
        "observed": len(observed),
        "rate_percent": (
            round(favorable_count * 100 / len(observed), 1) if observed else None
        ),
        "pilot_target": target,
        "signal_met": favorable_count >= target,
    }


def _validate_selection_packet(packet: dict[str, Any]) -> dict[str, Any]:
    required = (
        "id",
        "workspace_id",
        "lane",
        "choice_kind",
        "consequence_level",
        "decision_summary",
        "options",
        "recommendation_key",
        "selected_option_key",
        "success_signal",
        "risk_signal",
        "selected_by",
    )
    missing = [name for name in required if name not in packet or packet[name] is None]
    if missing:
        raise OpsError(f"Choice selection is missing required fields: {', '.join(missing)}")
    consequence = _text(packet["consequence_level"])
    if consequence not in CONSEQUENCE_LEVELS:
        raise OpsError(f"Invalid consequence_level: {consequence}")
    options = packet["options"]
    if not isinstance(options, list) or not 3 <= len(options) <= 4:
        raise OpsError("Choice selection requires 3-4 possibilities")
    normalized_options = []
    seen_keys: set[str] = set()
    seen_roles: set[str] = set()
    for index, option in enumerate(options, start=1):
        if not isinstance(option, dict):
            raise OpsError(f"Choice option {index} must be a mapping")
        normalized = {
            "key": _bounded(option.get("key"), f"option {index} key", required=True, maximum=120),
            "role": _bounded(option.get("role"), f"option {index} role", required=True, maximum=40),
            "label": _bounded(option.get("label"), f"option {index} label", required=True),
            "tradeoff": _bounded(option.get("tradeoff"), f"option {index} tradeoff", required=True),
            "expected_outcome": _bounded(
                option.get("expected_outcome"), f"option {index} expected_outcome", required=True
            ),
            "risk": _bounded(option.get("risk"), f"option {index} risk", required=True),
            "learning_refs": _string_list(
                option.get("learning_refs", []), f"option {index} learning_refs"
            ),
        }
        supplied_classification = {
            field for field in CLASSIFICATION_FIELDS if field in option
        }
        if supplied_classification:
            missing_classification = [
                field
                for field in (
                    "classification_version",
                    "pattern_key",
                    "action_boundary",
                )
                if field not in option
            ]
            if missing_classification:
                raise OpsError(
                    f"Choice option {index} classification is missing required fields: "
                    + ", ".join(missing_classification)
                )
            classification_version = _bounded(
                option.get("classification_version"),
                f"option {index} classification_version",
                required=True,
                maximum=80,
            )
            if classification_version != CHOICE_CLASSIFICATION_VERSION:
                raise OpsError(
                    f"Invalid option {index} classification_version: "
                    f"{classification_version}"
                )
            pattern_key = _bounded(
                option.get("pattern_key"),
                f"option {index} pattern_key",
                required=True,
                maximum=80,
            )
            if pattern_key not in CHOICE_PATTERN_KEYS:
                raise OpsError(f"Invalid option {index} pattern_key: {pattern_key}")
            action_boundary = _bounded(
                option.get("action_boundary"),
                f"option {index} action_boundary",
                required=True,
                maximum=80,
            )
            if action_boundary not in CHOICE_ACTION_BOUNDARIES:
                raise OpsError(
                    f"Invalid option {index} action_boundary: {action_boundary}"
                )
            normalized.update(
                {
                    "classification_version": classification_version,
                    "pattern_key": pattern_key,
                    "action_boundary": action_boundary,
                }
            )
            if "comparability_key" in option:
                comparability_key = _bounded(
                    option.get("comparability_key"),
                    f"option {index} comparability_key",
                    required=True,
                    maximum=120,
                )
                normalized["comparability_key"] = comparability_key
        if normalized["key"] in seen_keys:
            raise OpsError(f"Duplicate choice option key: {normalized['key']}")
        if normalized["role"] not in CHOICE_ROLES:
            raise OpsError(f"Invalid choice option role: {normalized['role']}")
        if normalized["role"] in seen_roles:
            raise OpsError(f"Duplicate choice option role: {normalized['role']}")
        seen_keys.add(normalized["key"])
        seen_roles.add(normalized["role"])
        normalized_options.append(normalized)
    for required_role in ("recommended", "alternative"):
        if required_role not in seen_roles:
            raise OpsError(f"Choice options require the {required_role} role")
    if not ({"overlooked", "pause-or-deepen"} & seen_roles):
        raise OpsError(
            "Choice options require an overlooked or pause-or-deepen possibility"
        )
    recommendation_key = _text(packet["recommendation_key"])
    selected_key = _text(packet["selected_option_key"])
    option_by_key = {option["key"]: option for option in normalized_options}
    if recommendation_key not in option_by_key:
        raise OpsError("recommendation_key must name a presented option")
    if option_by_key[recommendation_key]["role"] != "recommended":
        raise OpsError("recommendation_key must bind the recommended option")
    if selected_key not in option_by_key:
        raise OpsError("selected_option_key must name a presented option")
    learning_refs = _string_list(packet.get("learning_refs", []), "learning_refs")
    normalized = {
        "id": _bounded(packet["id"], "id", required=True, maximum=200),
        "workspace_id": _bounded(packet["workspace_id"], "workspace_id", required=True),
        "lane": _bounded(packet["lane"], "lane", required=True),
        "choice_kind": _bounded(packet["choice_kind"], "choice_kind", required=True),
        "consequence_level": consequence,
        "decision_summary": _bounded(packet["decision_summary"], "decision_summary", required=True),
        "options": normalized_options,
        "recommendation_key": recommendation_key,
        "selected_option_key": selected_key,
        "learning_refs": learning_refs,
        "learning_context": packet.get("learning_context", {"learning_refs": learning_refs}),
        "success_signal": _bounded(packet["success_signal"], "success_signal", required=True),
        "risk_signal": _bounded(packet["risk_signal"], "risk_signal", required=True),
        "source_ref": _nullable_bounded(packet.get("source_ref"), "source_ref") or "",
        "presented_at": _nullable_bounded(packet.get("presented_at"), "presented_at", maximum=100),
        "selected_at": _nullable_bounded(packet.get("selected_at"), "selected_at", maximum=100)
        or now_utc(),
        "review_after": _nullable_bounded(packet.get("review_after"), "review_after", maximum=100)
        or now_utc(),
        "selected_by": _bounded(packet["selected_by"], "selected_by", required=True),
        "actor_id": _nullable_bounded(packet.get("actor_id"), "actor_id", maximum=200),
        "evidence_ref": _nullable_bounded(packet.get("evidence_ref"), "evidence_ref") or "",
        "recorded_at": _nullable_bounded(packet.get("recorded_at"), "recorded_at", maximum=100)
        or now_utc(),
        "option_by_key": option_by_key,
    }
    _privacy_safe(
        {key: value for key, value in normalized.items() if key != "option_by_key"},
        "choice selection",
    )
    for timestamp_name in (
        "presented_at",
        "selected_at",
        "review_after",
        "recorded_at",
    ):
        if normalized[timestamp_name]:
            _timestamp(normalized[timestamp_name])
    if len(_canonical_json(normalized_options)) > MAX_JSON:
        raise OpsError("Choice option set is too large")
    return normalized


def _validate_selection_classification_scope(
    normalized: dict[str, Any], tenant: str
) -> None:
    for option in normalized["options"]:
        key = option.get("comparability_key")
        if not key or key == "Missing":
            continue
        _validate_comparability_policy(
            key,
            tenant=tenant,
            workspace_id=normalized["workspace_id"],
            lane=normalized["lane"],
            choice_kind=normalized["choice_kind"],
            consequence_level=normalized["consequence_level"],
            pattern_key=option.get("pattern_key", "unclassified"),
            action_boundary=option.get("action_boundary", "unclassified"),
        )


def _comparability_policy(key: str) -> dict[str, Any] | None:
    return next(
        (policy for policy in CHOICE_COMPARABILITY_POLICIES if policy["id"] == key),
        None,
    )


def _validate_comparability_policy(
    key: str,
    *,
    tenant: str,
    workspace_id: str,
    lane: str,
    choice_kind: str,
    consequence_level: str,
    pattern_key: str,
    action_boundary: str,
) -> dict[str, Any]:
    policy = _comparability_policy(key)
    if not policy:
        raise OpsError(f"Unknown choice comparability policy: {key}")
    if policy["status"] == "disabled":
        raise OpsError(f"Choice comparability policy is disabled: {key}")
    expected = {
        "tenant": tenant,
        "workspace_id": workspace_id,
        "lane": lane,
        "choice_kind": choice_kind,
        "pattern_key": pattern_key,
        "action_boundary": action_boundary,
    }
    mismatched = [
        field for field, value in expected.items() if policy[field] != value
    ]
    if consequence_level not in policy["consequence_levels"]:
        mismatched.append("consequence_level")
    if mismatched:
        raise OpsError(
            f"Choice comparability policy scope mismatch for {key}: "
            + ", ".join(sorted(set(mismatched)))
        )
    return policy


def _validate_event_payload(event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    value = dict(payload)
    if event_type == "outcome_recorded":
        result = _text(value.get("result"))
        if result not in OUTCOME_RESULTS:
            raise OpsError(f"Invalid choice outcome result: {result}")
        value["result"] = result
        value["cognitive_load"] = _enum_or_missing(
            value.get("cognitive_load"), COGNITIVE_LOAD, "cognitive_load"
        )
        value["momentum"] = _enum_or_missing(value.get("momentum"), MOMENTUM, "momentum")
        value["discovery_value"] = _enum_or_missing(
            value.get("discovery_value"), DISCOVERY_VALUE, "discovery_value"
        )
        value["observation"] = _bounded(
            value.get("observation", "Missing"), "observation", required=True
        )
        rework = value.get("rework_minutes")
        if rework is not None:
            rework = float(rework)
            if rework < 0:
                raise OpsError("rework_minutes must be non-negative")
        value["rework_minutes"] = rework
        value["authority_issue"] = bool(value.get("authority_issue", False))
        value["membrane_issue"] = bool(value.get("membrane_issue", False))
    elif event_type == "review_deferred":
        value = {
            "review_after": _bounded(
                value.get("review_after"), "review_after", required=True, maximum=100
            ),
            "reason": _bounded(value.get("reason"), "reason", required=True),
        }
        _timestamp(value["review_after"])
    elif event_type == "corrected":
        value["reason"] = _bounded(value.get("reason"), "reason", required=True)
        replacement = value.get("replacement_outcome")
        correction = value.get("classification_correction")
        if replacement is not None and correction is not None:
            raise OpsError(
                "A corrected event cannot replace an outcome and classification together"
            )
        if replacement is not None:
            if not isinstance(replacement, dict):
                raise OpsError("replacement_outcome must be a mapping")
            value["replacement_outcome"] = _validate_event_payload(
                "outcome_recorded", replacement
            )
        if correction is not None:
            if not isinstance(correction, dict):
                raise OpsError("classification_correction must be a mapping")
            field = _text(correction.get("field"))
            if field not in {
                "pattern_key",
                "action_boundary",
                "comparability_key",
            }:
                raise OpsError(f"Invalid classification correction field: {field}")
            prior_value = _bounded(
                correction.get("prior_value"),
                "classification correction prior_value",
                required=True,
                maximum=120,
            )
            replacement_value = _bounded(
                correction.get("replacement_value"),
                "classification correction replacement_value",
                required=True,
                maximum=120,
            )
            if field == "pattern_key" and replacement_value not in CHOICE_PATTERN_KEYS:
                raise OpsError(
                    f"Invalid classification correction pattern_key: {replacement_value}"
                )
            if (
                field == "action_boundary"
                and replacement_value not in CHOICE_ACTION_BOUNDARIES
            ):
                raise OpsError(
                    "Invalid classification correction action_boundary: "
                    f"{replacement_value}"
                )
            value["classification_correction"] = {
                "option_key": _bounded(
                    correction.get("option_key"),
                    "classification correction option_key",
                    required=True,
                    maximum=120,
                ),
                "field": field,
                "prior_value": prior_value,
                "replacement_value": replacement_value,
                "policy_ref": _bounded(
                    correction.get("policy_ref"),
                    "classification correction policy_ref",
                    required=True,
                    maximum=200,
                ),
            }
            policy_issue = _comparability_correction_policy_issue(
                value["classification_correction"]
            )
            if policy_issue:
                raise OpsError(policy_issue)
    elif event_type == "superseded":
        value = {
            "reason": _bounded(value.get("reason"), "reason", required=True),
            "superseding_choice_id": _bounded(
                value.get("superseding_choice_id"),
                "superseding_choice_id",
                required=True,
                maximum=200,
            ),
        }
    return value


def _tenant_slug(connection: sqlite3.Connection, tenant_identifier: str) -> str:
    row = connection.execute(
        "SELECT slug FROM tenant WHERE id = ?", (tenant_identifier,)
    ).fetchone()
    if not row:
        raise OpsError("Choice tenant is unavailable")
    return str(row["slug"])


def _project_option_classification(option: dict[str, Any]) -> dict[str, str]:
    return {
        "classification_version": option.get(
            "classification_version", "legacy-unclassified"
        ),
        "pattern_key": option.get("pattern_key", "unclassified"),
        "action_boundary": option.get("action_boundary", "unclassified"),
        "comparability_key": option.get("comparability_key", "Missing"),
    }


def _projection_effective_classifications(
    projection: dict[str, Any],
) -> dict[str, dict[str, str]]:
    effective = {
        option["key"]: _project_option_classification(option)
        for option in projection["options"]
    }
    for correction in projection["classification_corrections"]:
        if not correction.get("valid"):
            continue
        option = effective.get(correction["option_key"])
        if option is not None:
            option[correction["field"]] = correction["replacement_value"]
    return effective


def _comparability_correction_policy_issue(
    correction: dict[str, Any],
) -> str | None:
    if correction.get("field") != "comparability_key":
        return None
    prior_value = str(correction.get("prior_value", ""))
    replacement_value = str(correction.get("replacement_value", ""))
    policy_ref = str(correction.get("policy_ref", ""))
    if prior_value == replacement_value:
        return "Comparability correction must change the effective value"
    expected_ref = (
        replacement_value if replacement_value != "Missing" else prior_value
    )
    policy = _comparability_policy(policy_ref)
    if not policy:
        return f"Unknown choice comparability policy: {policy_ref}"
    if policy["status"] == "disabled":
        return f"Choice comparability policy is disabled: {policy_ref}"
    if policy_ref != expected_ref:
        expected_source = (
            "replacement_value"
            if replacement_value != "Missing"
            else "prior_value when removing a policy"
        )
        return (
            "Comparability correction policy_ref must match "
            f"{expected_source}"
        )
    return None


def _classification_policy_issue(
    prompt: sqlite3.Row,
    tenant: str,
    classification: dict[str, str],
) -> str | None:
    key = classification["comparability_key"]
    if key == "Missing":
        return None
    try:
        _validate_comparability_policy(
            key,
            tenant=tenant,
            workspace_id=str(prompt["workspace_id"]),
            lane=str(prompt["lane"]),
            choice_kind=str(prompt["choice_kind"]),
            consequence_level=str(prompt["consequence_level"]),
            pattern_key=classification["pattern_key"],
            action_boundary=classification["action_boundary"],
        )
    except OpsError as exc:
        return str(exc)
    return None


def _derive_classifications(
    connection: sqlite3.Connection,
    prompt: sqlite3.Row,
    events: list[sqlite3.Row] | list[dict[str, Any]],
) -> dict[str, Any]:
    options = json.loads(prompt["options_json"])
    original = {
        option["key"]: _project_option_classification(option)
        for option in options
        if isinstance(option, dict) and isinstance(option.get("key"), str)
    }
    effective = {key: dict(value) for key, value in original.items()}
    corrections: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    tenant = _tenant_slug(connection, str(prompt["tenant_id"]))
    for event in events:
        event_type = event["event_type"]
        if event_type != "corrected":
            continue
        payload = (
            event["payload"]
            if isinstance(event, dict) and "payload" in event
            else json.loads(event["payload_json"])
        )
        correction = payload.get("classification_correction")
        if not isinstance(correction, dict):
            continue
        option_key = str(correction.get("option_key", ""))
        field = str(correction.get("field", ""))
        current = effective.get(option_key)
        issue: str | None = None
        if current is None:
            issue = f"Classification correction names an unknown option: {option_key}"
        elif current.get(field) != correction.get("prior_value"):
            issue = (
                f"Classification correction prior_value is stale for "
                f"{option_key}/{field}"
            )
        else:
            candidate = dict(current)
            candidate[field] = str(correction.get("replacement_value"))
            correction_policy_issue = _comparability_correction_policy_issue(
                correction
            )
            if correction_policy_issue:
                issue = correction_policy_issue
            else:
                policy_issue = _classification_policy_issue(prompt, tenant, candidate)
                if policy_issue:
                    issue = policy_issue
                else:
                    effective[option_key] = candidate
        recorded = {
            "event_key": event["event_key"],
            "sequence": event["sequence"],
            **correction,
            "valid": issue is None,
        }
        if issue:
            recorded["issue"] = issue
            issues.append(
                {
                    "code": "classification-correction-invalid",
                    "message": issue,
                }
            )
        corrections.append(recorded)
    for option_key, classification in effective.items():
        issue = _classification_policy_issue(prompt, tenant, classification)
        if issue:
            issues.append(
                {
                    "code": "classification-policy-invalid",
                    "message": f"{option_key}: {issue}",
                }
            )
    return {
        "original": original,
        "effective": effective,
        "corrections": corrections,
        "issues": issues,
    }


def _validate_new_classification_correction(
    connection: sqlite3.Connection,
    prompt: sqlite3.Row,
    payload: dict[str, Any],
) -> None:
    rows = connection.execute(
        "SELECT * FROM choice_event WHERE choice_id = ? ORDER BY sequence",
        (prompt["id"],),
    ).fetchall()
    derived = _derive_classifications(connection, prompt, list(rows))
    if derived["issues"]:
        raise OpsError("Existing choice classification is invalid")
    correction = payload["classification_correction"]
    option_key = correction["option_key"]
    current = derived["effective"].get(option_key)
    if not current:
        raise OpsError(
            f"Classification correction names an unknown option: {option_key}"
        )
    field = correction["field"]
    if current[field] != correction["prior_value"]:
        raise OpsError(
            f"Classification correction prior_value is stale for {option_key}/{field}"
        )
    candidate = dict(current)
    candidate[field] = correction["replacement_value"]
    correction_policy_issue = _comparability_correction_policy_issue(correction)
    if correction_policy_issue:
        raise OpsError(correction_policy_issue)
    issue = _classification_policy_issue(
        prompt,
        _tenant_slug(connection, str(prompt["tenant_id"])),
        candidate,
    )
    if issue:
        raise OpsError(issue)


def _semantic_choice_issues(
    connection: sqlite3.Connection,
    prompt: sqlite3.Row,
    events: list[sqlite3.Row],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    options: list[dict[str, Any]] = []
    option_by_key: dict[str, dict[str, Any]] = {}
    try:
        decoded_options = json.loads(prompt["options_json"])
    except (TypeError, json.JSONDecodeError):
        decoded_options = None
    if not isinstance(decoded_options, list) or not 3 <= len(decoded_options) <= 4:
        issues.append(
            {
                "code": "option-set-invalid",
                "message": "Immutable option set is not a three- or four-option list.",
            }
        )
    else:
        options = decoded_options
        keys: set[str] = set()
        roles: set[str] = set()
        for option in options:
            if not isinstance(option, dict):
                issues.append(
                    {
                        "code": "option-invalid",
                        "message": "Immutable option set contains a non-mapping option.",
                    }
                )
                continue
            key = option.get("key")
            role = option.get("role")
            if not isinstance(key, str) or not key or key in keys:
                issues.append(
                    {
                        "code": "option-key-invalid",
                        "message": "Immutable option keys must be present and unique.",
                    }
                )
            else:
                keys.add(key)
                option_by_key[key] = option
            if role not in CHOICE_ROLES or role in roles:
                issues.append(
                    {
                        "code": "option-role-invalid",
                        "message": "Immutable option roles must be supported and unique.",
                    }
                )
            else:
                roles.add(role)
            supplied = {
                field for field in CLASSIFICATION_FIELDS if field in option
            }
            if supplied:
                required_classification = {
                    "classification_version",
                    "pattern_key",
                    "action_boundary",
                }
                if not required_classification.issubset(option):
                    issues.append(
                        {
                            "code": "option-classification-incomplete",
                            "message": (
                                "Classified immutable options require version, "
                                "pattern, and action boundary."
                            ),
                        }
                    )
                elif (
                    option.get("classification_version")
                    != CHOICE_CLASSIFICATION_VERSION
                    or option.get("pattern_key") not in CHOICE_PATTERN_KEYS
                    or option.get("action_boundary")
                    not in CHOICE_ACTION_BOUNDARIES
                ):
                    issues.append(
                        {
                            "code": "option-classification-invalid",
                            "message": "Immutable option classification is unsupported.",
                        }
                    )
        if not {"recommended", "alternative"}.issubset(roles) or not (
            {"overlooked", "pause-or-deepen"} & roles
        ):
            issues.append(
                {
                    "code": "option-role-shape-invalid",
                    "message": (
                        "Immutable options must retain recommended and alternative "
                        "roles plus an overlooked or pause-or-deepen possibility."
                    ),
                }
            )
        if _hash(options) != prompt["option_set_hash"]:
            issues.append(
                {
                    "code": "option-set-hash-mismatch",
                    "message": "Immutable option set differs from its recorded identity.",
                }
            )
        recommended = option_by_key.get(prompt["recommendation_key"])
        if not recommended:
            issues.append(
                {
                    "code": "recommendation-key-invalid",
                    "message": "Recommendation key does not name an immutable option.",
                }
            )
        elif recommended.get("role") != "recommended":
            issues.append(
                {
                    "code": "recommendation-role-mismatch",
                    "message": "Recommendation key does not bind the recommended role.",
                }
            )

    selection_events = [
        event for event in events if event["event_type"] == "branch_selected"
    ]
    if len(selection_events) != 1:
        issues.append(
            {
                "code": "selection-count-invalid",
                "message": f"Expected exactly one branch selection; found {len(selection_events)}.",
            }
        )
    if events and events[0]["event_type"] != "branch_selected":
        issues.append(
            {
                "code": "selection-not-first",
                "message": "Branch selection is not the first choice event.",
            }
        )
    if selection_events:
        selection = selection_events[0]
        if selection["sequence"] != 1:
            issues.append(
                {
                    "code": "selection-sequence-invalid",
                    "message": "Branch selection must have sequence 1.",
                }
            )
        if selection["event_key"] != "selection":
            issues.append(
                {
                    "code": "selection-event-key-invalid",
                    "message": "Branch selection must use the stable selection event key.",
                }
            )
        try:
            payload = json.loads(selection["payload_json"])
        except (TypeError, json.JSONDecodeError):
            payload = None
        if not isinstance(payload, dict):
            issues.append(
                {
                    "code": "selection-payload-invalid",
                    "message": "Branch selection payload is not a mapping.",
                }
            )
        else:
            selected_key = payload.get("selected_option_key")
            selected = option_by_key.get(selected_key)
            if not selected:
                issues.append(
                    {
                        "code": "selection-key-invalid",
                        "message": "Selected key does not name an immutable option.",
                    }
                )
            elif payload.get("selected_option_role") != selected.get("role"):
                issues.append(
                    {
                        "code": "selection-role-mismatch",
                        "message": "Selection role differs from the immutable option set.",
                    }
                )
            if payload.get("authority_effect") != "none":
                issues.append(
                    {
                        "code": "selection-authority-invalid",
                        "message": "Choice selection must not grant execution authority.",
                    }
                )
            review_after = payload.get("review_after")
            try:
                _timestamp(review_after)
            except (OpsError, TypeError):
                issues.append(
                    {
                        "code": "selection-review-time-invalid",
                        "message": "Choice selection has an invalid review timestamp.",
                    }
                )

    supersession_events: list[sqlite3.Row] = []
    for event in events:
        if event["event_type"] == "branch_selected":
            continue
        if event["event_type"] not in EVENT_TYPES:
            issues.append(
                {
                    "code": "event-type-invalid",
                    "message": f"Event {event['id']} has an unsupported type.",
                }
            )
            continue
        try:
            payload = json.loads(event["payload_json"])
            if not isinstance(payload, dict):
                raise OpsError("payload must be a mapping")
            normalized = _validate_event_payload(event["event_type"], payload)
        except (OpsError, TypeError, ValueError, json.JSONDecodeError):
            issues.append(
                {
                    "code": "event-payload-invalid",
                    "message": f"Event {event['id']} has an invalid semantic payload.",
                }
            )
            continue
        if _canonical_json(normalized) != event["payload_json"]:
            issues.append(
                {
                    "code": "event-payload-noncanonical",
                    "message": f"Event {event['id']} differs from its canonical payload.",
                }
            )
        if event["event_type"] == "superseded":
            supersession_events.append(event)

    if isinstance(decoded_options, list):
        issues.extend(
            _derive_classifications(connection, prompt, list(events))["issues"]
        )

    if len(supersession_events) > 1:
        issues.append(
            {
                "code": "supersession-count-invalid",
                "message": "A choice may have at most one supersession disposition.",
            }
        )
    for event in supersession_events:
        payload = json.loads(event["payload_json"])
        issues.extend(
            _supersession_issues(
                connection,
                prompt,
                str(prompt["id"]),
                payload["superseding_choice_id"],
            )
        )
    return issues


def _supersession_issues(
    connection: sqlite3.Connection,
    origin: sqlite3.Row,
    choice_id: str,
    superseding_choice_id: str,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    seen = {choice_id}
    current_id = superseding_choice_id
    while current_id:
        if current_id in seen:
            issues.append(
                {
                    "code": "supersession-cycle",
                    "message": "Choice supersession lineage contains a cycle.",
                }
            )
            return issues
        seen.add(current_id)
        current = connection.execute(
            "SELECT * FROM choice_prompt WHERE id = ?", (current_id,)
        ).fetchone()
        if not current:
            issues.append(
                {
                    "code": "superseding-choice-missing",
                    "message": "Superseding choice does not exist.",
                }
            )
            return issues
        if any(
            current[field] != origin[field]
            for field in ("tenant_id", "workspace_id", "lane")
        ):
            issues.append(
                {
                    "code": "superseding-choice-scope-mismatch",
                    "message": "Superseding choice crosses tenant, workspace, or lane.",
                }
            )
            return issues
        rows = connection.execute(
            """SELECT payload_json FROM choice_event
            WHERE choice_id = ? AND event_type = 'superseded'
            ORDER BY sequence""",
            (current_id,),
        ).fetchall()
        if not rows:
            return issues
        if len(rows) > 1:
            issues.append(
                {
                    "code": "supersession-lineage-ambiguous",
                    "message": "Superseding choice has multiple supersession dispositions.",
                }
            )
            return issues
        try:
            payload = json.loads(rows[0]["payload_json"])
            current_id = str(payload["superseding_choice_id"])
        except (KeyError, TypeError, json.JSONDecodeError):
            issues.append(
                {
                    "code": "supersession-lineage-invalid",
                    "message": "Superseding choice has an invalid lineage reference.",
                }
            )
            return issues
    return issues


def _attention_flags(
    prompt: sqlite3.Row,
    state: str,
    outcome: dict[str, Any] | None,
    verification: dict[str, Any],
) -> list[dict[str, str]]:
    flags = []
    if not verification["ok"]:
        flags.append({"priority": "P0", "code": "invalid-chain", "message": "Choice event chain failed verification."})
    if outcome and (
        outcome["payload"].get("authority_issue")
        or outcome["payload"].get("membrane_issue")
    ):
        flags.append({"priority": "P0", "code": "authority-or-membrane-incident", "message": "Outcome recorded a controlling boundary incident."})
    if state in {"selected", "review_deferred", "outcome_pending"}:
        flags.append({"priority": "P2", "code": "outcome-unresolved", "message": "Selected branch lacks a resolved outcome."})
    if prompt["consequence_level"] != "ordinary":
        flags.append({"priority": "P1", "code": "authority-separate", "message": "Choice receipt grants no consequential action authority."})
    return flags


def _event_hash(values: dict[str, Any]) -> str:
    payload = {key: values[key] for key in _event_hash_fields()}
    return _hash(payload)


def _event_hash_fields() -> tuple[str, ...]:
    return (
        "id",
        "choice_id",
        "tenant_id",
        "event_key",
        "sequence",
        "event_type",
        "actor_id",
        "actor_label",
        "action_summary",
        "occurred_at",
        "evidence_ref",
        "payload_json",
        "recorded_at",
        "prior_hash",
    )


def _event_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "event_key": row["event_key"],
        "sequence": row["sequence"],
        "event_type": row["event_type"],
        "actor_id": row["actor_id"],
        "actor_label": row["actor_label"],
        "action_summary": row["action_summary"],
        "occurred_at": row["occurred_at"],
        "recorded_at": row["recorded_at"],
        "evidence_ref": row["evidence_ref"],
        "payload": json.loads(row["payload_json"]),
        "prior_hash": row["prior_hash"],
        "event_hash": row["event_hash"],
    }


def _prompt(connection: sqlite3.Connection, choice_id: str) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM choice_prompt WHERE id = ?", (choice_id,)
    ).fetchone()
    if not row:
        raise OpsError(f"Unknown choice: {choice_id}")
    return row


def _validate_actor(
    connection: sqlite3.Connection, tid: str, actor_id: str | None
) -> None:
    if not actor_id:
        return
    actor = connection.execute(
        "SELECT id FROM actor WHERE id = ? AND tenant_id = ? AND active = 1",
        (actor_id, tid),
    ).fetchone()
    if not actor:
        raise OpsError(f"Unknown or cross-tenant choice actor: {actor_id}")


def _selected_label(projection: dict[str, Any]) -> str:
    selected_key = projection["selection"]["payload"]["selected_option_key"]
    return next(
        option["label"] for option in projection["options"] if option["key"] == selected_key
    )


def _projection_guardrail(projection: dict[str, Any]) -> dict[str, str] | None:
    outcome = projection["outcome"]
    if not outcome:
        return None
    payload = outcome["payload"]
    if not (payload.get("authority_issue") or payload.get("membrane_issue")):
        return None
    return {
        "choice_id": projection["choice"]["id"],
        "option_key": projection["selection"]["payload"]["selected_option_key"],
        "reason": "Prior outcome recorded an authority or membrane incident.",
        "evidence_ref": outcome["evidence_ref"],
    }


def _guidance_rationale(
    resolved_count: int,
    guardrails: list[dict[str, str]],
    favored: list[str],
    demoted: list[str],
) -> str:
    if guardrails:
        return "Prior outcomes contain an authority or membrane guardrail; surface it immediately."
    if favored or demoted:
        return "At least one explicit comparability cohort has outcome evidence; preserve an overlooked path while applying its policy."
    if resolved_count:
        return "Explicit comparability cohorts remain thin or unavailable; cite outcomes without changing option order."
    return "No comparable outcome evidence is available; use current evidence and repository learning."


def _choice_guidance_policy(
    tenant: str,
    workspace_id: str,
    lane: str,
    as_of: str,
) -> dict[str, Any] | None:
    reference = _timestamp(as_of)
    for configured in CHOICE_GUIDANCE_POLICIES:
        if (
            configured["tenant"] != tenant
            or configured["workspace_id"] != workspace_id
            or configured["lane"] != lane
        ):
            continue
        effective = _timestamp(configured["effective_at"])
        observation_end = _timestamp(configured["observation_ends_at"])
        if reference < effective:
            phase = "scheduled"
            frozen = False
        elif reference < observation_end:
            phase = "calibration"
            frozen = configured["guidance_mode"] == "diagnostic-only"
        else:
            phase = "awaiting-disposition"
            frozen = bool(configured["freeze_until_explicit_disposition"])
        return {
            **configured,
            "phase": phase,
            "ordering_frozen": frozen,
        }
    return None


def _bounded(
    value: Any,
    name: str,
    *,
    required: bool,
    maximum: int = MAX_TEXT,
) -> str:
    text = _text(value)
    if required and not text:
        raise OpsError(f"{name} is required")
    if len(text) > maximum:
        raise OpsError(f"{name} exceeds {maximum} characters")
    if scan_text(text):
        raise OpsError(f"{name} failed privacy scanning")
    return text


def _nullable_bounded(
    value: Any, name: str, *, maximum: int = MAX_TEXT
) -> str | None:
    text = _text(value)
    return _bounded(text, name, required=False, maximum=maximum) or None


def _string_list(value: Any, name: str) -> list[str]:
    if not isinstance(value, list):
        raise OpsError(f"{name} must be a list")
    if len(value) > 20:
        raise OpsError(f"{name} contains too many values")
    return [_bounded(item, name, required=True, maximum=300) for item in value]


def _enum_or_missing(value: Any, allowed: tuple[str, ...], name: str) -> str:
    text = _text(value) or "Missing"
    if text not in allowed:
        raise OpsError(f"Invalid {name}: {text}")
    return text


def _privacy_safe(value: Any, context: str) -> None:
    serialized = _canonical_json(value)
    if len(serialized) > MAX_JSON:
        raise OpsError(f"{context} is too large")
    if scan_text(serialized):
        raise OpsError(f"{context} failed privacy scanning")
    lowered = serialized.lower()
    for key in (
        "evidence_body",
        "raw_evidence",
        "raw_content",
        "customer_private_body",
        "client_private_body",
    ):
        if f'"{key}"' in lowered:
            raise OpsError(f"{context} may link evidence but may not store {key}")


def _timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(_text(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise OpsError(f"Invalid timestamp: {value}") from exc
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _normalize_yaml_dates(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _normalize_yaml_dates(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_yaml_dates(item) for item in value]
    return value


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()
