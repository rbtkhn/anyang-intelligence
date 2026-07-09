from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DreamContext:
    repo_root: Path
    git_status: str
    recent_commits: list[str]
    changed_paths: list[str]
    dashboard: str
    skills_readme: str
    membranes: str


def build_dream_brief(repo_root: str | Path = ".") -> str:
    root = Path(repo_root).resolve()
    context = DreamContext(
        repo_root=root,
        git_status=_git(root, ["status", "--short", "--branch"]),
        recent_commits=_git_lines(root, ["log", "--oneline", "--decorate", "-8"]),
        changed_paths=_changed_paths(root),
        dashboard=_read(root / "customers" / "operating-portfolio-dashboard.md"),
        skills_readme=_read(root / "skills" / "README.md"),
        membranes=_read(root / "docs" / "membranes.md"),
    )
    return render_dream_brief(context)


def render_dream_brief(context: DreamContext) -> str:
    return "\n".join(
        [
            "Dream:",
            "",
            "Recent rhythm:",
            _recent_rhythm(context),
            "",
            "Run status:",
            f"- Git: {_git_state(context.git_status)}",
            "- Validation: not run by `anyang-dream`; run native validators when the operator asks for verification.",
            "- Generated artifacts: none; dream is read-only unless the operator explicitly asks for file changes.",
            f"- Touched surfaces: {_touched_surfaces(context.changed_paths)}",
            "",
            "Integrity and governance:",
            *_governance_lines(context),
            "",
            "Tomorrow inherits:",
            f"- {_tomorrow_inherits(context)}",
        ]
    )


def _recent_rhythm(context: DreamContext) -> str:
    commit = context.recent_commits[0] if context.recent_commits else "no recent commit visible"
    if context.changed_paths:
        return (
            f"The repo has preserved recent work through `{commit}`, but the current cycle still has uncommitted surfaces. "
            "The closeout job is to keep those surfaces legible, separated, and governed before the next commit."
        )
    return (
        f"The repo appears settled around `{commit}` with no changed paths visible. "
        "The closeout job is to preserve continuity and let tomorrow inherit a clean operating picture."
    )


def _governance_lines(context: DreamContext) -> list[str]:
    lines: list[str] = []
    changed = "\n".join(context.changed_paths).lower()
    if "elementary-school" in changed:
        lines.append(
            "- Elementary School changes remain high-trust: preserve parent authority, child safety, evidence boundaries, and no unsupervised child-facing AI."
        )
    if "commercial" in changed or "subscription" in changed or "retainer" in changed:
        lines.append(
            "- Money language should keep retainers, donor-funded support, customer pricing, subscriptions, revenue, expenses, and hypotheses separate."
        )
    if "skills" in changed or "cli" in changed:
        lines.append("- Skill and CLI changes should stay advisory unless tests and human authority boundaries remain explicit.")
    if not lines:
        lines.append("- No new boundary issue found from changed path names; preserve membrane rules before transferring patterns across customers.")
    return lines


def _tomorrow_inherits(context: DreamContext) -> str:
    changed = "\n".join(context.changed_paths).lower()
    if "coffee" in changed or "dream" in changed:
        return "Verify the native cadence path by using plain `coffee` and `dream` in the next agent session."
    if "elementary-school" in changed:
        return "Choose one Elementary School slice to validate and commit: onboarding, Khan transition, Learning Core, or continuity."
    if context.changed_paths:
        return "Split the dirty worktree into one coherent validated slice before shipping."
    return "A clean re-entry path through native `coffee`."


def _changed_paths(root: Path) -> list[str]:
    paths = _git_lines(root, ["diff", "--name-only"])
    status = _git_lines(root, ["status", "--short"])
    for line in status:
        if line.startswith("?? "):
            paths.append(line[3:].strip())
    return _dedupe(paths)


def _git(root: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        return f"git unavailable: {exc}"
    output = result.stdout.strip()
    if result.returncode != 0:
        return f"git error: {result.stderr.strip() or output}"
    return output or "(no output)"


def _git_lines(root: Path, args: list[str]) -> list[str]:
    output = _git(root, args)
    if output.startswith("git unavailable:") or output.startswith("git error:") or output == "(no output)":
        return []
    return [line for line in output.splitlines() if line.strip()]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _git_state(status: str) -> str:
    branch = status.splitlines()[0] if status else "unknown branch"
    dirty = any(line and not line.startswith("##") for line in status.splitlines())
    return f"{branch}; {'dirty worktree' if dirty else 'clean worktree'}"


def _touched_surfaces(paths: list[str]) -> str:
    if not paths:
        return "none"
    surfaces: list[str] = []
    for prefix in ("customers", "skills", "cli", "tests", "docs", "templates"):
        if any(path.replace("\\", "/").startswith(prefix + "/") for path in paths):
            surfaces.append(prefix)
    return ", ".join(surfaces) if surfaces else ", ".join(paths[:5])


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result
