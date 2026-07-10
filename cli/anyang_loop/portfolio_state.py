from __future__ import annotations

import re
from dataclasses import dataclass


HEADING = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
NUMBERED = re.compile(r"^\d+\.\s+(.*)$")


@dataclass(frozen=True)
class PortfolioState:
    obligations: dict[str, tuple[str, ...]]
    unresolved: tuple[str, ...]
    priorities: tuple[str, ...]

    @property
    def first_paid_obligation(self) -> str | None:
        lane_order = [_lane_from_priority(item, self.obligations) for item in self.priorities]
        ordered = [lane for lane in lane_order if lane]
        ordered.extend(lane for lane in self.obligations if lane not in ordered)
        for lane in ordered:
            for item in self.obligations.get(lane, ()):
                if _contains_any(item, ("$", "paid", "retainer", "revenue", "client")):
                    return f"{lane}: {item}"
        return None

    @property
    def first_external_blocker(self) -> str | None:
        return self.unresolved[0] if self.unresolved else None


def parse_portfolio_dashboard(text: str) -> PortfolioState:
    section = ""
    subsection = ""
    obligations: dict[str, list[str]] = {}
    unresolved: list[str] = []
    priorities: list[str] = []
    pending_mode = False
    for raw in text.splitlines():
        line = raw.strip()
        heading = HEADING.match(line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2).strip()
            if level == 2:
                section, subsection, pending_mode = title, "", False
            else:
                subsection = title
            continue
        if section == "Current Cash Picture" and line.lower() == "unknown or pending:":
            pending_mode = True
            continue
        if line.startswith("- "):
            item = line[2:].strip()
            if section == "Active Obligations":
                obligations.setdefault(subsection or "Unclassified", []).append(item)
            if section == "Current Cash Picture" and pending_mode:
                unresolved.append(item)
            continue
        numbered = NUMBERED.match(line)
        if section == "Portfolio Rule" and numbered:
            priorities.append(numbered.group(1).strip())
    return PortfolioState(
        obligations={lane: tuple(items) for lane, items in obligations.items()},
        unresolved=tuple(unresolved),
        priorities=tuple(priorities),
    )


def _lane_from_priority(priority: str, obligations: dict[str, tuple[str, ...]]) -> str | None:
    lowered = priority.lower()
    for lane in obligations:
        if lane.lower() in lowered:
            return lane
    if "grace gems" in lowered and "Media Production" in obligations:
        return "Media Production"
    return None


def _contains_any(value: str, needles: tuple[str, ...]) -> bool:
    lowered = value.lower()
    return any(needle.lower() in lowered for needle in needles)
