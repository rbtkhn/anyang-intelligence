import sqlite3

from anyang_loop.ops_db import SCHEMA_VERSION, connect, migrate, schema_version


def test_sqlite_safe_backup_restores_integrity_schema_and_events(tmp_path):
    source_path = tmp_path / "source.db"
    backup_path = tmp_path / "backup.db"

    with connect(source_path, create_parent=True) as source:
        migrate(source, "2026-07-11T00:00:00Z")
        source.execute(
            "INSERT INTO tenant(id, slug, name, policy_profile, created_at) "
            "VALUES ('tenant-1', 'synthetic', 'Synthetic Recovery Tenant', 'test-only', '2026-07-11T00:00:00Z')"
        )
        source.execute(
            "INSERT INTO event(id, tenant_id, event_type, actor, details, created_at) "
            "VALUES ('event-1', 'tenant-1', 'synthetic-recovery-check', 'test', '', '2026-07-11T00:00:00Z')"
        )
        source.commit()
        with sqlite3.connect(backup_path) as backup:
            source.backup(backup)

    with connect(backup_path) as restored:
        assert restored.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert schema_version(restored) == SCHEMA_VERSION
        assert restored.execute("SELECT COUNT(*) FROM schema_migration").fetchone()[0] >= 1
        assert restored.execute("SELECT event_type FROM event WHERE id = 'event-1'").fetchone()[0] == "synthetic-recovery-check"
