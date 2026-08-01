from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Mapping

from .choice_learning import choice_context, choice_guardrails, choice_review
from .external_ledger import (
    CHOICE_SCOPE,
    DATABASE_NAME,
    LedgerConfigError,
    LedgerResolution,
    clear_user_config,
    resolve_ledger,
    user_config_path,
    validate_external_data_dir,
    write_user_config,
)
from .ops_db import SCHEMA_VERSION, connect, connect_readonly, migrate, schema_version
from .ops_service import OpsError, add_actor, init_tenant, now_utc


def choice_status(
    resolution: LedgerResolution,
    *,
    include_learning: bool = False,
    include_guardrails: bool = False,
    as_of: str | None = None,
) -> dict[str, object]:
    base: dict[str, object] = {
        "schema_version": 1,
        "status": "unconfigured",
        "source": resolution.source,
        "database": str(resolution.database) if resolution.database else None,
        "config_path": str(resolution.config_path),
        "retention_available": False,
        "scope": dict(CHOICE_SCOPE),
        "ledger_schema_version": None,
        "due_count": 0,
        "resolved_count": 0,
        "review_candidate": None,
        "reflection_sample_ready": False,
        "ordering_frozen": True,
        "guardrails": [],
        "authority_effect": "none",
    }
    if resolution.database is None:
        return base
    if not resolution.database.is_file():
        base["status"] = "configured-missing"
        return base
    try:
        with connect_readonly(resolution.database) as connection:
            version = schema_version(connection)
            base["ledger_schema_version"] = version
            if version != SCHEMA_VERSION:
                base["status"] = "schema-incompatible"
                return base
            tenant = connection.execute(
                """SELECT id, retainer_cents, contractor_budget_cents, tool_budget_cents
                FROM tenant WHERE slug = ?""",
                (CHOICE_SCOPE["tenant"],),
            ).fetchone()
            if not tenant:
                base["status"] = "configured-incomplete"
                return base
            if any(tenant[key] != 0 for key in ("retainer_cents", "contractor_budget_cents", "tool_budget_cents")):
                base["status"] = "scope-conflict"
                return base
            actor = connection.execute(
                "SELECT role, active FROM actor WHERE tenant_id = ? AND name = ?",
                (tenant["id"], CHOICE_SCOPE["actor_name"]),
            ).fetchone()
            if not actor:
                base["status"] = "configured-incomplete"
                return base
            if actor["role"] != CHOICE_SCOPE["actor_role"] or actor["active"] != 1:
                base["status"] = "scope-conflict"
                return base
            base["status"] = "ready"
            base["retention_available"] = True
            if include_learning:
                context = choice_context(
                    connection,
                    CHOICE_SCOPE["tenant"],
                    CHOICE_SCOPE["workspace"],
                    CHOICE_SCOPE["lane"],
                    "next-action",
                    as_of,
                )
                review = choice_review(
                    connection,
                    CHOICE_SCOPE["tenant"],
                    CHOICE_SCOPE["workspace"],
                    as_of,
                )
                base.update(
                    {
                        "due_count": review["due_count"],
                        "resolved_count": review["resolved_count"],
                        "review_candidate": review["choices"][0] if review["choices"] else None,
                        "reflection_sample_ready": review["reflection_sample_ready"],
                        "ordering_frozen": context["recommendation_guidance"]["ordering_frozen"],
                        "guardrails": context["guardrails"],
                    }
                )
            elif include_guardrails:
                base["guardrails"] = choice_guardrails(
                    connection,
                    CHOICE_SCOPE["tenant"],
                    CHOICE_SCOPE["workspace"],
                    CHOICE_SCOPE["lane"],
                    "next-action",
                )
    except sqlite3.DatabaseError as exc:
        raise LedgerConfigError(f"Configured Anyang ledger is unreadable: {resolution.database}") from exc
    return base


def resolved_choice_status(
    explicit_db: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
    *,
    include_learning: bool = False,
    include_guardrails: bool = False,
    as_of: str | None = None,
) -> dict[str, object]:
    return choice_status(
        resolve_ledger(explicit_db, environ),
        include_learning=include_learning,
        include_guardrails=include_guardrails,
        as_of=as_of,
    )


def configure_choice_continuity(
    data_dir: str | Path,
    repo_root: str | Path,
    *,
    environ: Mapping[str, str] | None = None,
    dry_run: bool = False,
) -> dict[str, object]:
    directory = validate_external_data_dir(data_dir, repo_root)
    database = directory / DATABASE_NAME
    config_path = user_config_path(environ)
    plan = {
        "dry_run": dry_run,
        "action": "configure_choice_continuity",
        "database": str(database),
        "config_path": str(config_path),
        "scope": dict(CHOICE_SCOPE),
        "schema_version": SCHEMA_VERSION,
        "authority_effect": "none",
    }
    if dry_run:
        return plan
    _reject_incompatible_existing_database(database)
    connection = connect(database, create_parent=True)
    try:
        migrate(connection, now_utc())
        tenant = connection.execute(
            "SELECT * FROM tenant WHERE slug = ?", (CHOICE_SCOPE["tenant"],)
        ).fetchone()
        if tenant:
            if any(tenant[key] != 0 for key in ("retainer_cents", "contractor_budget_cents", "tool_budget_cents")):
                raise OpsError("Existing anyang-internal tenant conflicts with choice continuity scope")
        else:
            init_tenant(
                connection,
                slug=CHOICE_SCOPE["tenant"],
                name="Anyang Internal",
                policy_profile="choice-learning-v1",
                retainer_cents=0,
                contractor_budget_cents=0,
                tool_budget_cents=0,
            )
            tenant = connection.execute(
                "SELECT * FROM tenant WHERE slug = ?", (CHOICE_SCOPE["tenant"],)
            ).fetchone()
        actor = connection.execute(
            "SELECT role, active FROM actor WHERE tenant_id = ? AND name = ?",
            (tenant["id"], CHOICE_SCOPE["actor_name"]),
        ).fetchone()
        if actor:
            if actor["role"] != CHOICE_SCOPE["actor_role"] or actor["active"] != 1:
                raise OpsError("Council Steward actor conflicts with choice continuity scope")
        else:
            add_actor(
                connection,
                CHOICE_SCOPE["tenant"],
                CHOICE_SCOPE["actor_name"],
                CHOICE_SCOPE["actor_role"],
            )
    finally:
        connection.close()
    write_user_config(directory, repo_root, environ)
    status = choice_status(
        LedgerResolution("user-config", database, directory, config_path)
    )
    return {**plan, "dry_run": False, "status": status}


def clear_choice_continuity(
    repo_root: str | Path,
    *,
    environ: Mapping[str, str] | None = None,
    dry_run: bool = False,
) -> dict[str, object]:
    target = user_config_path(environ)
    repository = Path(repo_root).resolve()
    if target == repository or target.is_relative_to(repository):
        raise LedgerConfigError("Anyang user configuration must remain outside the repository")
    if dry_run:
        return {
            "dry_run": True,
            "action": "clear_choice_continuity",
            "config_path": str(target),
            "config_exists": target.exists(),
            "database_deleted": False,
        }
    _, existed = clear_user_config(environ)
    return {
        "dry_run": False,
        "action": "clear_choice_continuity",
        "config_path": str(target),
        "config_removed": existed,
        "database_deleted": False,
    }


def render_choice_status_markdown(data: dict[str, object]) -> str:
    scope = data["scope"]
    lines = [
        "# Choice Continuity Status",
        "",
        f"Status: `{data['status']}`",
        f"Configuration source: `{data['source']}`",
        f"Retention available: {data['retention_available']}",
        f"Ledger schema: `{data['ledger_schema_version'] if data['ledger_schema_version'] is not None else 'Missing'}`",
        f"Scope: `{scope['tenant']} / {scope['workspace']} / {scope['lane']}`",
        "Authority effect: `none`",
        "",
    ]
    return "\n".join(lines)


def _reject_incompatible_existing_database(path: Path) -> None:
    if not path.exists():
        return
    try:
        with connect_readonly(path) as connection:
            version = schema_version(connection)
            if version > SCHEMA_VERSION:
                raise OpsError(
                    f"Configured ledger schema {version} is newer than supported schema {SCHEMA_VERSION}"
                )
            if version == 0:
                tables = connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
                ).fetchall()
                if tables:
                    raise OpsError("Refusing to initialize an unrecognized non-empty SQLite database")
    except sqlite3.DatabaseError as exc:
        raise OpsError(f"Configured ledger is not a readable SQLite database: {path}") from exc
