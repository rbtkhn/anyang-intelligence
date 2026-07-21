from __future__ import annotations

import pytest

from cli.anyang_loop.worldmonitor_adapter import normalize_worldmonitor_signal
from cli.anyang_loop.worldmonitor_promotion_gate import PromotionDisposition, evaluate_promotion


@pytest.fixture()
def receipt():
    return normalize_worldmonitor_signal(
        {
            "id": "fixture-001",
            "provider": "World Monitor fixture",
            "source_url": "https://example.test/signals/fixture-001",
            "published_at": "2026-07-20T12:00:00Z",
            "freshness": "fresh",
            "source_classification": "observation",
            "observation": "A fictional infrastructure event was reported.",
            "provider_summary": "Provider summary.",
            "confidence": "medium",
            "uncertainty": "Corroboration pending.",
        },
        retrieved_at="2026-07-20T13:00:00Z",
    )


def test_relevant_signal_with_complete_evidence_is_only_eligible_for_human_promotion(receipt):
    decision = evaluate_promotion(
        receipt,
        materially_relevant=True,
        source_body_available=True,
        rights_status_known=True,
        independent_corroboration=True,
    )
    assert decision.disposition is PromotionDisposition.PROMOTE_SOURCE_NOTE
    assert decision.human_review_required is True
    assert decision.archive_write_performed is False
    assert decision.customer_routing_performed is False


def test_missing_source_body_holds(receipt):
    decision = evaluate_promotion(receipt, materially_relevant=True, source_body_available=False, rights_status_known=True)
    assert decision.disposition is PromotionDisposition.HOLD


def test_uncorroborated_signal_stays_at_receipt(receipt):
    decision = evaluate_promotion(receipt, materially_relevant=True, source_body_available=True, rights_status_known=True)
    assert decision.disposition is PromotionDisposition.RETAIN_RECEIPT


def test_duplicate_signal_is_not_promoted(receipt):
    decision = evaluate_promotion(
        receipt,
        materially_relevant=True,
        source_body_available=True,
        rights_status_known=True,
        duplicate_of="wm-existing-001",
    )
    assert decision.disposition is PromotionDisposition.RETAIN_RECEIPT


def test_irrelevant_signal_is_rejected_as_noise(receipt):
    decision = evaluate_promotion(receipt, materially_relevant=False, source_body_available=True, rights_status_known=True)
    assert decision.disposition is PromotionDisposition.REJECT


def test_non_singularity_lane_is_rejected():
    receipt = normalize_worldmonitor_signal(
        {
            "id": "fixture-002",
            "provider": "World Monitor fixture",
            "source_url": "https://example.test/signals/fixture-002",
            "observation": "An observation.",
        },
        retrieved_at="2026-07-20T13:00:00Z",
        lane="grace-gems",
    )
    with pytest.raises(ValueError, match="limited to Singularity Science"):
        evaluate_promotion(receipt, materially_relevant=True, source_body_available=True, rights_status_known=True)
