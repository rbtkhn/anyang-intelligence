from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CoffeeContext:
    repo_root: Path
    git_status: str
    recent_commits: list[str]
    changed_paths: list[str]
    dashboard: str
    comparison: str
    commercial: str
    skills_readme: str


def build_coffee_brief(repo_root: str | Path = ".") -> str:
    root = Path(repo_root).resolve()
    context = CoffeeContext(
        repo_root=root,
        git_status=_git(root, ["status", "--short", "--branch"]),
        recent_commits=_git_lines(root, ["log", "--oneline", "-5"]),
        changed_paths=_git_lines(root, ["diff", "--name-only"]),
        dashboard=_read(root / "customers" / "operating-portfolio-dashboard.md"),
        comparison=_read(root / "customers" / "comparison-matrix.md"),
        commercial=_read(root / "customers" / "commercial-hypotheses.md"),
        skills_readme=_read(root / "skills" / "README.md"),
    )
    return render_coffee_brief(context)


def render_coffee_brief(context: CoffeeContext) -> str:
    current = _current_picture(context)
    obligations = _live_obligations(context)
    waiting = _waiting_on(context)
    entropy = _entropy_flags(context)
    learning = _one_learning(context)
    improvement = _improvement_candidate(context)
    menu = _menu(context, improvement)
    return "\n".join(
        [
            "Current picture:",
            current,
            "",
            "Live obligations:",
            *_bullets(obligations),
            "",
            "Waiting on:",
            *_bullets(waiting),
            "",
            "Entropy flags:",
            *_bullets(entropy),
            "",
            "One learning:",
            f"- {learning}",
            "",
            "Improvement candidate:",
            f"- {improvement}",
            "",
            "Coffee menu - reply A-D:",
            *menu,
        ]
    )


def _current_picture(context: CoffeeContext) -> str:
    priority = _extract_after(context.dashboard, "Current priority order:", max_lines=6)
    top_priority = _first_numbered(priority) or "Serve paid obligations before unpaid complexity."
    git_summary = _git_summary(context.git_status)
    commit = context.recent_commits[0] if context.recent_commits else "no recent commit visible"
    return (
        f"Anyang Intelligence is operating from `repo_probe` with {git_summary}. "
        f"The latest visible commit is `{commit}`. "
        f"The portfolio rule still points to: {top_priority}"
    )


def _live_obligations(context: CoffeeContext) -> list[str]:
    obligations: list[str] = []
    for line in _section_bullets(context.dashboard, "Active Obligations"):
        normalized = _clean_bullet(line)
        if _contains_any(normalized.lower(), ["$1,000", "paid", "retainer", "grace gems", "elementary school"]):
            obligations.append(normalized)
    if not obligations:
        obligations = [
            "Serve paid customer obligations before unpaid complexity.",
            "Keep human approval boundaries explicit before delivery, publication, spending, or customer commitments.",
        ]
    return _dedupe(obligations)[:5]


def _waiting_on(context: CoffeeContext) -> list[str]:
    waiting = [_clean_bullet(line) for line in _section_bullets(context.dashboard, "Current Cash Picture")]
    waiting = [line for line in waiting if _contains_any(line.lower(), ["unknown", "pending", "await", "response"])]
    if not waiting:
        waiting = [_clean_bullet(line) for line in _section_bullets(context.dashboard, "Immediate Decision Queue")]
    if not waiting:
        waiting = ["Next customer input or operator decision before expanding scope."]
    return _dedupe(waiting)[:5]


def _entropy_flags(context: CoffeeContext) -> list[str]:
    flags: list[str] = []
    status = context.git_status.lower()
    if "ahead" in status:
        flags.append("Local commits are ahead of the remote; sync state should remain visible before assuming remote continuity.")
    if _dirty_status(context.git_status):
        flags.append("The worktree is dirty; split customer drafts, tooling, and skill work before staging.")
    changed = "\n".join(context.changed_paths).lower()
    if "elementary-school" in changed:
        flags.append("Elementary School is high-trust child/family work; parent authority and evidence boundaries need extra scrutiny.")
    if "subscription" in changed or "commercial-hypotheses" in changed:
        flags.append("Pricing, retainer, subscription, donor support, and commercial hypotheses can blur unless named separately.")
    if not flags:
        flags.append("No major entropy flag detected from git state; rely on portfolio dashboard for priority pressure.")
    return flags[:5]


def _one_learning(context: CoffeeContext) -> str:
    changed = "\n".join(context.changed_paths).lower()
    commits = "\n".join(context.recent_commits).lower()
    if "catalog" in changed or "catalog" in commits:
        return "Catalog work is strongest when treated as a scaffold for resource awareness, not as curriculum authority or proof of mastery."
    if "elementary-school" in changed:
        return "Elementary School progress improves when onboarding, parent authority, readiness classification, and plan drafting stay visibly separated."
    if "media-production" in changed:
        return "Media Production work compounds when brief, quality gate, package, and ledger remain separate review surfaces."
    if "skills" in changed:
        return "Repeated operator behavior should become narrow skills only when it improves future execution without weakening human authority."
    return "The Executive OS gets smarter when each work cycle preserves one durable improvement instead of expanding every possible surface."


def _improvement_candidate(context: CoffeeContext) -> str:
    changed = "\n".join(context.changed_paths).lower()
    if "skills/coffee" in changed or "coffee" in context.skills_readme.lower():
        return "Use native `anyang-coffee` plus `skills/coffee/SKILL.md` as the repo-local re-entry path before falling back to external cadence rituals."
    if "elementary-school" in changed:
        return "Stabilize the Elementary School dirty set into one coherent slice: onboarding, Khan transition, Learning Core, or Student Operating System skill."
    if _dirty_status(context.git_status):
        return "Run validation, then commit one clean thematic slice instead of letting mixed customer/docs/tooling changes accumulate."
    return "Keep the portfolio dashboard current so paid obligations remain visible before new exploratory work."


def _menu(context: CoffeeContext, improvement: str) -> list[str]:
    changed = "\n".join(context.changed_paths).lower()
    recommended = "D" if _dirty_status(context.git_status) else "A"
    scope_target = (
        "Elementary School readiness and parent-authority boundaries"
        if "elementary-school" in changed
        else "the highest-priority paid obligation from the portfolio dashboard"
    )
    deepen_target = (
        "catalog -> Khan transition -> Learning Core architecture"
        if "elementary-school" in changed
        else "the next reusable primitive named by the comparison matrix"
    )
    ship_target = "one clean dirty-worktree slice" if _dirty_status(context.git_status) else "the selected improvement candidate"
    lines = [
        "A. Confirm{mark} - Run `anyang-install validate customers` and `anyang-loop validate customers`, then compare results with the portfolio dashboard.",
        f"B. Scope{{mark}} - Clarify {scope_target} before drafting or expanding delivery.",
        f"C. Deepen{{mark}} - Develop {deepen_target} without transferring private customer facts across membranes.",
        f"D. Ship{{mark}} - Implement or commit {ship_target} while preserving human authority and validation evidence.",
    ]
    rendered: list[str] = []
    for index, line in zip(("A", "B", "C", "D"), lines):
        mark = " (recommended)" if index == recommended else ""
        rendered.append(line.format(mark=mark))
    if improvement.startswith("Use native `anyang-coffee`"):
        rendered[0] = "A. Confirm (recommended) - Run `anyang-coffee --repo .` and verify it produces the native Anyang Intelligence coffee shape."
        rendered[3] = "D. Ship - Commit the native coffee command, docs, and tests after validation."
    return rendered


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


def _git_summary(status: str) -> str:
    first = status.splitlines()[0] if status else "unknown git state"
    dirty = "dirty worktree" if _dirty_status(status) else "clean worktree"
    return f"{first}; {dirty}"


def _dirty_status(status: str) -> bool:
    return any(line and not line.startswith("##") for line in status.splitlines())


def _section_bullets(text: str, heading: str) -> list[str]:
    section = _section(text, heading)
    return [
        line.strip()
        for line in section.splitlines()
        if line.strip().startswith(("-", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9."))
    ]


def _section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        return ""
    tail = text[start + len(marker) :]
    end = tail.find("\n## ")
    return tail if end == -1 else tail[:end]


def _extract_after(text: str, marker: str, max_lines: int) -> str:
    start = text.find(marker)
    if start == -1:
        return ""
    return "\n".join(text[start + len(marker) :].splitlines()[:max_lines])


def _first_numbered(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if len(stripped) > 3 and stripped[0].isdigit() and stripped[1] == ".":
            return stripped[3:].strip()
    return None


def _clean_bullet(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("- "):
        return stripped[2:].strip()
    if len(stripped) > 3 and stripped[0].isdigit() and stripped[1] == ".":
        return stripped[3:].strip()
    return stripped


def _contains_any(value: str, needles: list[str]) -> bool:
    return any(needle in value for needle in needles)


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def _bullets(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values]
