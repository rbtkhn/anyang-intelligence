from pathlib import Path

from anyang_loop.context_audit import audit_repository, render_markdown, write_audit


def test_audit_detects_broken_links_and_is_deterministic(tmp_path):
    (tmp_path / "README.md").write_text("[missing](missing.md)\n", encoding="utf-8")
    first = audit_repository(tmp_path)
    second = audit_repository(tmp_path)
    assert first == second
    assert any(item["category"] == "broken-link" for item in first["findings"])


def test_archive_transcripts_and_gitkeep_are_not_membrane_or_orphan_findings(tmp_path):
    transcript = tmp_path / "operating-substrate/projects/singularity-science/archive/x/transcripts"
    transcript.mkdir(parents=True)
    (transcript / ".gitkeep").write_text("", encoding="utf-8")
    (transcript / "source-transcript.md").write_text("source", encoding="utf-8")
    report = audit_repository(tmp_path)
    categories = {item["category"] for item in report["findings"]}
    assert "membrane-boundary" not in categories


def test_archive_linkage_is_reported(tmp_path):
    transcripts = tmp_path / "operating-substrate/projects/singularity-science/archive/x/transcripts"
    transcripts.mkdir(parents=True)
    (transcripts / "2026-01-01-example.md").write_text("source", encoding="utf-8")
    report = audit_repository(tmp_path)
    assert any(item["category"] == "archive-linkage" for item in report["findings"])


def test_authority_conflict_is_reported(tmp_path):
    (tmp_path / "grant.md").write_text("This grants authority to publish.\n", encoding="utf-8")
    (tmp_path / "limit.md").write_text("This never grants authority.\n", encoding="utf-8")
    report = audit_repository(tmp_path)
    assert any(item["category"] == "authority-conflict" for item in report["findings"])


def test_authority_document_without_freshness_metadata_is_reported(tmp_path):
    (tmp_path / "authority.md").write_text("Permission and approval rules for publication.\n", encoding="utf-8")
    report = audit_repository(tmp_path)
    assert any(item["category"] == "freshness-metadata" for item in report["findings"])


def test_markdown_and_json_views_share_findings(tmp_path):
    (tmp_path / "README.md").write_text("[missing](missing.md)\n", encoding="utf-8")
    report = audit_repository(tmp_path)
    markdown = render_markdown(report)
    assert report["findings"][0]["finding_id"] in markdown
    assert report["counts"]["error"] == 1


def test_audit_findings_do_not_fail_and_do_not_mutate(tmp_path):
    source = tmp_path / "README.md"
    source.write_text("[missing](missing.md)\n", encoding="utf-8")
    before = source.read_bytes()
    report = audit_repository(tmp_path)
    assert report["read_only"] is True
    assert source.read_bytes() == before


def test_audit_output_can_be_written(tmp_path):
    output = tmp_path / "audit.json"
    write_audit(tmp_path, output, "json")
    assert output.exists()
