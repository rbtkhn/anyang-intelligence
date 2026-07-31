from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Mapping
import uuid

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib


CONFIG_VERSION = 1
DATABASE_NAME = "anyang-ops.db"
CHOICE_SCOPE = {
    "tenant": "anyang-internal",
    "workspace": "anyang-intelligence",
    "lane": "repository",
    "actor_name": "Council Steward",
    "actor_role": "steward",
}


class LedgerConfigError(ValueError):
    pass


@dataclass(frozen=True)
class LedgerResolution:
    source: str
    database: Path | None
    data_dir: Path | None
    config_path: Path

    @property
    def configured(self) -> bool:
        return self.database is not None


def user_config_path(
    environ: Mapping[str, str] | None = None,
    *,
    platform_name: str | None = None,
    home: Path | None = None,
) -> Path:
    env = os.environ if environ is None else environ
    if env.get("ANYANG_CONFIG_HOME"):
        return Path(env["ANYANG_CONFIG_HOME"]).expanduser().resolve() / "config.toml"
    platform_value = platform_name or sys.platform
    home_value = (home or Path.home()).expanduser()
    if platform_value == "win32" and env.get("LOCALAPPDATA"):
        root = Path(env["LOCALAPPDATA"]) / "AnyangIntelligence"
    elif platform_value == "darwin":
        root = home_value / "Library" / "Application Support" / "AnyangIntelligence"
    elif env.get("XDG_CONFIG_HOME"):
        root = Path(env["XDG_CONFIG_HOME"]) / "anyang-intelligence"
    else:
        root = home_value / ".config" / "anyang-intelligence"
    return root.resolve() / "config.toml"


def resolve_ledger(
    explicit_db: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> LedgerResolution:
    env = os.environ if environ is None else environ
    config_path = user_config_path(env)
    if explicit_db:
        database = Path(explicit_db).expanduser().resolve()
        return LedgerResolution("explicit", database, database.parent, config_path)
    if env.get("ANYANG_DATA_DIR"):
        data_dir = Path(env["ANYANG_DATA_DIR"]).expanduser().resolve()
        return LedgerResolution("environment", data_dir / DATABASE_NAME, data_dir, config_path)
    config = load_user_config(config_path)
    if config is not None:
        data_dir = Path(config["data_dir"]).expanduser().resolve()
        return LedgerResolution("user-config", data_dir / DATABASE_NAME, data_dir, config_path)
    return LedgerResolution("unconfigured", None, None, config_path)


def load_user_config(path: str | Path) -> dict[str, object] | None:
    target = Path(path)
    if not target.exists():
        return None
    try:
        with target.open("rb") as handle:
            value = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise LedgerConfigError(f"Invalid Anyang user configuration: {target}") from exc
    if set(value) != {"version", "data_dir", "choice"}:
        raise LedgerConfigError("Anyang user configuration has unknown or missing fields")
    if value.get("version") != CONFIG_VERSION:
        raise LedgerConfigError(f"Unsupported Anyang user configuration version: {value.get('version')}")
    data_dir = _absolute_path(value.get("data_dir"), "data_dir")
    choice = value.get("choice")
    if not isinstance(choice, dict) or set(choice) != set(CHOICE_SCOPE):
        raise LedgerConfigError("Anyang choice configuration has unknown or missing fields")
    for key, expected in CHOICE_SCOPE.items():
        if choice.get(key) != expected:
            raise LedgerConfigError(f"Anyang choice configuration conflicts at {key}")
    return {"version": CONFIG_VERSION, "data_dir": str(data_dir), "choice": dict(CHOICE_SCOPE)}


def validate_external_data_dir(data_dir: str | Path, repo_root: str | Path) -> Path:
    raw = Path(data_dir).expanduser()
    if not raw.is_absolute():
        raise LedgerConfigError("Choice data directory must be an absolute external path")
    resolved = raw.resolve()
    repository = Path(repo_root).expanduser().resolve()
    if resolved == repository or resolved.is_relative_to(repository):
        raise LedgerConfigError("Choice data directory must remain outside the repository")
    _safe_string(str(resolved), "data_dir", maximum=1000)
    return resolved


def write_user_config(
    data_dir: str | Path,
    repo_root: str | Path,
    environ: Mapping[str, str] | None = None,
) -> Path:
    resolved = validate_external_data_dir(data_dir, repo_root)
    target = user_config_path(environ)
    if target == Path(repo_root).resolve() or target.is_relative_to(Path(repo_root).resolve()):
        raise LedgerConfigError("Anyang user configuration must remain outside the repository")
    target.parent.mkdir(parents=True, exist_ok=True)
    content = _render_config(resolved)
    temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(content, encoding="utf-8", newline="\n")
        try:
            temporary.chmod(0o600)
        except OSError:
            pass
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    return target


def clear_user_config(environ: Mapping[str, str] | None = None) -> tuple[Path, bool]:
    target = user_config_path(environ)
    existed = target.exists()
    if existed:
        target.unlink()
    return target, existed


def _render_config(data_dir: Path) -> str:
    values = [
        f"version = {CONFIG_VERSION}",
        f"data_dir = {json.dumps(str(data_dir))}",
        "",
        "[choice]",
    ]
    values.extend(f"{key} = {json.dumps(value)}" for key, value in CHOICE_SCOPE.items())
    return "\n".join(values) + "\n"


def _absolute_path(value: object, label: str) -> Path:
    if not isinstance(value, str):
        raise LedgerConfigError(f"Anyang user configuration {label} must be a string")
    _safe_string(value, label, maximum=1000)
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise LedgerConfigError(f"Anyang user configuration {label} must be absolute")
    return path.resolve()


def _safe_string(value: str, label: str, *, maximum: int) -> None:
    if not value or len(value) > maximum or any(ord(character) < 32 for character in value):
        raise LedgerConfigError(f"Invalid Anyang user configuration {label}")
