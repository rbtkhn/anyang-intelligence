from pathlib import Path

from anyang_loop.authority_inventory import inventory_authority, render_inventory


def test_inventory_is_read_only_and_reports_stale_terms(tmp_path: Path):
    source = tmp_path / "sample.md"
    source.write_text("The ai-ceo directs Hannah.\n", encoding="utf-8")
    findings = inventory_authority(tmp_path)
    assert len(findings) == 2
    assert all(item.classification == "stale-term" for item in findings)
    assert source.read_text(encoding="utf-8") == "The ai-ceo directs Hannah.\n"


def test_inventory_json_is_reviewable(tmp_path: Path):
    (tmp_path / "sample.md").write_text("Access does not imply authority.\n", encoding="utf-8")
    output = render_inventory(inventory_authority(tmp_path), "json")
    assert "authority-warning" in output
