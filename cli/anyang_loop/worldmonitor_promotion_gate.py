"""Human-gated bridge from World Monitor receipts to Singularity Science intake."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .worldmonitor_adapter import ExternalSignalReceipt


class PromotionDisposition(str, Enum):
    RETAIN_RECEIPT = "retain-as-external-receipt"
    PROMOTE_SOURCE_NOTE = "promote-to-singularity-source-note"
    HOLD = "hold-for-more-evidence"
    REJECT = "reject-as-noise"


@dataclass(frozen=True)
class PromotionDecision:
    disposition: PromotionDisposition
    rationale: str
    human_review_required: bool = True
    archive_write_performed: bool = False
    customer_routing_performed: bool = False


def evaluate_promotion(
    receipt: ExternalSignalReceipt,
    *,
    materially_relevant: bool,
    source_body_available: bool,
    rights_status_known: bool,
    independent_corroboration: bool = False,
    duplicate_of: str | None = None,
    archive_approval_status: str = "not_requested",
    archive_approval_receipt_ref: str = "",
) -> PromotionDecision:
    """Return a promotion recommendation without writing or routing anything."""
    if receipt.lane != "singularity-science":
        raise ValueError("World Monitor promotion is limited to Singularity Science")
    if receipt.authority_status != "no_authority_created":
        raise ValueError("Receipt has an invalid authority status")
    if duplicate_of:
        return PromotionDecision(PromotionDisposition.RETAIN_RECEIPT, f"Duplicate of {duplicate_of}; retain lineage without archive promotion.")
    if not materially_relevant:
        return PromotionDecision(PromotionDisposition.REJECT, "Signal is not materially relevant to the current Singularity Science question.")
    if not rights_status_known or not source_body_available:
        return PromotionDecision(PromotionDisposition.HOLD, "Hold until source material and rights/attribution status are sufficiently known.")
    if receipt.freshness == "stale" or receipt.confidence == "unknown":
        return PromotionDecision(PromotionDisposition.HOLD, "Hold until freshness or confidence uncertainty is resolved.")
    if not independent_corroboration:
        return PromotionDecision(PromotionDisposition.RETAIN_RECEIPT, "Retain as an external receipt pending independent corroboration.")
    if archive_approval_status != "approved" or not archive_approval_receipt_ref.strip():
        return PromotionDecision(
            PromotionDisposition.HOLD,
            "Evidence is eligible for review, but explicit archive approval and a receipt reference are required before source-note intake.",
        )
    return PromotionDecision(PromotionDisposition.PROMOTE_SOURCE_NOTE, "Eligible for human-reviewed Singularity Science source-note promotion; no archive write performed.")
