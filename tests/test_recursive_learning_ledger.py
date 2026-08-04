import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "os" / "recursive-learning-ledger.md"
ID_PATTERN = re.compile(r"RL-\d{4}-\d{3}")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ALLOWED_STATES = {
    "candidate",
    "approved",
    "implemented",
    "validated",
    "observed",
    "deferred",
    "rejected",
    "superseded",
}
LEDGER_HEADER = [
    "ID",
    "Opened",
    "Signal",
    "Learning",
    "Decision and authority",
    "Durable surface",
    "Evidence and validation",
    "Outcome or revisit",
    "State",
]
MEASUREMENT_HEADER = [
    "ID",
    "Primary outcome question",
    "Measures and initial threshold",
    "Revisit trigger",
]


def _section(content: str, start: str, end: str) -> str:
    assert start in content
    assert end in content
    return content.split(start, 1)[1].split(end, 1)[0]


def _cells(line: str) -> list[str]:
    assert line.startswith("|") and line.endswith("|")
    return [cell.strip() for cell in line[1:-1].split("|")]


def _rows(section: str) -> list[list[str]]:
    return [_cells(line) for line in section.splitlines() if line.startswith("| RL-")]


def test_canonical_ledger_rows_have_stable_unique_schema_and_states():
    content = LEDGER.read_text(encoding="utf-8")
    section = _section(content, "## Ledger", "## Outcome Measurement Protocol")
    header = next(_cells(line) for line in section.splitlines() if line.startswith("| ID |"))
    rows = _rows(section)

    assert header == LEDGER_HEADER
    assert rows
    assert all(len(row) == len(LEDGER_HEADER) for row in rows)

    ids = [row[0] for row in rows]
    assert len(ids) == len(set(ids))
    assert all(ID_PATTERN.fullmatch(learning_id) for learning_id in ids)
    assert all(row[-1] in ALLOWED_STATES for row in rows)
    assert all(date.fromisoformat(row[1]) for row in rows)
    assert all(row[4] for row in rows)


def test_measurements_reference_unique_canonical_learning_ids():
    content = LEDGER.read_text(encoding="utf-8")
    ledger_section = _section(content, "## Ledger", "## Outcome Measurement Protocol")
    measurement_section = _section(content, "## Outcome Measurement Protocol", "## Update Rules")
    header = next(
        _cells(line) for line in measurement_section.splitlines() if line.startswith("| ID |")
    )
    canonical_ids = {row[0] for row in _rows(ledger_section)}
    measurement_ids = [row[0] for row in _rows(measurement_section)]

    assert header == MEASUREMENT_HEADER
    assert measurement_ids
    assert len(measurement_ids) == len(set(measurement_ids))
    assert set(measurement_ids) <= canonical_ids


def test_relative_evidence_links_resolve_inside_repository():
    content = LEDGER.read_text(encoding="utf-8")
    repository_root = ROOT.resolve()

    for match in LINK_PATTERN.finditer(content):
        target = match.group(1).strip("<>").split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        resolved = (LEDGER.parent / target).resolve()
        assert resolved.is_relative_to(repository_root), f"Link escapes repository: {target}"
        assert resolved.exists(), f"Missing ledger link: {target}"
