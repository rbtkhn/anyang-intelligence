from pathlib import Path
import tempfile

from anyang_loop.install_cli import main
from anyang_loop.install_model import load_install_input
from anyang_loop.install_render import build_customer_files
from anyang_loop.install_validate import validate_install_path
from anyang_loop.membrane import classify_text, extract_patterns
from anyang_loop.parser import parse_yaml


def example_input_path() -> Path:
    return Path(__file__).resolve().parents[1] / "templates" / "customer-install" / "input-example.yaml"


def test_load_install_input():
    spec = load_install_input(example_input_path())
    assert spec.slug == "example-customer"
    assert "Operating context" in spec.context_map


def test_build_customer_files_contains_required_scaffold():
    spec = load_install_input(example_input_path())
    files = build_customer_files(spec)
    for name in (
        "README.md",
        "executive-os-install.md",
        "risk-register.md",
        "decision-log.md",
        "operating-review.md",
        "30-day-plan.md",
        "membrane-notes.md",
    ):
        assert name in files
    loop_files = [name for name in files if name.startswith("loop-examples/")]
    assert len(loop_files) == 3
    for name in loop_files:
        loop = parse_yaml(files[name], name)
        assert loop.customer_lane == "example-customer"


def test_cli_new_validate_and_overwrite_protection():
    output = Path(tempfile.mkdtemp()) / "example-customer"
    assert main(["new", str(example_input_path()), "--output", str(output)]) == 0
    assert (output / "executive-os-install.md").exists()
    assert main(["new", str(example_input_path()), "--output", str(output)]) == 1
    assert main(["validate", str(output)]) == 0


def test_render_formats():
    tmp_path = Path(tempfile.mkdtemp())
    markdown = tmp_path / "markdown"
    obsidian = tmp_path / "obsidian"
    html = tmp_path / "html"
    assert main(["render", str(example_input_path()), "--format", "markdown", "--output", str(markdown)]) == 0
    assert main(["render", str(example_input_path()), "--format", "obsidian", "--output", str(obsidian)]) == 0
    assert main(["render", str(example_input_path()), "--format", "html", "--output", str(html)]) == 0
    assert (markdown / "README.md").exists()
    assert (obsidian / "Index.md").exists()
    assert (html / "index.html").exists()


def test_validate_incomplete_customer_fails():
    tmp_path = Path(tempfile.mkdtemp())
    customer = tmp_path / "thin"
    customer.mkdir()
    (customer / "README.md").write_text("# Thin\n", encoding="utf-8")
    results = validate_install_path(customer)
    assert results[0].errors


def test_membrane_classification_sensitive_terms():
    classification, reason, approval = classify_text("Private customer pricing and tax review")
    assert classification in {"approval required", "professional review required", "keep local"}
    assert reason
    assert approval


def test_extract_patterns_from_customers():
    root = Path(__file__).resolve().parents[1]
    candidates = extract_patterns(root / "customers")
    assert candidates
    assert any("review" in candidate.transfer_candidate.lower() for candidate in candidates)


def test_cli_extract_patterns():
    tmp_path = Path(tempfile.mkdtemp())
    root = Path(__file__).resolve().parents[1]
    output = tmp_path / "patterns.md"
    assert main(["extract-patterns", str(root / "customers"), "--output", str(output)]) == 0
    text = output.read_text(encoding="utf-8")
    assert "Membrane classification" in text
