from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import re

from .artifact_state import repository_root


STALE_TERMS = {
    "engineer-operator-owner": "engineer",
    "ai-ceo": "executive",
    "hannah": "interface",
    "client-human-ceo": "client",
}


@dataclass(frozen=True)
class AuthorityFinding:
    path: str
    line: int
    classification: str
    text: str
    recommendation: str
    safe_to_rewrite: bool


def inventory_authority(root: str | Path | None = None) -> list[AuthorityFinding]:
    base = Path(root or repository_root()).resolve()
    findings: list[AuthorityFinding] = []
    for path in sorted(base.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in {".md", ".yaml", ".yml", ".py", ".json"}:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for number, line in enumerate(lines, 1):
            lowered = line.casefold()
            for stale, canonical in STALE_TERMS.items():
                if stale in lowered:
                    findings.append(AuthorityFinding(
                        path.relative_to(base).as_posix(), number, "stale-term", line.strip(),
                        f"Use '{canonical}' in new records; retain only as a migration alias.", False,
                    ))
            if re.search(r"access.{0,30}authority|authority.{0,30}access", lowered):
                findings.append(AuthorityFinding(
                    path.relative_to(base).as_posix(), number, "authority-warning", line.strip(),
                    "Confirm that access does not imply authority and name the approval gate.", False,
                ))
    return findings


def render_inventory(findings: list[AuthorityFinding], fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps([asdict(item) for item in findings], indent=2, sort_keys=True)
    if not findings:
        return "OK authority inventory: no findings\n"
    lines = [f"Authority inventory: {len(findings)} findings"]
    lines.extend(f"- {item.path}:{item.line} [{item.classification}] {item.recommendation}" for item in findings)
    return "\n".join(lines) + "\n"
