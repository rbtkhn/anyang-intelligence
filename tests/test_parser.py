from pathlib import Path

import pytest

from anyang_loop.parser import LoopParseError, discover_loop_files, parse_markdown, parse_yaml


def test_parse_yaml_loop():
    loop = parse_yaml(
        """
name: test-loop
signal: weekly review
memory_objects:
  - decision log
decision: prepare recommendation
action: owner approves next action
evidence: operating review record
cadence: weekly
learning_update: update memory with lesson
governance_boundary: human owner approval required
"""
    )
    assert loop.name == "test-loop"
    assert loop.memory_objects == ["decision log"]


def test_parse_markdown_front_matter():
    loop = parse_markdown(
        """---
name: frontmatter-loop
signal: event
memory_objects: [risk register]
decision: prepare options
action: human approves
evidence: approval record
cadence: event-driven
learning_update: preserve lesson in memory
governance_boundary: human approval required
---

# Body
"""
    )
    assert loop.name == "frontmatter-loop"
    assert loop.cadence == "event-driven"


def test_parse_markdown_headings():
    loop = parse_markdown(
        """# Heading Loop

## Signal
Weekly signal.

## Memory Objects
- decision log
- risk register

## Decision
Prepare options.

## Action
Owner approves action.

## Evidence
Approval record.

## Cadence
Weekly.

## Learning Update
Update memory.

## Governance Boundary
Human approval required.
""",
        "heading-loop.md",
    )
    assert loop.name == "Heading Loop"
    assert "decision log" in loop.memory_objects


def test_parse_markdown_malformed_front_matter_falls_back_to_headings():
    loop = parse_markdown(
        """---
title: Non-loop source note
...
lane: singularity-science
---

# Recovered Loop

## Signal
Weekly signal.

## Memory Objects
- decision log

## Decision
Prepare options.

## Action
Owner approves action.

## Evidence
Approval record.

## Cadence
Weekly.

## Learning Update
Update memory.

## Governance Boundary
Human approval required.
"""
    )
    assert loop.name == "Recovered Loop"


def test_parse_markdown_malformed_front_matter_without_loop_shape_is_parse_error():
    with pytest.raises(LoopParseError):
        parse_markdown(
            """---
title: Non-loop source note
...
lane: singularity-science
---

# Source Note
"""
        )


def test_discover_loop_files_skips_non_loop_catalog_yaml(tmp_path):
    catalog = tmp_path / "projects" / "learning-core" / "catalog"
    loops = tmp_path / "projects" / "learning-core" / "loop-examples"
    catalog.mkdir(parents=True)
    loops.mkdir(parents=True)
    (catalog / "khan-catalog-manifest.sample.yaml").write_text("catalog_entries: []\n", encoding="utf-8")
    loop_file = loops / "parent-intake-readiness.yaml"
    loop_file.write_text(
        """
name: parent-intake-readiness
signal: parent response
memory_objects: [parent intake]
decision: classify readiness
action: draft, hold, or ask for missing input
evidence: readiness record
cadence: event-driven
learning_update: update intake checklist
governance_boundary: parent approval required
""",
        encoding="utf-8",
    )

    discovered = discover_loop_files(tmp_path / "projects")

    assert discovered == [loop_file]


def test_project_examples_parse():
    root = Path(__file__).resolve().parents[1]
    examples = list(root.glob("projects/*/loop-examples/*.yaml"))
    assert examples
    for path in examples:
        loop = parse_yaml(path.read_text(encoding="utf-8"), str(path))
        assert loop.name
