from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILL = ROOT / "skills/student-operating-system/learner-intake/SKILL.md"
CLICKABLE_CARDS = (
    ROOT
    / "skills/student-operating-system/learner-intake/references/clickable-create-cards.md"
)
DISCOVERY_ADAPTER = ROOT / ".agents/skills/learner-intake/SKILL.md"


def test_learner_intake_and_clickable_cards_are_discoverable():
    adapter = DISCOVERY_ADAPTER.read_text(encoding="utf-8")
    skill = CANONICAL_SKILL.read_text(encoding="utf-8")

    assert "skills/student-operating-system/learner-intake/SKILL.md" in adapter
    assert "references/clickable-create-cards.md" in skill
    assert CLICKABLE_CARDS.is_file()


def test_first_native_batch_obeys_control_limits():
    cards = CLICKABLE_CARDS.read_text(encoding="utf-8")

    assert "at most three questions per batch" in cards
    assert "two or three mutually exclusive choices per question" in cards
    assert "R1-A, R2-A, and R3-P1" in cards
    assert "`More choices` is navigation only" in cards
    assert "Learner increasingly carries choices" in cards
    assert "`Select` / `Do not select`" in cards
    assert "record the corresponding `Nothing named` answer" in cards
