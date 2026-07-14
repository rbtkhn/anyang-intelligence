from pathlib import Path
import tempfile

from anyang_loop.project_cli import main
from anyang_loop.phase_preflight import TRANSCRIPT_PHASE, run_preflight
from anyang_loop.transcript_import import TEMP_SUFFIX, import_transcripts, render_completion_report, temporary_path
from cadence_helpers import make_git_repo, run


def write_manifest(path: Path, transcript_a: Path, transcript_b: Path) -> Path:
    manifest = path / "projects" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
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
        '      "lane": "nate-b-jones",\n'
        '      "title": "First Nate B. Jones",\n'
        '      "slug": "first-nate-b-jones",\n'
        '      "date_captured": "2026-07-08",\n'
        f'      "source_ref": "https://example.com/nate-b-jones/{transcript_b.stem}",\n'
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
    make_git_repo(tmp_path)
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
    assert "| nate-b-jones | 1 | 1 | 0 | 0 | 100% |" in report


def test_transcript_import_blocks_all_writes_when_any_approved_source_is_missing():
    tmp_path = Path(tempfile.mkdtemp())
    make_git_repo(tmp_path)
    transcript_a = tmp_path / "first-innermost.txt"
    transcript_b = tmp_path / "first-moonshots.txt"
    transcript_a.write_text("Innermost transcript body.", encoding="utf-8")
    transcript_b.write_text("Moonshots transcript body.", encoding="utf-8")
    manifest = write_manifest(tmp_path, transcript_a, transcript_b)

    assert main(["import-transcripts", "--manifest", str(manifest)]) == 1

    innermost = manifest.parent / "innermost-loop" / "transcripts" / "2026-07-08-captured-first-innermost-loop.md"
    moonshots = manifest.parent / "moonshots" / "transcripts" / "2026-07-08-captured-first-moonshots.md"
    nate = manifest.parent / "nate-b-jones" / "transcripts" / "2026-07-08-captured-first-nate-b-jones.md"
    ledger = manifest.parent / "transcript-import-ledger.md"

    assert not innermost.exists()
    assert not moonshots.exists()
    assert not nate.exists()
    assert not ledger.exists()


def test_transcript_import_redacts_email_addresses():
    tmp_path = Path(tempfile.mkdtemp())
    make_git_repo(tmp_path)
    transcript = tmp_path / "email-transcript.txt"
    address = "person" + chr(64) + "example.com"
    transcript.write_text(f"Contact {address} for details.", encoding="utf-8")
    manifest = tmp_path / "projects" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "{\n"
        '  "transcripts": [\n'
        "    {\n"
        '      "lane": "innermost-loop",\n'
        '      "title": "Email Transcript",\n'
        '      "slug": "email-transcript",\n'
        '      "date_captured": "2026-07-08",\n'
        '      "source_ref": "https://example.com/email",\n'
        '      "rights_status": "internal-commit-approved",\n'
        '      "capture_method": "manual export",\n'
        f'      "local_input_path": "{transcript.as_posix()}"\n'
        "    }\n"
        "  ]\n"
        "}\n",
        encoding="utf-8",
    )

    assert main(["import-transcripts", "--manifest", str(manifest)]) == 0

    imported = manifest.parent / "innermost-loop" / "transcripts" / "2026-07-08-captured-email-transcript.md"
    imported_text = imported.read_text(encoding="utf-8")
    assert address not in imported_text
    assert "[redacted-email]" in imported_text
    ledger = manifest.parent / "transcript-import-ledger.md"
    assert ledger.exists()
    assert "Manifest: `projects/singularity-science/archive/transcript-intake-manifest.json`" in ledger.read_text(encoding="utf-8")


def test_transcript_import_duplicate_detection_and_no_overwrite():
    tmp_path = Path(tempfile.mkdtemp())
    make_git_repo(tmp_path)
    transcript = tmp_path / "first-innermost.txt"
    transcript.write_text("First transcript body.", encoding="utf-8")
    manifest = tmp_path / "projects" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
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
    assert main(["import-transcripts", "--manifest", str(manifest)]) == 1
    assert imported.read_text(encoding="utf-8") == original_text


def test_transcript_import_validation_failures(capsys):
    tmp_path = Path(tempfile.mkdtemp())
    make_git_repo(tmp_path)
    transcript = tmp_path / "blank.txt"
    transcript.write_text("   \n", encoding="utf-8")
    manifest = tmp_path / "projects" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
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


def test_rights_hold_does_not_block_independently_approved_row_and_json_transition(capsys):
    tmp_path = Path(tempfile.mkdtemp())
    make_git_repo(tmp_path)
    approved = tmp_path / "approved.txt"
    held = tmp_path / "held.txt"
    approved.write_text("Approved source.", encoding="utf-8")
    held.write_text("Held source.", encoding="utf-8")
    manifest = tmp_path / "projects" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        '{"transcripts": ['
        '{"lane":"moonshots","title":"Approved","slug":"approved","date_captured":"2026-07-13",'
        f'"source_ref":"internal","rights_status":"internal-commit-approved","capture_method":"manual","local_input_path":"{approved.as_posix()}"}},'
        '{"lane":"moonshots","title":"Held","slug":"held","date_captured":"2026-07-13",'
        f'"source_ref":"internal","rights_status":"uncertain-review-needed","capture_method":"manual","local_input_path":"{held.as_posix()}"}}]}}\n',
        encoding="utf-8",
    )
    run(tmp_path, "git", "add", ".")
    run(tmp_path, "git", "commit", "-m", "intake fixture")

    assert main(["import-transcripts", "--manifest", str(manifest), "--format", "json"]) == 0
    payload = __import__("json").loads(capsys.readouterr().out)

    assert (manifest.parent / "moonshots" / "transcripts" / "2026-07-13-captured-approved.md").exists()
    assert not (manifest.parent / "moonshots" / "transcripts" / "2026-07-13-captured-held.md").exists()
    assert [row["status"] for row in payload["import"]["rows"]] == ["imported", "blocked-rights"]
    assert payload["transition"]["baseline_fingerprint"]
    assert payload["transition"]["status"] == "pass"
    assert all(item["status"] == "pass" for item in payload["validation_results"])
    assert payload["handoff"]["authority"].startswith("advisory-only")


def test_mutation_rechecks_state_and_recovery_removes_bounded_temp_file():
    tmp_path = Path(tempfile.mkdtemp())
    make_git_repo(tmp_path)
    source = tmp_path / "source.txt"
    source.write_text("Stable source.", encoding="utf-8")
    manifest = tmp_path / "projects" / "singularity-science" / "archive" / "transcript-intake-manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        '{"transcripts":[{"lane":"innermost-loop","title":"Stable","slug":"stable","date_captured":"2026-07-13",'
        f'"source_ref":"internal","rights_status":"internal-commit-approved","capture_method":"manual","local_input_path":"{source.as_posix()}"}}]}}\n',
        encoding="utf-8",
    )
    run(tmp_path, "git", "add", ".")
    run(tmp_path, "git", "commit", "-m", "intake fixture")
    standalone = run_preflight(TRANSCRIPT_PHASE, manifest, repo_root=tmp_path)
    destination = standalone.summary.planned_destinations[0]
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(standalone.summary.results[0].expected_content, encoding="utf-8")
    temp = temporary_path(standalone.summary.ledger_path)
    temp.write_text("abandoned", encoding="utf-8")

    assert temp.name.endswith(TEMP_SUFFIX)
    assert main(["import-transcripts", "--manifest", str(manifest)]) == 0
    assert not temp.exists()
    assert standalone.summary.ledger_path.exists()

    destination.write_text("late conflicting state", encoding="utf-8")
    assert main(["import-transcripts", "--manifest", str(manifest)]) == 1
    assert destination.read_text(encoding="utf-8") == "late conflicting state"
