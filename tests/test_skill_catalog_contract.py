from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CATALOG = SKILLS / "README.md"
CATALOG_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+/SKILL\.md)\)")


def canonical_skill_paths() -> list[Path]:
    return sorted(SKILLS.rglob("SKILL.md"))


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert text.startswith("---\n"), path.relative_to(ROOT).as_posix()
    end = text.find("\n---", 4)
    assert end >= 0, path.relative_to(ROOT).as_posix()
    metadata = yaml.safe_load(text[4:end]) or {}
    assert isinstance(metadata, dict), path.relative_to(ROOT).as_posix()
    return metadata


def test_every_canonical_skill_has_unique_discovery_metadata() -> None:
    declared_names: list[str] = []
    for path in canonical_skill_paths():
        metadata = frontmatter(path)
        name = metadata.get("name")
        description = metadata.get("description")
        assert isinstance(name, str) and name.strip(), path.relative_to(ROOT).as_posix()
        assert isinstance(description, str) and description.strip(), path.relative_to(ROOT).as_posix()
        declared_names.append(name.strip())

    duplicates = sorted(name for name, count in Counter(declared_names).items() if count > 1)
    assert duplicates == []


def test_catalog_links_every_canonical_skill_exactly_once() -> None:
    catalog_text = CATALOG.read_text(encoding="utf-8")
    targets = CATALOG_LINK_RE.findall(catalog_text)
    counts = Counter(targets)
    duplicates = sorted(target for target, count in counts.items() if count > 1)
    assert duplicates == []

    canonical = {
        path.relative_to(SKILLS).as_posix()
        for path in canonical_skill_paths()
    }
    assert set(targets) == canonical
    assert len(targets) == len(canonical)

    for target in targets:
        resolved = SKILLS / target
        assert resolved.is_file(), target
