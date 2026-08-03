from pathlib import Path

from anyang_loop.parser import load_loop_file
from anyang_loop.project_validate import validate_project_path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/game-design"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalized(path: Path) -> str:
    return " ".join(read(path).split())


def test_game_design_project_is_a_complete_inactive_installation():
    results = validate_project_path(PROJECT)
    assert len(results) == 1
    assert results[0].ok, results[0].errors
    assert not results[0].warnings

    charter = normalized(PROJECT / "README.md").lower()
    install = normalized(PROJECT / "executive-os-install.md").lower()
    assert "provisional internal capability lane" in charter
    assert "named game: none" in charter
    assert "budget and spend authority: `$0`" in charter
    assert "activation status | held" in install
    assert "if any required field is unknown" in install
    assert "preserve it as `missing`" in install


def test_game_design_project_preserves_authorship_and_action_boundaries():
    install = normalized(PROJECT / "executive-os-install.md").lower()
    risks = normalized(PROJECT / "risk-register.md").lower()
    review = normalized(PROJECT / "operating-review.md").lower()
    for phrase in (
        "robert is the aspiring designer and creative authority",
        "recommendation is not selection",
        "may not, by implication",
        "artifact count, code volume, and apparent polish are not success measures",
    ):
        assert phrase in install
    assert "agent steals authorship" in risks
    assert "imagined fun becomes fact" in risks
    assert "candidate human lesson" in review
    assert "candidate agent lesson" in review


def test_game_design_membrane_keeps_adjacent_lanes_separate():
    membrane = normalized(PROJECT / "membrane-notes.md").lower()
    for phrase in (
        "transfer primitives, not private context",
        "media production",
        "system engineering",
        "singularity science",
        "learning core",
        "learner and family facts never cross",
        "when provenance, consent, evidence, sensitivity, or authority is uncertain",
    ):
        assert phrase in membrane
    assert "[game design](game-design/readme.md)" in read(
        ROOT / "projects/README.md"
    ).lower()


def test_game_design_loops_are_bounded_and_machine_valid():
    loop_paths = sorted((PROJECT / "loop-examples").glob("*.yaml"))
    assert len(loop_paths) == 3
    loops = [load_loop_file(path) for path in loop_paths]
    assert {loop.loop_type for loop in loops} == {"operating", "governance", "learning"}
    assert {loop.project_lane for loop in loops} == {"game-design"}
    for loop in loops:
        assert loop.evidence
        assert loop.cadence
        assert loop.learning_update
        assert "authority" in loop.governance_boundary.lower() or "approval" in loop.governance_boundary.lower()
