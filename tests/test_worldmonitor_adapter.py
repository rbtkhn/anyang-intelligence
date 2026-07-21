from __future__ import annotations

import pytest

from cli.anyang_loop.worldmonitor_adapter import (
    normalize_worldmonitor_signal,
    WorldMonitorSignalError,
)


@pytest.fixture()
def signal():
    return {
        "id": "fixture-001",
        "provider": "World Monitor fixture",
        "source_url": "https://example.test/signals/fixture-001",
        "published_at": "2026-07-20T12:00:00Z",
        "freshness": "fresh",
        "source_classification": "observation",
        "observation": "A fictional infrastructure event was reported by the fixture source.",
        "provider_summary": "Provider-generated summary; not an Anyang conclusion.",
        "confidence": "medium",
        "uncertainty": "Independent corroboration is not yet available.",
    }


def test_normalizes_receipt_with_lineage_and_no_authority(signal):
    receipt = normalize_worldmonitor_signal(signal, retrieved_at="2026-07-20T13:00:00Z")
    assert receipt.receipt_id == "wm-" + receipt.integrity_hash[:16]
    assert receipt.source_url == signal["source_url"]
    assert receipt.anyang_inference == ""
    assert receipt.authority_status == "no_authority_created"
    assert receipt.adapter_version == "worldmonitor-rest-v1"


@pytest.mark.parametrize("field", ["id", "provider", "source_url", "observation"])
def test_rejects_missing_lineage_or_observation(signal, field):
    signal[field] = ""
    with pytest.raises(WorldMonitorSignalError, match="Missing required"):
        normalize_worldmonitor_signal(signal, retrieved_at="2026-07-20T13:00:00Z")


def test_rejects_bad_timestamp(signal):
    with pytest.raises(WorldMonitorSignalError, match="ISO-8601"):
        normalize_worldmonitor_signal(signal, retrieved_at="not-a-time")


def test_rejects_authority_creation(signal):
    signal["authority_status"] = "approved"
    with pytest.raises(WorldMonitorSignalError, match="cannot create authority"):
        normalize_worldmonitor_signal(signal, retrieved_at="2026-07-20T13:00:00Z")


def test_duplicate_signal_is_idempotent(signal):
    first = normalize_worldmonitor_signal(signal, retrieved_at="2026-07-20T13:00:00Z")
    second = normalize_worldmonitor_signal(signal, retrieved_at="2026-07-20T13:00:00Z")
    assert first.to_dict() == second.to_dict()


def test_stale_signal_is_visible_but_marked_stale(signal):
    signal["freshness"] = "stale"
    receipt = normalize_worldmonitor_signal(signal, retrieved_at="2026-07-20T13:00:00Z")
    assert receipt.freshness == "stale"
    assert receipt.authority_status == "no_authority_created"


def test_provider_summary_stays_distinct_from_anyang_inference(signal):
    receipt = normalize_worldmonitor_signal(signal, retrieved_at="2026-07-20T13:00:00Z")
    assert receipt.provider_summary
    assert receipt.anyang_inference == ""
