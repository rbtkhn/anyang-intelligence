from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/executive-council-singularity-science-interface-contract.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_singularity_interface_contract_is_adopted_without_operational_authority():
    text = normalized(CONTRACT)
    for phrase in (
        "Status:",
        "`adopted",
        "durable interface only; no standing mandate or operational authority created",
        "creates no Council role, runtime, operational authority, persistence, publication",
        "customer action, commercial offer, or standing mandate",
        "This adopted interface contract is not itself a standing mandate",
        "No general standing mandate should be inferred",
    ):
        assert phrase in text


def test_singularity_interface_preserves_tasking_and_authority_roles():
    text = normalized(CONTRACT)
    for phrase in (
        "Singularity Science investigates",
        "Executive Council integrates and recommends",
        "The System Engineer decides what may proceed",
        "The normal tasker of Singularity Science is the Chief Executive",
        "request a question != task the lane != approve execution != adopt the result",
        "Audit provenance and claimed state",
        "Independently activated Council Steward",
        "Communicate externally",
        "Executive Assistant under an approved dispatch",
    ):
        assert phrase in text


def test_singularity_interface_keeps_state_namespaces_distinct():
    text = normalized(CONTRACT)
    for phrase in (
        "Every state-bearing handoff must name its state namespace",
        "source-progression state",
        "retention status",
        "lane ROI disposition",
        "recurrence disposition",
        "None of these labels authorizes testing, installation, publication",
        "System Engineer approval does not create client-company",
    ):
        assert phrase in text


def test_singularity_interface_requires_membrane_and_ongoing_review():
    text = normalized(CONTRACT)
    for phrase in (
        "transcript bulk and long quotations",
        "remain inside Singularity Science unless separately reviewed",
        "Cross-project transfer requires a reusable abstraction",
        "Adoption evidence and ongoing review gate",
        "EC-SS-INTERFACE-ADOPTION-2026-08-05-01",
        "explicit decision not to create a standing mandate",
        "cannot expand authority, renew a standing mandate, or adopt research automatically",
    ):
        assert phrase in text
