from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class RepoSnapshot:
    root: Path
    repo_id: str
    head: str
    branch: str
    sync_status: str
    branch_status: str
    staged: tuple[str, ...]
    unstaged: tuple[str, ...]
    deleted: tuple[str, ...]
    renamed: tuple[str, ...]
    untracked: tuple[str, ...]
    changed_paths: tuple[str, ...]
    touched_surfaces: tuple[str, ...]
    recent_commits: tuple[str, ...]
    fingerprint: str

    @property
    def dirty(self) -> bool:
        return bool(self.changed_paths)

    @property
    def worktree_state(self) -> str:
        return "dirty" if self.dirty else "clean"

    def as_dict(self) -> dict:
        return {
            "repo_id": self.repo_id,
            "head": self.head,
            "branch": self.branch,
            "sync_status": self.sync_status,
            "branch_status": self.branch_status,
            "worktree_state": self.worktree_state,
            "staged": list(self.staged),
            "unstaged": list(self.unstaged),
            "deleted": list(self.deleted),
            "renamed": list(self.renamed),
            "untracked": list(self.untracked),
            "changed_paths": list(self.changed_paths),
            "touched_surfaces": list(self.touched_surfaces),
            "recent_commits": list(self.recent_commits),
            "fingerprint": self.fingerprint,
        }


def collect_repo_snapshot(repo_root: str | Path, recent_limit: int = 8) -> RepoSnapshot:
    root = Path(repo_root).resolve()
    head = _git(root, "rev-parse", "HEAD")
    branch = _git(root, "branch", "--show-current") or "detached"
    branch_status = (_git(root, "status", "--short", "--branch").splitlines() or ["unknown"])[0]
    staged_rows = _name_status(root, "diff", "--cached", "--name-status", "-z")
    unstaged_rows = _name_status(root, "diff", "--name-status", "-z")
    untracked = tuple(sorted(_split_nul(_git(root, "ls-files", "--others", "--exclude-standard", "-z"))))
    staged = tuple(sorted(_row_path(row) for row in staged_rows))
    unstaged = tuple(sorted(_row_path(row) for row in unstaged_rows))
    deleted = tuple(sorted({row[-1] for row in (*staged_rows, *unstaged_rows) if row[0].startswith("D")}))
    renamed = tuple(sorted(f"{row[1]} -> {row[2]}" for row in (*staged_rows, *unstaged_rows) if row[0].startswith("R")))
    changed_paths = tuple(sorted(set((*staged, *unstaged, *untracked))))
    surfaces = tuple(sorted({_surface(path) for path in changed_paths if _surface(path)}))
    recent = tuple(line for line in _git(root, "log", "--oneline", f"-{recent_limit}").splitlines() if line.strip())
    repo_id = repository_identity(root)
    sync = _sync_status(branch_status)
    payload = {
        "head": head,
        "branch": branch,
        "sync": sync,
        "staged": staged,
        "unstaged": unstaged,
        "untracked": untracked,
        "deleted": deleted,
        "renamed": renamed,
    }
    fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return RepoSnapshot(
        root=root,
        repo_id=repo_id,
        head=head,
        branch=branch,
        sync_status=sync,
        branch_status=branch_status,
        staged=staged,
        unstaged=unstaged,
        deleted=deleted,
        renamed=renamed,
        untracked=untracked,
        changed_paths=changed_paths,
        touched_surfaces=surfaces,
        recent_commits=recent,
        fingerprint=fingerprint,
    )


def repository_identity(root: Path) -> str:
    remote = _git(root, "config", "--get", "remote.origin.url", allow_failure=True).strip()
    if remote:
        return _sanitize_remote(remote)
    return root.name


def _sanitize_remote(remote: str) -> str:
    if "://" in remote:
        parsed = urlsplit(remote)
        host = parsed.hostname or ""
        port = f":{parsed.port}" if parsed.port else ""
        return urlunsplit((parsed.scheme.lower(), f"{host.lower()}{port}", parsed.path.rstrip("/"), "", ""))
    if "@" in remote and ":" in remote:
        remote = remote.split("@", 1)[1]
    return remote.rstrip("/")


def _git(root: Path, *args: str, allow_failure: bool = False) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, check=False, text=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0 and not allow_failure:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout.decode("utf-8", errors="replace").strip("\0\r\n")


def _name_status(root: Path, *args: str) -> tuple[tuple[str, ...], ...]:
    parts = _split_nul(_git(root, *args))
    rows: list[tuple[str, ...]] = []
    index = 0
    while index < len(parts):
        status = parts[index]
        width = 3 if status.startswith(("R", "C")) else 2
        if index + width > len(parts):
            break
        rows.append(tuple(parts[index : index + width]))
        index += width
    return tuple(rows)


def _split_nul(value: str) -> list[str]:
    return [part for part in value.split("\0") if part]


def _row_path(row: tuple[str, ...]) -> str:
    return row[-1]


def _surface(path: str) -> str:
    normalized = path.replace("\\", "/")
    return normalized.split("/", 1)[0] if normalized else ""


def _sync_status(branch_status: str) -> str:
    lowered = branch_status.lower()
    if "ahead" in lowered and "behind" in lowered:
        return "diverged"
    if "ahead" in lowered:
        return "ahead"
    if "behind" in lowered:
        return "behind"
    if "..." in branch_status:
        return "synced"
    return "untracked-branch"
