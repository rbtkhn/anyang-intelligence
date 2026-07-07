from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .model import FIELD_ALIASES, LoopDefinition, normalize_field_name


class LoopParseError(ValueError):
    """Raised when a file cannot be parsed as a loop definition."""


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


def load_loop_file(path: str | Path) -> LoopDefinition:
    source = Path(path)
    text = source.read_text(encoding="utf-8")
    suffix = source.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return parse_yaml(text, str(source))
    if suffix == ".md":
        return parse_markdown(text, str(source))
    raise LoopParseError(f"Unsupported file type: {source}")


def discover_loop_files(path: str | Path) -> list[Path]:
    root = Path(path)
    if root.is_file():
        return [root]
    files: list[Path] = []
    for pattern in ("*.yaml", "*.yml", "*.md"):
        files.extend(root.rglob(pattern))
    return sorted(files)


def load_loops_from_path(path: str | Path) -> tuple[list[LoopDefinition], list[tuple[Path, str]]]:
    root = Path(path)
    loops: list[LoopDefinition] = []
    errors: list[tuple[Path, str]] = []
    for file_path in discover_loop_files(root):
        try:
            loop = load_loop_file(file_path)
        except LoopParseError as exc:
            if root.is_file():
                errors.append((file_path, str(exc)))
            continue
        loops.append(loop)
    return loops, errors


def parse_yaml(text: str, source_path: str = "") -> LoopDefinition:
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise LoopParseError("YAML loop definition must be a mapping.")
    if isinstance(data.get("loop"), dict):
        data = data["loop"]
    return LoopDefinition.from_mapping(data, source_path)


def parse_markdown(text: str, source_path: str = "") -> LoopDefinition:
    front_matter = FRONT_MATTER_RE.match(text)
    if front_matter:
        data = yaml.safe_load(front_matter.group(1)) or {}
        if isinstance(data.get("loop"), dict):
            data = data["loop"]
        if has_loop_shape(data):
            return LoopDefinition.from_mapping(data, source_path)

    data = parse_markdown_sections(text)
    if not has_loop_shape(data):
        raise LoopParseError("Markdown file does not contain loop grammar headings or loop front matter.")
    return LoopDefinition.from_mapping(data, source_path)


def parse_markdown_sections(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    current_lines: list[str] = []
    title = ""

    def flush() -> None:
        nonlocal current_key, current_lines
        if current_key:
            data[current_key] = "\n".join(current_lines).strip()
        current_key = None
        current_lines = []

    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            heading = match.group(2).strip().rstrip(":")
            if not title and match.group(1) == "#":
                title = heading
            normalized = normalize_field_name(heading)
            if normalized in FIELD_ALIASES.values():
                flush()
                current_key = normalized
                continue
            if current_key:
                flush()
            continue
        if current_key:
            current_lines.append(line)
    flush()
    if title:
        data.setdefault("name", title)
    return data


def has_loop_shape(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    normalized = {normalize_field_name(str(key)) for key in data.keys()}
    return "signal" in normalized and bool({"decision", "action", "evidence"} & normalized)
