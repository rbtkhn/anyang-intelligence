from pathlib import Path
import tempfile

from anyang_loop.install_cli import main
from anyang_loop.transcript_import import import_transcripts, render_completion_report


def write_manifest(path: Path, transcript_a: Path, transcript_b: Path) -> Path:
    manifest = path / "customers" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "{\n"
        '  "transcripts": [\n'
        "    {\n"
        '      "lane": "innermost-loop",\n'
        '      "title": "First Innermost Loop",\n'
        '      "slug": "first-innermost-loop",\n'
        '      "date_captured": "2026-07-08",\n'
        f'      "source_ref": "https://example.com/innermost/{transcript_a.stem}",\n'
        '      "rights_status": "internal-commit-approved",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript_a.as_posix()}"\n'
        "    },\n"
        "    {\n"
        '      "lane": "moonshots",\n'
        '      "title": "First Moonshots",\n'
        '      "slug": "first-moonshots",\n'
        '      "date_captured": "2026-07-08",\n'
        f'      "source_ref": "https://example.com/moonshots/{transcript_b.stem}",\n'
        '      "rights_status": "internal-commit-approved",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript_b.as_posix()}"\n'
        "    },\n"
        "    {\n"
        '      "lane": "moonshots",\n'
        '      "title": "Rights Hold Moonshots",\n'
        '      "slug": "rights-hold-moonshots",\n'
        '      "date_captured": "2026-07-08",\n'
        '      "source_ref": "https://example.com/moonshots/hold",\n'
        '      "rights_status": "uncertain-review-needed",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript_b.as_posix()}"\n'
        "    },\n"
        "    {\n"
        '      "lane": "innermost-loop",\n'
        '      "title": "Missing Source",\n'
        '      "slug": "missing-source",\n'
        '      "date_captured": "2026-07-08",\n'
        '      "source_ref": "https://example.com/innermost/missing",\n'
        '      "rights_status": "internal-commit-approved",\n'
        '      "capture_method": "manual export",\n'
        '      "local_input_path": "C:/missing/missing-source.txt"\n'
        "    },\n"
        "    {\n"
        '      "lane": "moonshots",\n'
        '      "title": "Skip This",\n'
        '      "slug": "skip-this",\n'
        '      "date_captured": "2026-07-08",\n'
        '      "source_ref": "https://example.com/moonshots/skip",\n'
        '      "rights_status": "do-not-commit",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript_b.as_posix()}"\n'
        "    }\n"
        "  ]\n"
        "}\n",
        encoding="utf-8",
    )
    return manifest


def test_transcript_import_dry_run_and_report():
    tmp_path = Path(tempfile.mkdtemp())
    transcript_a = tmp_path / "first-innermost.txt"
    transcript_b = tmp_path / "first-moonshots.txt"
    transcript_a.write_text("Innermost transcript body.", encoding="utf-8")
    transcript_b.write_text("Moonshots transcript body.", encoding="utf-8")
    manifest = write_manifest(tmp_path, transcript_a, transcript_b)

    assert main(["import-transcripts", "--manifest", str(manifest), "--dry-run"]) == 1
    assert not (manifest.parent / "innermost-loop" / "transcripts" / "2026-07-08-captured-first-innermost-loop.md").exists()

    report = render_completion_report(import_transcripts(manifest, dry_run=True))
    assert "Blocked rights-review items: 1" in report
    assert "Missing source files: 1" in report
    assert "| innermost-loop | 2 | 1 | 0 | 1 | 50% |" in report
    assert "| moonshots | 3 | 1 | 1 | 0 | 33% |" in report


def test_transcript_import_writes_files_and_ledger():
    tmp_path = Path(tempfile.mkdtemp())
    transcript_a = tmp_path / "first-innermost.txt"
    transcript_b = tmp_path / "first-moonshots.txt"
    transcript_a.write_text("Innermost transcript body.", encoding="utf-8")
    transcript_b.write_text("Moonshots transcript body.", encoding="utf-8")
    manifest = write_manifest(tmp_path, transcript_a, transcript_b)

    assert main(["import-transcripts", "--manifest", str(manifest)]) == 1

    innermost = manifest.parent / "innermost-loop" / "transcripts" / "2026-07-08-captured-first-innermost-loop.md"
    moonshots = manifest.parent / "moonshots" / "transcripts" / "2026-07-08-captured-first-moonshots.md"
    ledger = manifest.parent / "transcript-import-ledger.md"

    assert innermost.exists()
    assert moonshots.exists()
    assert ledger.exists()

    innermost_text = innermost.read_text(encoding="utf-8")
    assert "rights_status: internal-commit-approved" in innermost_text
    assert "## Transcript" in innermost_text
    assert "Innermost transcript body." in innermost_text
    front_matter = innermost_text.split("---", 2)[1]
    assert "\n...\n" not in front_matter

    ledger_text = ledger.read_text(encoding="utf-8")
    assert "needs-source-note" in ledger_text
    assert "blocked-rights" in ledger_text
    assert "missing-source" in ledger_text
    assert "skipped-do-not-commit" in ledger_text


def test_transcript_import_duplicate_detection_and_no_overwrite():
    tmp_path = Path(tempfile.mkdtemp())
    transcript = tmp_path / "first-innermost.txt"
    transcript.write_text("First transcript body.", encoding="utf-8")
    manifest = tmp_path / "customers" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "{\n"
        '  "transcripts": [\n'
        "    {\n"
        '      "lane": "innermost-loop",\n'
        '      "title": "First Innermost Loop",\n'
        '      "slug": "first-innermost-loop",\n'
        '      "date_captured": "2026-07-08",\n'
        '      "source_ref": "https://example.com/innermost/first",\n'
        '      "rights_status": "internal-commit-approved",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript.as_posix()}"\n'
        "    }\n"
        "  ]\n"
        "}\n",
        encoding="utf-8",
    )

    assert main(["import-transcripts", "--manifest", str(manifest)]) == 0
    imported = manifest.parent / "innermost-loop" / "transcripts" / "2026-07-08-captured-first-innermost-loop.md"
    original_text = imported.read_text(encoding="utf-8")

    transcript.write_text("Updated transcript body that should not overwrite.", encoding="utf-8")
    assert main(["import-transcripts", "--manifest", str(manifest)]) == 0
    assert imported.read_text(encoding="utf-8") == original_text


def test_transcript_import_validation_failures(capsys):
    tmp_path = Path(tempfile.mkdtemp())
    transcript = tmp_path / "blank.txt"
    transcript.write_text("   \n", encoding="utf-8")
    manifest = tmp_path / "customers" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "{\n"
        '  "transcripts": [\n'
        "    {\n"
        '      "lane": "invalid-lane",\n'
        '      "title": "Invalid Lane",\n'
        '      "slug": "invalid-lane",\n'
        '      "date_captured": "2026-07-08",\n'
        '      "source_ref": "https://example.com/invalid",\n'
        '      "rights_status": "internal-commit-approved",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript.as_posix()}"\n'
        "    },\n"
        "    {\n"
        '      "lane": "moonshots",\n'
        '      "title": "Missing Slug",\n'
        '      "slug": "",\n'
        '      "date_captured": "2026-07-08",\n'
        '      "source_ref": "https://example.com/missing-slug",\n'
        '      "rights_status": "internal-commit-approved",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript.as_posix()}"\n'
        "    },\n"
        "    {\n"
        '      "lane": "moonshots",\n'
        '      "title": "Missing Rights",\n'
        '      "slug": "missing-rights",\n'
        '      "date_captured": "2026-07-08",\n'
        '      "source_ref": "https://example.com/missing-rights",\n'
        '      "rights_status": "",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript.as_posix()}"\n'
        "    },\n"
        "    {\n"
        '      "lane": "moonshots",\n'
        '      "title": "Blank Body",\n'
        '      "slug": "blank-body",\n'
        '      "date_captured": "2026-07-08",\n'
        '      "source_ref": "https://example.com/blank-body",\n'
        '      "rights_status": "internal-commit-approved",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript.as_posix()}"\n'
        "    }\n"
        "  ]\n"
        "}\n",
        encoding="utf-8",
    )

    assert main(["import-transcripts", "--manifest", str(manifest)]) == 1
    captured = capsys.readouterr()
    assert "Invalid lane: invalid-lane." in captured.out
    assert "Missing required fields: slug." in captured.out
    assert "Missing required fields: rights_status." in captured.out
    assert "Transcript body is empty after normalization" in captured.out
