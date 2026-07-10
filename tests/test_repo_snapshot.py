from pathlib import Path

from anyang_loop.portfolio_state import parse_portfolio_dashboard
from anyang_loop.repo_snapshot import collect_repo_snapshot

from cadence_helpers import make_git_repo, run, write


def test_snapshot_includes_staged_unstaged_deleted_renamed_and_untracked(tmp_path: Path):
    make_git_repo(tmp_path)
    write(tmp_path / "a.txt", "a\n")
    write(tmp_path / "b.txt", "b\n")
    write(tmp_path / "c.txt", "c\n")
    run(tmp_path, "git", "add", ".")
    run(tmp_path, "git", "commit", "-m", "tracked files")

    write(tmp_path / "a.txt", "changed\n")
    (tmp_path / "b.txt").unlink()
    run(tmp_path, "git", "mv", "c.txt", "renamed.txt")
    write(tmp_path / "staged.txt", "staged\n")
    run(tmp_path, "git", "add", "staged.txt")
    write(tmp_path / "untracked.txt", "untracked\n")

    snapshot = collect_repo_snapshot(tmp_path)

    assert "a.txt" in snapshot.unstaged
    assert "b.txt" in snapshot.deleted
    assert "c.txt -> renamed.txt" in snapshot.renamed
    assert "staged.txt" in snapshot.staged
    assert "untracked.txt" in snapshot.untracked
    assert snapshot.dirty


def test_portfolio_parser_preserves_pending_context_and_paid_priority():
    state = parse_portfolio_dashboard(
        """# Dashboard

## Current Cash Picture

Unknown or pending:

- Grace Gems owner intake.
- Margin evidence.

## Active Obligations

### Exploratory

- Explore an unpaid idea.

### Media Production

- Operate the Grace Gems $1,000/month retainer.

## Portfolio Rule

Current priority order:

1. Serve Grace Gems through Media Production.
"""
    )

    assert state.unresolved == ("Grace Gems owner intake.", "Margin evidence.")
    assert state.first_paid_obligation == "Media Production: Operate the Grace Gems $1,000/month retainer."


def test_repository_identity_strips_remote_credentials(tmp_path: Path):
    make_git_repo(tmp_path)
    credentialed_remote = "https://user:secret" + chr(64) + "example.com/org/repo.git"
    run(tmp_path, "git", "remote", "add", "origin", credentialed_remote)

    snapshot = collect_repo_snapshot(tmp_path)

    assert snapshot.repo_id == "https://example.com/org/repo.git"
    assert "secret" not in snapshot.repo_id
