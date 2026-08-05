from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from anyang_loop.pattern_memory import (
    ELIGIBLE_LEARNING_STATES,
    MAX_CHARS_PER_RESULT,
    MAX_RESULTS,
    MAX_TOTAL_CHARS,
    PatternMemoryError,
    compile_corpus,
    query_pattern_memory,
    render_pattern_memory_json,
    render_pattern_memory_markdown,
    verify_source_reference,
    write_pattern_memory_report,
)
from anyang_loop.project_cli import main


ROOT = Path(__file__).resolve().parents[1]
REPLAY = ROOT / "tests" / "fixtures" / "pattern-memory-replay-v1.json"


def _run(repo: Path, *args: str) -> None:
    subprocess.run(list(args), cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def _row(learning_id: str, state: str, learning: str, *, signal: str = "Observed reusable work.") -> str:
    return (
        f"| {learning_id} | 2026-08-04 | {signal} | {learning} | Operator approved bounded review. "
        "| `docs/source.md` | [Evidence](../docs/source.md) | Outcome remains measured separately. "
        f"| {state} |"
    )


def _ledger(rows: list[str]) -> str:
    return "\n".join(
        [
            "# Recursive Learning Ledger",
            "",
            "## Ledger",
            "",
            "| ID | Opened | Signal | Learning | Decision and authority | Durable surface | Evidence and validation | Outcome or revisit | State |",
            "|---|---|---|---|---|---|---|---|---|",
            *rows,
            "",
            "## Outcome Measurement Protocol",
            "",
            "| ID | Question | Measure | Trigger |",
            "|---|---|---|---|",
            "| RL-2026-999 | Synthetic protocol row | None | Later |",
            "",
        ]
    )


def _fixture_repo(tmp_path: Path, *, long_learning: bool = False) -> Path:
    repo = tmp_path / "repo"
    (repo / "os").mkdir(parents=True)
    (repo / "docs").mkdir()
    (repo / "projects" / "alpha").mkdir(parents=True)
    (repo / "projects" / "tenant-private").mkdir(parents=True)
    (repo / "projects" / "alpha" / "archive").mkdir()
    learning = "Evidence-linked review patterns improve repeatable audit assurance."
    if long_learning:
        learning = "retrieval " + ("bounded evidence pattern " * 90)
    rows = [
        _row("RL-2026-001", "approved", learning),
        _row("RL-2026-002", "implemented", "Cadence reviews preserve source evidence."),
        _row("RL-2026-003", "validated", "Validation distinguishes structure from outcomes."),
        _row("RL-2026-004", "observed", "Observed reuse requires later outcome evidence."),
        _row("RL-2026-005", "candidate", "Candidate learning is not eligible."),
        _row("RL-2026-006", "deferred", "Deferred learning is not eligible."),
        _row("RL-2026-007", "rejected", "Rejected learning is not eligible."),
        _row("RL-2026-008", "superseded", "Superseded learning is not eligible."),
    ]
    (repo / "os" / "recursive-learning-ledger.md").write_text(_ledger(rows), encoding="utf-8")
    (repo / "docs" / "source.md").write_text("# Synthetic source\n", encoding="utf-8")
    (repo / "projects" / "alpha" / "README.md").write_text(
        "# Alpha\n\n## Review Gate\n\nA reusable evidence checklist supports a bounded review cadence.\n",
        encoding="utf-8",
    )
    (repo / "projects" / "alpha" / "executive-os-install.md").write_text(
        "# Install\n\n## Memory\n\nPreserve decisions, risks, evidence, and follow-ups.\n",
        encoding="utf-8",
    )
    synthetic_email = "reviewer" + chr(64) + "example.com"
    (repo / "projects" / "alpha" / "operating-review.md").write_text(
        f"# Review\n\nContact {synthetic_email} for the private review.\n", encoding="utf-8"
    )
    (repo / "projects" / "tenant-private" / "README.md").write_text(
        "# Private\n\nA private customer pattern must not cross.\n", encoding="utf-8"
    )
    (repo / "projects" / "alpha" / "archive" / "README.md").write_text(
        "# Archive\n\nArchived transcript evidence must not be mined.\n", encoding="utf-8"
    )
    _run(repo, "git", "init", "-q")
    _run(repo, "git", "config", "user.name", "Pattern Memory Test")
    _run(repo, "git", "config", "user.email", "pattern-memory-test" + chr(64) + "example.invalid")
    _run(repo, "git", "add", ".")
    _run(repo, "git", "commit", "-qm", "synthetic governed pattern corpus")
    (repo / "projects" / "alpha" / "membrane-notes.md").write_text(
        "# Untracked\n\nAn untracked pattern must not enter the corpus.\n", encoding="utf-8"
    )
    return repo


def test_only_eligible_learning_and_allowlisted_tracked_projects_enter(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path)
    corpus = compile_corpus(repo)
    learning = [item for item in corpus.candidates if item.source_tier == "governed-learning"]
    assert {item.learning_state for item in learning} == ELIGIBLE_LEARNING_STATES
    references = {item.source_reference for item in corpus.candidates}
    assert any(value.startswith("projects/alpha/README.md#") for value in references)
    assert not any("archive" in value or "tenant-private" in value for value in references)
    assert not any("operating-review.md" in value or "membrane-notes.md" in value for value in references)
    assert corpus.exclusion_counts["untracked-source"] == 1
    assert corpus.exclusion_counts["privacy-source"] == 1
    assert corpus.exclusion_counts["prohibited-source"] == 1


def test_live_governed_learning_evidence_references_are_navigable() -> None:
    corpus = compile_corpus(ROOT)
    governed = [
        item
        for item in corpus.candidates
        if item.source_tier == "governed-learning"
    ]

    assert governed
    assert all(item.evidence_references for item in governed)

    tracked = {
        line.strip()
        for line in subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.splitlines()
        if line.strip()
    }

    for candidate in governed:
        source_path = candidate.source_reference.split("#", 1)[0]
        source_parent = (ROOT / source_path).parent
        for reference in candidate.evidence_references:
            evidence_path = (source_parent / reference.split("#", 1)[0]).resolve()
            relative = evidence_path.relative_to(ROOT).as_posix()
            assert relative in tracked

    rl_001 = next(item for item in governed if item.section == "RL-2026-001")
    assert rl_001.evidence_references == (
        "../docs/recursive-self-enhancement.md",
        "recursive-learning-ledger.md",
    )
    assert verify_source_reference(
        ROOT,
        {
            "candidate_id": rl_001.candidate_id,
            "source_reference": rl_001.source_reference,
            "content_hash": rl_001.content_hash,
        },
    )


def test_stable_json_ranking_hashes_and_provenance_reconstruct(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path)
    first = query_pattern_memory("evidence review assurance", "shared-primitives", "2026-08-04T18:00:00Z", repo=repo)
    second = query_pattern_memory("evidence review assurance", "shared-primitives", "2026-08-04T18:00:00Z", repo=repo)
    assert render_pattern_memory_json(first) == render_pattern_memory_json(second)
    assert first["report_id"] == second["report_id"]
    assert first["candidates"]
    assert all(verify_source_reference(repo, item) for item in first["candidates"])
    assert first["candidates"][0]["source_reference"].endswith("#RL-2026-001")


def test_exact_learning_id_and_heading_receive_predictable_boosts(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path)
    exact = query_pattern_memory("RL-2026-003", "shared-primitives", "2026-08-04T18:00:00Z", repo=repo)
    heading = query_pattern_memory("Review Gate", "alpha", "2026-08-04T18:00:00Z", repo=repo)
    assert exact["candidates"][0]["source_reference"].endswith("#RL-2026-003")
    assert heading["candidates"][0]["section"] == "Review Gate"


def test_retrieval_budgets_are_visible_and_deterministic(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path, long_learning=True)
    report = query_pattern_memory("retrieval bounded evidence pattern", "shared-primitives", "2026-08-04T18:00:00Z", repo=repo)
    limits = report["retrieval_limits"]
    assert len(report["candidates"]) <= MAX_RESULTS
    assert limits["max_chars_per_result"] == MAX_CHARS_PER_RESULT
    assert limits["max_total_chars"] == MAX_TOTAL_CHARS
    assert limits["returned_chars"] <= MAX_TOTAL_CHARS
    assert any(item["excerpt_truncated"] for item in report["candidates"])
    assert report["exclusion_counts"]["per-result-character-budget"] >= 1


def test_invalid_sources_and_outputs_write_nothing(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path)
    ledger = repo / "os" / "recursive-learning-ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8").replace(
            "| RL-2026-001 | 2026-08-04 |",
            "| RL-2026-001 |",
        ),
        encoding="utf-8",
    )
    report_path = repo / "generated-patterns" / "invalid.json"
    with pytest.raises(PatternMemoryError):
        query_pattern_memory("evidence", "shared-primitives", "2026-08-04T18:00:00Z", repo=repo)
    assert not report_path.exists()

    _run(repo, "git", "restore", "os/recursive-learning-ledger.md")
    report = query_pattern_memory("evidence", "shared-primitives", "2026-08-04T18:00:00Z", repo=repo)
    with pytest.raises(PatternMemoryError):
        write_pattern_memory_report(report, repo / "docs" / "forbidden.json", format="json", repo=repo)
    assert not (repo / "docs" / "forbidden.json").exists()


def test_output_collision_requires_force_and_markdown_matches_projection(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path)
    report = query_pattern_memory("evidence review", "shared-primitives", "2026-08-04T18:00:00Z", repo=repo)
    output = repo / "generated-patterns" / "report.md"
    write_pattern_memory_report(report, output, format="markdown", repo=repo)
    before = output.read_text(encoding="utf-8")
    with pytest.raises(FileExistsError):
        write_pattern_memory_report(report, output, format="markdown", repo=repo)
    assert output.read_text(encoding="utf-8") == before
    markdown = render_pattern_memory_markdown(report)
    assert str(report["report_id"]) in markdown
    assert str(report["source_corpus_digest"]) in markdown
    assert "Authority effect: `none`" in markdown
    assert all(str(item["candidate_id"]) in markdown for item in report["candidates"])


def test_cli_writes_review_only_json_without_canonical_mutation(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path)
    ledger = repo / "os" / "recursive-learning-ledger.md"
    before = ledger.read_bytes()
    output = repo / "generated-patterns" / "cli.json"
    assert main(
        [
            "pattern-memory",
            "query",
            "--query",
            "evidence review",
            "--target-lane",
            "shared-primitives",
            "--as-of",
            "2026-08-04T18:00:00Z",
            "--format",
            "json",
            "--output",
            str(output),
            "--repo",
            str(repo),
        ]
    ) == 0
    packet = json.loads(output.read_text(encoding="utf-8"))
    assert packet["authority_effect"] == "none"
    assert packet["disposition"] == "review-only"
    assert packet["generation_provenance"]["automatic_promotion"] is False
    assert ledger.read_bytes() == before


def test_request_privacy_and_timestamp_fail_closed(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path)
    with pytest.raises(PatternMemoryError, match="privacy scan"):
        query_pattern_memory(
            "contact reviewer" + chr(64) + "example.com",
            "shared-primitives",
            "2026-08-04T18:00:00Z",
            repo=repo,
        )
    with pytest.raises(PatternMemoryError, match="UTC offset"):
        query_pattern_memory("evidence", "shared-primitives", "2026-08-04T18:00:00", repo=repo)


def test_live_ten_query_replay_meets_shadow_gate() -> None:
    cohort = json.loads(REPLAY.read_text(encoding="utf-8"))
    successes = 0
    for case in cohort["queries"]:
        report = query_pattern_memory(case["query"], cohort["target_lane"], cohort["as_of"], repo=ROOT)
        references = {item["source_reference"] for item in report["candidates"]}
        successes += case["expected_source"] in references
        assert report["authority_effect"] == "none"
        assert all(verify_source_reference(ROOT, item) for item in report["candidates"])
        assert all(item["learning_state"] in ELIGIBLE_LEARNING_STATES for item in report["candidates"] if item["source_tier"] == "governed-learning")
    assert successes >= cohort["minimum_top_five_successes"]
