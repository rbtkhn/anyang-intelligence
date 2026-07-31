from __future__ import annotations

import os
from pathlib import Path

import pytest

from anyang_loop.choice_continuity import (
    choice_status,
    clear_choice_continuity,
    configure_choice_continuity,
    resolved_choice_status,
)
from anyang_loop.external_ledger import (
    CHOICE_SCOPE,
    LedgerConfigError,
    load_user_config,
    resolve_ledger,
    user_config_path,
    validate_external_data_dir,
)
from anyang_loop.ops_cli import main
from anyang_loop.ops_db import SCHEMA_VERSION, connect, migrate, schema_version
from anyang_loop.ops_service import OpsError, add_actor, init_tenant, now_utc


def environment(tmp_path: Path) -> dict[str, str]:
    return {
        "LOCALAPPDATA": str(tmp_path / "local-app-data"),
        "ANYANG_CONFIG_HOME": str(tmp_path / "config-home"),
    }


def test_user_config_locations_are_platform_appropriate(tmp_path: Path):
    assert user_config_path(
        {"LOCALAPPDATA": str(tmp_path / "local")}, platform_name="win32", home=tmp_path
    ) == (tmp_path / "local" / "AnyangIntelligence" / "config.toml").resolve()
    assert user_config_path({}, platform_name="darwin", home=tmp_path) == (
        tmp_path / "Library" / "Application Support" / "AnyangIntelligence" / "config.toml"
    ).resolve()
    assert user_config_path({}, platform_name="linux", home=tmp_path) == (
        tmp_path / ".config" / "anyang-intelligence" / "config.toml"
    ).resolve()


def test_resolution_precedence_is_explicit_environment_config_then_fallback(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    env = environment(tmp_path)
    configured = tmp_path / "configured-data"
    configure_choice_continuity(configured, repo, environ=env)

    assert resolve_ledger(environ=env).source == "user-config"
    with_environment = {**env, "ANYANG_DATA_DIR": str(tmp_path / "environment-data")}
    assert resolve_ledger(environ=with_environment).source == "environment"
    explicit = resolve_ledger(tmp_path / "explicit.db", with_environment)
    assert explicit.source == "explicit"
    assert explicit.database == (tmp_path / "explicit.db").resolve()
    assert resolve_ledger(environ={"ANYANG_CONFIG_HOME": str(tmp_path / "empty")}).source == "unconfigured"


def test_configure_dry_run_is_pure_then_execute_is_idempotent_and_clear_keeps_database(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    data = tmp_path / "private" / "data"
    env = environment(tmp_path)

    dry = configure_choice_continuity(data, repo, environ=env, dry_run=True)
    assert dry["schema_version"] == SCHEMA_VERSION == 8
    assert not data.exists()
    assert not user_config_path(env).exists()

    first = configure_choice_continuity(data, repo, environ=env)
    second = configure_choice_continuity(data, repo, environ=env)
    assert first["status"]["status"] == second["status"]["status"] == "ready"
    database = data / "anyang-ops.db"
    assert database.exists()
    config = load_user_config(user_config_path(env))
    assert config["choice"] == CHOICE_SCOPE
    with connect(database) as connection:
        assert schema_version(connection) == 8
        assert connection.execute(
            "SELECT COUNT(*) FROM tenant WHERE slug = 'anyang-internal'"
        ).fetchone()[0] == 1
        assert connection.execute(
            "SELECT COUNT(*) FROM actor WHERE name = 'Council Steward'"
        ).fetchone()[0] == 1

    clear_plan = clear_choice_continuity(repo, environ=env, dry_run=True)
    assert clear_plan["database_deleted"] is False
    assert user_config_path(env).exists()
    cleared = clear_choice_continuity(repo, environ=env)
    assert cleared["config_removed"] is True
    assert database.exists()


def test_status_is_read_only_and_reports_all_non_error_states(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    env = environment(tmp_path)
    assert resolved_choice_status(environ=env)["status"] == "unconfigured"

    config_path = user_config_path(env)
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        "version = 1\n"
        f'data_dir = "{str(tmp_path / "missing").replace(os.sep, "/")}"\n\n'
        "[choice]\n"
        + "\n".join(f'{key} = "{value}"' for key, value in CHOICE_SCOPE.items())
        + "\n",
        encoding="utf-8",
    )
    assert resolved_choice_status(environ=env)["status"] == "configured-missing"

    data = tmp_path / "ready"
    configure_choice_continuity(data, repo, environ=env)
    database = data / "anyang-ops.db"
    before = database.read_bytes()
    modified = database.stat().st_mtime_ns
    status = resolved_choice_status(environ=env, include_learning=True)
    assert status["status"] == "ready"
    assert status["retention_available"] is True
    assert database.read_bytes() == before
    assert database.stat().st_mtime_ns == modified

    incomplete = tmp_path / "incomplete.db"
    with connect(incomplete, create_parent=True) as connection:
        migrate(connection, now_utc())
    assert choice_status(resolve_ledger(incomplete))["status"] == "configured-incomplete"

    legacy = tmp_path / "legacy.db"
    with connect(legacy, create_parent=True) as connection:
        connection.execute(
            "CREATE TABLE schema_migration(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)"
        )
        connection.execute("INSERT INTO schema_migration VALUES (7, '2026-07-01T00:00:00Z')")
        connection.commit()
    assert choice_status(resolve_ledger(legacy))["status"] == "schema-incompatible"


def test_configure_rejects_repo_paths_symlink_escapes_and_scope_conflicts(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    env = environment(tmp_path)
    with pytest.raises(LedgerConfigError, match="outside the repository"):
        validate_external_data_dir(repo / "private", repo)

    link = tmp_path / "repo-link"
    try:
        link.symlink_to(repo, target_is_directory=True)
    except OSError:
        pass
    else:
        with pytest.raises(LedgerConfigError, match="outside the repository"):
            validate_external_data_dir(link / "private", repo)

    conflict_data = tmp_path / "conflict"
    database = conflict_data / "anyang-ops.db"
    with connect(database, create_parent=True) as connection:
        migrate(connection, now_utc())
        init_tenant(
            connection,
            slug="anyang-internal",
            name="Anyang Internal",
            policy_profile="choice-learning-v1",
            retainer_cents=1,
            contractor_budget_cents=0,
            tool_budget_cents=0,
        )
    with pytest.raises(OpsError, match="conflicts"):
        configure_choice_continuity(conflict_data, repo, environ=env)
    assert not user_config_path(env).exists()

    actor_data = tmp_path / "actor-conflict"
    actor_db = actor_data / "anyang-ops.db"
    with connect(actor_db, create_parent=True) as connection:
        migrate(connection, now_utc())
        init_tenant(
            connection,
            slug="anyang-internal",
            name="Anyang Internal",
            policy_profile="choice-learning-v1",
            retainer_cents=0,
            contractor_budget_cents=0,
            tool_budget_cents=0,
        )
        add_actor(connection, "anyang-internal", "Council Steward", "wrong-role")
    with pytest.raises(OpsError, match="actor conflicts"):
        configure_choice_continuity(actor_data, repo, environ=env)
    assert choice_status(resolve_ledger(actor_db))["status"] == "scope-conflict"


def test_malformed_or_unrecognized_configuration_fails_closed(tmp_path: Path):
    env = environment(tmp_path)
    config = user_config_path(env)
    config.parent.mkdir(parents=True)
    config.write_text("not valid = [", encoding="utf-8")
    with pytest.raises(LedgerConfigError, match="Invalid Anyang user configuration"):
        resolve_ledger(environ=env)

    config.write_text(
        "version = 1\ndata_dir = \"C:/private\"\nunknown = true\n[choice]\n",
        encoding="utf-8",
    )
    with pytest.raises(LedgerConfigError, match="unknown or missing fields"):
        resolve_ledger(environ=env)

    unreadable = tmp_path / "unreadable.db"
    unreadable.write_text("not sqlite", encoding="utf-8")
    with pytest.raises(LedgerConfigError, match="unreadable"):
        choice_status(resolve_ledger(unreadable))


def test_cli_configure_dry_run_and_status_do_not_activate_private_state(tmp_path: Path, monkeypatch, capsys):
    from anyang_loop import ops_cli

    config_home = tmp_path / "config-home"
    monkeypatch.setenv("ANYANG_CONFIG_HOME", str(config_home))
    fake_repo = tmp_path / "repo"
    fake_repo.mkdir()
    monkeypatch.setattr(ops_cli, "REPO_ROOT", fake_repo)
    data = tmp_path / "private"
    assert main(["choice", "configure", "--data-dir", str(data), "--dry-run"]) == 0
    assert '"dry_run": true' in capsys.readouterr().out
    assert not data.exists()
    assert main(["choice", "status", "--format", "json"]) == 0
    assert '"status": "unconfigured"' in capsys.readouterr().out
