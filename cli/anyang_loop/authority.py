from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from .artifact_state import repository_root


DEFAULT_ENVELOPE = "authority-envelope.yaml"
REQUIRED_DOMAIN_FIELDS = (
    "scope", "allowed_actions", "prohibited_actions", "required_evidence",
    "approval_threshold", "approver", "review_expiry", "audit_record",
    "revocation_path", "recovery",
)


@dataclass(frozen=True)
class AuthorityDiagnostic:
    code: str
    path: Path
    message: str


@dataclass(frozen=True)
class AuthorityPreflight:
    domain: str
    action: str
    status: str
    authority: str
    approval_required: bool
    blockers: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "action": self.action,
            "status": self.status,
            "authority": self.authority,
            "approval_required": self.approval_required,
            "blockers": list(self.blockers),
            "enforcement": "preflight-reports-never-grants-authority",
        }


def load_authority_envelope(path: str | Path | None = None) -> tuple[Path, dict[str, Any]]:
    target = (Path(path) if path else repository_root() / DEFAULT_ENVELOPE).resolve()
    try:
        data = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    except FileNotFoundError as exc:
        raise ValueError(f"Authority envelope not found: {target}") from exc
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"Cannot load authority envelope {target}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Authority envelope root must be a mapping.")
    return target, data


def validate_authority_envelope(path: str | Path | None = None) -> list[AuthorityDiagnostic]:
    target = (Path(path) if path else repository_root() / DEFAULT_ENVELOPE).resolve()
    try:
        target, data = load_authority_envelope(target)
    except ValueError as exc:
        return [AuthorityDiagnostic("authority-envelope-invalid", target, str(exc))]
    diagnostics: list[AuthorityDiagnostic] = []
    if data.get("version") != 1:
        diagnostics.append(AuthorityDiagnostic("authority-version-invalid", target, "Version must be 1."))
    governance = data.get("governance")
    for field in ("organization", "ai_role", "owner", "default_posture", "conflict_precedence"):
        if not isinstance(governance, dict) or not governance.get(field):
            diagnostics.append(AuthorityDiagnostic("authority-governance-incomplete", target, f"Governance requires '{field}'."))
    roles = data.get("roles")
    for role in ("engineer", "executive", "interface", "steward", "client"):
        if not isinstance(roles, dict) or not isinstance(roles.get(role), dict) or not roles[role].get("authority"):
            diagnostics.append(AuthorityDiagnostic("authority-role-incomplete", target, f"Role '{role}' requires an authority declaration."))
    domains = data.get("domains")
    if not isinstance(domains, dict) or not domains:
        return diagnostics + [AuthorityDiagnostic("authority-domains-empty", target, "Declare at least one authority domain.")]
    for name, domain in domains.items():
        if not isinstance(domain, dict):
            diagnostics.append(AuthorityDiagnostic("authority-domain-invalid", target, f"Domain '{name}' must be a mapping."))
            continue
        for field in REQUIRED_DOMAIN_FIELDS:
            value = domain.get(field)
            if value is None or value == "" or value == []:
                diagnostics.append(AuthorityDiagnostic("authority-field-missing", target, f"Domain '{name}' requires '{field}'."))
        if domain.get("approver") == "" or domain.get("review_expiry") == "":
            diagnostics.append(AuthorityDiagnostic("authority-approval-incomplete", target, f"Domain '{name}' needs approver and review expiry."))
        required_approvers = domain.get("required_approvers")
        if required_approvers is not None:
            if (
                not isinstance(required_approvers, list)
                or len(required_approvers) < 2
                or any(not isinstance(item, str) or not item for item in required_approvers)
            ):
                diagnostics.append(
                    AuthorityDiagnostic(
                        "authority-required-approvers-invalid",
                        target,
                        f"Domain '{name}' required_approvers must name at least two authorities.",
                    )
                )
            elif domain.get("approver") not in required_approvers:
                diagnostics.append(
                    AuthorityDiagnostic(
                        "authority-approver-not-required",
                        target,
                        f"Domain '{name}' primary approver must appear in required_approvers.",
                    )
                )
    rollout = data.get("rollout")
    if not isinstance(rollout, dict) or rollout.get("stages") != ["shadow", "bounded-operation", "measured-expansion"]:
        diagnostics.append(AuthorityDiagnostic("authority-rollout-invalid", target, "Rollout must define shadow, bounded-operation, and measured-expansion in order."))
    floors = data.get("protected_floors")
    if not isinstance(floors, list) or not floors:
        diagnostics.append(AuthorityDiagnostic("authority-protected-floors-missing", target, "Declare non-delegable protected floors."))
    aliases = data.get("migration_aliases")
    if not isinstance(aliases, dict) or aliases.get("ai-ceo") != "executive" or aliases.get("hannah") != "interface":
        diagnostics.append(AuthorityDiagnostic("authority-aliases-incomplete", target, "Declare legacy role aliases for migration."))
    return diagnostics


def authority_preflight(domain: str, action: str, path: str | Path | None = None) -> AuthorityPreflight:
    _, data = load_authority_envelope(path)
    domains = data.get("domains", {})
    selected = domains.get(domain)
    if not isinstance(selected, dict):
        return AuthorityPreflight(domain, action, "blocked", "unknown", True, ("unknown-domain",))
    prohibited = set(selected.get("prohibited_actions", []))
    allowed = set(selected.get("allowed_actions", []))
    required_approvers = selected.get("required_approvers")
    if isinstance(required_approvers, list) and required_approvers:
        authority = "+".join(str(item) for item in required_approvers)
        approval_blocker = "dual-approval-required"
    else:
        authority = str(selected.get("approver"))
        approval_blocker = "explicit-approval-required"
    if action in prohibited:
        return AuthorityPreflight(domain, action, "blocked", authority, True, ("prohibited-action",))
    if action not in allowed:
        return AuthorityPreflight(
            domain,
            action,
            "approval-required",
            authority,
            True,
            ("action-not-declared", approval_blocker),
        )
    return AuthorityPreflight(
        domain,
        action,
        "approval-required",
        authority,
        True,
        (approval_blocker,),
    )


def approval_receipt_is_current(receipt: dict[str, Any], *, as_of: date | None = None) -> bool:
    if receipt.get("status") != "Approved" or receipt.get("revoked") is True:
        return False
    today = as_of or date.today()
    expires = receipt.get("expires_on")
    if not expires:
        return False
    try:
        return today <= date.fromisoformat(str(expires))
    except ValueError:
        return False
