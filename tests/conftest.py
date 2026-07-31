from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def isolate_anyang_user_configuration(monkeypatch, tmp_path):
    """Never let repository tests read or mutate the operator's real config."""
    monkeypatch.delenv("ANYANG_DATA_DIR", raising=False)
    monkeypatch.setenv("ANYANG_CONFIG_HOME", str(tmp_path / "anyang-user-config"))
