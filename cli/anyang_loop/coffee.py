from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .cadence_store import CadenceHandoff, latest_handoff, resolve_cadence_db
from .portfolio_state import PortfolioState, parse_portfolio_dashboard
from .repo_snapshot import RepoSnapshot, collect_repo_snapshot


@dataclass(frozen=True)
class CoffeeContext:
    snapshot: RepoSnapshot
    portfolio: PortfolioState
    handoff: CadenceHandoff | None
    handoff_source: str


def build_coffee_context(repo_root: str | Path = ".", db_path: str | None = None) -> CoffeeContext:
    root = Path(repo_root).resolve()
    snapshot = collect_repo_snapshot(root, recent_limit=5)
    dashboard = _read(root / "customers" / "operating-portfolio-dashboard.md")
    portfolio = parse_portfolio_dashboard(dashboard)
    database = resolve_cadence_db(db_path, for_record=False)
    handoff = latest_handoff(database, snapshot.repo_id) if database else None
    source = str(database) if database else "git-only fallback"
    return CoffeeContext(snapshot=snapshot, portfolio=portfolio, handoff=handoff, handoff_source=source)


def build_coffee_data(repo_root: str | Path = ".", db_path: str | None = None) -> dict[str, Any]:
    context = build_coffee_context(repo_root, db_path)
    snapshot, portfolio, handoff = context.snapshot, context.portfolio, context.handoff
    obligations = _ordered_obligations(portfolio)[:5]
    waiting = list(portfolio.unresolved[:5]) or ["No external blocker is explicitly recorded in the portfolio dashboard."]
    failures = _handoff_failures(handoff)
    if failures:
        learning = "The last recorded closeout found verification failures; the next cycle should resolve evidence before expanding scope."
        improvement = handoff.tomorrow_inherits if handoff else "Resolve the recorded verification failure."
        reason = "validation-failure"
    elif handoff:
        learning = f"The last recorded closeout bounded the next cycle: {handoff.tomorrow_inherits}"
        improvement = handoff.tomorrow_inherits
        reason = "recorded-handoff"
    elif snapshot.dirty:
        learning = "No recorded learning is available; current Git and portfolio state are orientation only."
        improvement = "Validate and isolate one coherent dirty-worktree slice before shipping."
        reason = "dirty-worktree"
    elif portfolio.first_external_blocker:
        learning = "No recorded learning is available; the portfolio still exposes an unresolved external input."
        improvement = f"Clarify the highest-priority external blocker: {portfolio.first_external_blocker}"
        reason = "external-blocker"
    elif portfolio.first_paid_obligation:
        learning = "No recorded learning is available; the next move should remain grounded in the first paid obligation."
        improvement = f"Scope the next deliverable for {portfolio.first_paid_obligation}"
        reason = "paid-obligation"
    else:
        learning = "No supported learning is recorded."
        improvement = "Refresh the portfolio dashboard before selecting more work."
        reason = "stale-portfolio"
    entropy = _entropy(context, failures)
    menu = _menu(context, reason, improvement)
    latest = snapshot.recent_commits[0] if snapshot.recent_commits else "no recent commit visible"
    return {
        "current_picture": (
            f"Anyang Intelligence is operating from `{snapshot.root.name}` on `{snapshot.branch}` with a "
            f"{snapshot.worktree_state} worktree and remote state `{snapshot.sync_status}`. "
            f"The latest visible commit is `{latest}`. Cadence continuity source: {context.handoff_source}."
        ),
        "live_obligations": obligations or ["No active obligation is explicitly recorded."],
        "waiting_on": waiting,
        "entropy_flags": entropy,
        "one_learning": learning,
        "improvement_candidate": improvement,
        "menu": menu,
        "decision_reason": reason,
        "snapshot": snapshot.as_dict(),
        "handoff": handoff.as_dict() if handoff else None,
    }


def build_coffee_brief(repo_root: str | Path = ".", db_path: str | None = None) -> str:
    return render_coffee_text(build_coffee_data(repo_root, db_path))


def render_coffee_text(data: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Current picture:",
            data["current_picture"],
            "",
            "Live obligations:",
            *_bullets(data["live_obligations"]),
            "",
            "Waiting on:",
            *_bullets(data["waiting_on"]),
            "",
            "Entropy flags:",
            *_bullets(data["entropy_flags"]),
            "",
            "One learning:",
            f"- {data['one_learning']}",
            "",
            "Improvement candidate:",
            f"- {data['improvement_candidate']}",
            "",
            "Coffee menu - reply A-D:",
            *data["menu"],
        ]
    )


def render_coffee_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def _ordered_obligations(portfolio: PortfolioState) -> list[str]:
    result: list[str] = []
    lane_order: list[str] = []
    for priority in portfolio.priorities:
        lowered = priority.lower()
        for lane in portfolio.obligations:
            if lane.lower() in lowered or ("grace gems" in lowered and lane == "Media Production"):
                if lane not in lane_order:
                    lane_order.append(lane)
    lane_order.extend(lane for lane in portfolio.obligations if lane not in lane_order)
    for lane in lane_order:
        result.extend(f"{lane}: {item}" for item in portfolio.obligations[lane])
    return result


def _handoff_failures(handoff: CadenceHandoff | None) -> list[dict[str, Any]]:
    if not handoff:
        return []
    return [item for item in handoff.validation if item.get("status") == "fail"]


def _entropy(context: CoffeeContext, failures: list[dict[str, Any]]) -> list[str]:
    snapshot = context.snapshot
    flags: list[str] = []
    if failures:
        flags.append(f"The last recorded dream contains {len(failures)} failed verification check(s).")
    if snapshot.sync_status in {"ahead", "behind", "diverged"}:
        flags.append(f"The local branch is {snapshot.sync_status}; remote continuity should not be assumed.")
    if snapshot.dirty:
        flags.append(
            f"The worktree has {len(snapshot.changed_paths)} changed path(s), including {len(snapshot.untracked)} untracked path(s)."
        )
    if context.handoff and context.handoff.snapshot_fingerprint == snapshot.fingerprint:
        flags.append("Repository state matches the latest recorded dream snapshot.")
    if not context.portfolio.priorities:
        flags.append("The portfolio dashboard has no parseable current priority order.")
    return flags or ["No material entropy flag is supported by the current repository and portfolio state."]


def _menu(context: CoffeeContext, reason: str, improvement: str) -> list[str]:
    blocker = (context.portfolio.first_external_blocker or "the highest-priority external input").rstrip(".")
    paid = (context.portfolio.first_paid_obligation or "the highest-priority paid obligation").rstrip(".")
    recommended = {"validation-failure": "A", "dirty-worktree": "A", "external-blocker": "B", "paid-obligation": "B"}.get(reason, "A")
    ship = (
        "Ship the validated cadence or customer slice after human review."
        if not context.snapshot.dirty and not _handoff_failures(context.handoff)
        else "Hold shipping until the selected slice is cleanly validated."
    )
    options = {
        "A": ("Confirm", f"Validate the evidence behind: {improvement}"),
        "B": ("Scope", f"Clarify {blocker} before expanding {paid}."),
        "C": ("Deepen", "Inspect the relevant loop, membrane, and authority boundary without transferring private context."),
        "D": ("Ship", ship),
    }
    return [
        f"{key}. {label}{' (recommended)' if key == recommended else ''} - {action}"
        for key, (label, action) in options.items()
    ]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _bullets(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values]
