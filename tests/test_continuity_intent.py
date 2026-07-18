from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTENT = (
    "This substrate is intended to coordinate successive models and specialized agents "
    "into one continuous, owner-aligned intelligence across the operator's life, work, "
    "and projects."
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def test_continuity_intent_is_canonical_and_bounded():
    readme = read(ROOT / "README.md")
    architecture = read(ROOT / "docs/operating-substrate.md")
    related = [
        read(ROOT / "docs/thesis.md"),
        read(ROOT / "docs/product.md"),
        read(ROOT / "docs/artificial-enlightened-intelligence.md"),
        read(ROOT / "docs/governance.md"),
        read(ROOT / "docs/membranes.md"),
        read(ROOT / "docs/repository-anchored-bounded-agency.md"),
    ]

    assert INTENT in readme
    assert INTENT in architecture
    assert all(INTENT not in document for document in related)

    assert "continuity of purpose, memory, governance, and learning" in readme
    assert "does not claim continuous consciousness" in readme
    assert "collapse the membranes between projects" in readme
    assert "grant the system autonomous authority" in readme

    assert "continuity is architectural" in architecture
    assert "project membranes and legitimate human authority remain intact" in architecture


def test_two_offerings_share_a_substrate_without_collapsing_scope():
    readme = read(ROOT / "README.md")
    thesis = read(ROOT / "docs/thesis.md")
    product = read(ROOT / "docs/product.md")
    combined = readme + thesis + product

    assert "Personal AI Agent" in readme
    assert "Operational OS" in readme
    assert "emerging owner-facing continuity offering" in combined
    assert "first commercial wedge" in combined
    assert "founder-led" in combined
    assert "not yet represented as a production-mature autonomous agent" in product
    assert "facts, approvals, and authority remain membrane-separated" in readme


def test_agent_succession_preserves_governance_not_permission_drift():
    enlightened = read(ROOT / "docs/artificial-enlightened-intelligence.md")
    governance = read(ROOT / "docs/governance.md")
    membranes = read(ROOT / "docs/membranes.md")
    bounded = read(ROOT / "docs/repository-anchored-bounded-agency.md")

    assert "without pretending to be one continuous consciousness" in enlightened
    assert "unresolved uncertainty, and active holds" in enlightened
    assert "does not transfer unrecorded authority" in enlightened

    assert "does not preserve or create permission by implication" in governance
    assert "does not inherit unrecorded approval" in governance
    assert "reconstruct its live authority envelope" in governance

    assert "does not make project-local information globally available" in membranes
    assert "Continuity leak" in membranes
    assert "Model or agent succession does not widen that subset" in bounded
