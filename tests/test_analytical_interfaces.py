from pathlib import Path
import tempfile

import yaml

from anyang_loop.analytical_interfaces import GovernedDocument, validate_document, validate_manifest
from anyang_loop.project_cli import main
from anyang_loop.project_model import load_project_input
from anyang_loop.project_render import build_project_files


def codes(text: str, **options: bool) -> set[str]:
    document = GovernedDocument(path=Path("example.md"), **options)
    return {item.code for item in validate_document(text, document)}


def valid_document(extra: str = "") -> str:
    return f"""# When Queue Growth Outruns Worker Scaling

Title rationale: The title names the threshold that determines whether scaling remains reliable.

## Lead Judgment

Queue latency is rising because worker capacity now grows more slowly than incoming work.

## Controlling Object

Whether worker scaling can recover before latency breaches the service threshold.

{extra}

## Uncertainty

| Status and cause | Consequence | Evidence that would reduce it |
| --- | --- | --- |
| Uncertain—retry telemetry is incomplete | Keep the scaling decision reversible | Complete retry and worker saturation telemetry |
"""


def test_accepts_specific_argument_bearing_document():
    assert codes(valid_document()) == set()


def test_requires_exactly_one_h1_and_a_controlling_object():
    assert "h1-count" in codes(valid_document().replace("# When Queue Growth Outruns Worker Scaling\n", ""))
    assert "h1-count" in codes(valid_document() + "\n# A Second Title\n")
    assert "controlling-object" in codes(
        valid_document().replace(
            "Whether worker scaling can recover before latency breaches the service threshold.", "TBD"
        )
    )


def test_rejects_placeholder_and_administrative_titles():
    assert "placeholder-title" in codes(valid_document().replace("When Queue Growth Outruns Worker Scaling", "[Working title]"))
    assert "administrative-title" in codes(valid_document().replace("When Queue Growth Outruns Worker Scaling", "Report"))


def test_rejects_missing_or_trivial_title_rationale():
    assert "title-rationale" in codes(valid_document().replace("The title names the threshold that determines whether scaling remains reliable.", "TBD"))


def test_rejects_generic_analytical_heading():
    assert "generic-heading" in codes(valid_document("## Findings\n\nWorker saturation is the controlling mechanism."))


def test_forecast_requires_causal_and_resolution_fields():
    result = codes(valid_document("- Observable claim: Adoption rises next quarter."), require_forecast=True)
    assert "forecast-field" in result


def test_complete_forecast_passes():
    forecast = """
- Observable claim: Repeat use rises by quarter end.
- Causal mechanism: Guided setup removes first-session configuration abandonment.
- Time boundary: Resolve at the end of 2026 Q3.
- Strengthening evidence: Setup completion and repeat use rise together.
- Weakening evidence: Setup completion rises while repeat use stays flat.
- Resolution criteria: Compare authorized cohort completion and repeat-use telemetry.
- Principal alternative: Seasonal demand independently raises repeat use.
- Permitted unresolved state: Mark unresolved when authorized cohort telemetry is absent.
"""
    assert codes(valid_document(forecast), require_forecast=True) == set()


def test_deliberative_question_must_discriminate():
    assert "nondiscriminating-question" in codes(valid_document("What do we think?"), require_deliberative_questions=True)
    assert codes(
        valid_document("Does faster recovery reduce risk enough to justify losing local reversibility?"),
        require_deliberative_questions=True,
    ) == set()


def test_uncertainty_requires_cause_and_reduction_evidence():
    broken = valid_document().replace("Status and cause", "Status").replace("Evidence that would reduce it", "Notes")
    assert "uncertainty-cause" in codes(broken)


def test_manifest_exemption_preserves_provenance_surface():
    tmp_path = Path(tempfile.mkdtemp())
    archive = tmp_path / "archive" / "transcripts"
    archive.mkdir(parents=True)
    source = archive / "stable-source-title.md"
    original = "Imported source title without an H1\n"
    source.write_text(original, encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "documents": [{"path": "archive/transcripts/stable-source-title.md"}],
                "exemptions": ["archive/**"],
            }
        ),
        encoding="utf-8",
    )
    assert validate_manifest(manifest) == []
    assert source.name == "stable-source-title.md"
    assert source.read_text(encoding="utf-8") == original


def test_generated_operating_review_satisfies_template_contract():
    root = Path(__file__).resolve().parents[1]
    spec = load_project_input(root / "templates" / "project-install" / "input-example.yaml")
    review = build_project_files(spec)["operating-review.md"]
    document = GovernedDocument(
        path=Path("operating-review.md"), template=True, require_deliberative_questions=True
    )
    assert validate_document(review, document) == []


def test_default_manifest_and_cli_pass():
    assert validate_manifest() == []
    assert main(["validate-interfaces"]) == 0
