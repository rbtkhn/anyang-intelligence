"""Read-only normalization boundary for World Monitor signals.

The adapter deliberately stops at a source receipt. It never creates claims,
approvals, work items, permissions, or doctrine.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Mapping
from urllib.request import Request, urlopen


ADAPTER_VERSION = "worldmonitor-rest-v1"
ALLOWED_CLASSIFICATIONS = {"observation", "inference", "unknown"}


class WorldMonitorSignalError(ValueError):
    """Raised when a signal cannot be safely converted to a receipt."""


@dataclass(frozen=True)
class ExternalSignalReceipt:
    receipt_id: str
    provider: str
    source_url: str
    raw_signal_id: str
    retrieved_at: str
    published_at: str | None
    freshness: str
    source_classification: str
    observation: str
    provider_summary: str
    anyang_inference: str
    confidence: str
    uncertainty: str
    adapter_version: str
    integrity_hash: str
    authority_status: str = "no_authority_created"
    lane: str = "singularity-science"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_worldmonitor_signal(
    signal: Mapping[str, Any], *, retrieved_at: str, lane: str = "singularity-science"
) -> ExternalSignalReceipt:
    """Normalize one World Monitor-shaped signal without assigning authority."""
    required = ("id", "source_url", "provider", "observation")
    missing = [field for field in required if not str(signal.get(field, "")).strip()]
    if missing:
        raise WorldMonitorSignalError(f"Missing required signal fields: {', '.join(missing)}")
    if not _is_timestamp(retrieved_at):
        raise WorldMonitorSignalError("retrieved_at must be an ISO-8601 timestamp")
    classification = str(signal.get("source_classification", "unknown"))
    if classification not in ALLOWED_CLASSIFICATIONS:
        raise WorldMonitorSignalError("source_classification must be observation, inference, or unknown")
    if signal.get("authority_status") not in (None, "no_authority_created"):
        raise WorldMonitorSignalError("World Monitor receipts cannot create authority")
    freshness = str(signal.get("freshness", "unknown"))
    if freshness not in {"fresh", "stale", "unknown"}:
        raise WorldMonitorSignalError("freshness must be fresh, stale, or unknown")
    payload = {
        "id": str(signal["id"]),
        "provider": str(signal["provider"]),
        "source_url": str(signal["source_url"]),
        "observation": str(signal["observation"]),
        "provider_summary": str(signal.get("provider_summary", "")),
        "published_at": signal.get("published_at"),
        "source_classification": classification,
        "freshness": freshness,
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return ExternalSignalReceipt(
        receipt_id=f"wm-{digest[:16]}",
        provider=str(signal["provider"]),
        source_url=str(signal["source_url"]),
        raw_signal_id=str(signal["id"]),
        retrieved_at=retrieved_at,
        published_at=signal.get("published_at"),
        freshness=freshness,
        source_classification=classification,
        observation=str(signal["observation"]),
        provider_summary=str(signal.get("provider_summary", "")),
        anyang_inference="",
        confidence=str(signal.get("confidence", "unknown")),
        uncertainty=str(signal.get("uncertainty", "not assessed")),
        adapter_version=ADAPTER_VERSION,
        integrity_hash=digest,
        lane=lane,
    )


def fetch_worldmonitor_json(url: str, *, api_key: str | None = None, timeout: float = 10.0) -> Any:
    """Fetch JSON only; callers must normalize and review it before use."""
    headers = {"Accept": "application/json", "User-Agent": "anyang-worldmonitor-adapter/1"}
    if api_key:
        headers["X-WorldMonitor-Key"] = api_key
    request = Request(url, headers=headers, method="GET")
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - URL is operator-supplied
        return json.loads(response.read().decode("utf-8"))


def _is_timestamp(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True
