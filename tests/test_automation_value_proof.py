from pathlib import Path

from anyang_loop.automation_value_proof import validate_value_proof_text


VALID = """# Automation Value Proof

- Recurring constraint: Weekly documentation review is repetitive.
- Baseline measurement: Four hours across four representative weekly runs.
- Target metric: Reduce preparation time without increasing revisions.
- Approved inputs and tools: Public repo Markdown and approved local validator.
- Human owner: Repository operator.
- Approval boundary: Human approval required before merge or publication.
- Representative test cases: Four prior weekly packets and one malformed packet.
- Exception behavior: Hold and report malformed or ambiguous inputs.
- Before/after evidence: Four runs reduced preparation from 4 hours to 2 hours with no revision increase.
- Review burden: 20 minutes per run.
- Unresolved uncertainty: Long-term maintenance burden is not yet known.
- Completion receipt: RECEIPT-001 with links to sanitized run records.
"""


def test_valid_value_proof_passes():
    assert validate_value_proof_text(VALID) == []


def test_missing_baseline_and_target_metric_fail():
    text = VALID.replace("- Baseline measurement: Four hours across four representative weekly runs.\n", "")
    text = text.replace("- Target metric: Reduce preparation time without increasing revisions.\n", "")
    codes = {item.code for item in validate_value_proof_text(text)}
    assert {"missing-baseline", "missing-target-metric"} <= codes


def test_quantitative_claim_without_evidence_fails():
    text = VALID.replace("- Baseline measurement: Four hours across four representative weekly runs.\n", "- Baseline measurement: [fill]\n")
    codes = {item.code for item in validate_value_proof_text(text)}
    assert "unsupported-quantitative-claim" in codes


def test_private_path_fails():
    text = VALID.replace("- Approved inputs and tools:", "- Approved inputs and tools: tenant-private/customer.db and approved local validator\n- Approved inputs and tools:")
    codes = {item.code for item in validate_value_proof_text(text)}
    assert "private-data-route" in codes


def test_human_judgment_is_not_validated_as_a_boolean():
    text = VALID.replace("- Approval boundary: Human approval required before merge or publication.", "- Approval boundary: Human review decides whether the work is valuable and ready.")
    assert validate_value_proof_text(text) == []


def test_template_is_repo_visible():
    assert Path("templates/automation-value-proof.md").exists()

