from __future__ import annotations

import sys
import unittest
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT_ROOT))

from contradiction_kernel import evaluate_contradictions
from host_policy import HOST_POLICY, scan_packet_privacy


class ContradictionPreflightSmokeTest(unittest.TestCase):
    def packet(self, request_value: str = "main") -> dict:
        return {
            "schema_version": 1,
            "request_ref": "request:test",
            "scope": "repository",
            "consequence_level": "consequential",
            "as_of": "2026-07-30T18:00:00Z",
            "request_assertions": [
                {
                    "id": "requested-branch",
                    "field": "git.branch",
                    "value": request_value,
                    "scope": "repository",
                    "source_ref": "request:test#branch",
                    "provisional": False,
                }
            ],
            "controlling_facts": [
                {
                    "id": "current-branch",
                    "field": "git.branch",
                    "value": "main",
                    "scope": "repository",
                    "authority_role": "canonical",
                    "source_ref": "repo:git",
                    "as_of": "2026-07-30T17:59:00Z",
                    "fresh_until": "2026-07-30T18:05:00Z",
                }
            ],
        }

    def evaluate(self, packet: dict) -> dict:
        return evaluate_contradictions(
            packet,
            policy=HOST_POLICY,
            privacy_scanner=scan_packet_privacy,
        )

    def test_aligned_request_continues(self) -> None:
        result = self.evaluate(self.packet())
        self.assertEqual(result["disposition"], "continue")
        self.assertEqual(result["authority_effect"], "none")

    def test_direct_conflict_clarifies(self) -> None:
        result = self.evaluate(self.packet(request_value="feature"))
        self.assertEqual(result["disposition"], "clarify")
        self.assertEqual(
            result["recommended_interaction"],
            "decision-navigation",
        )

    def test_privacy_adapter_fails_closed(self) -> None:
        synthetic_credential = "api" + "_key=" + ("a" * 16)
        findings = scan_packet_privacy(synthetic_credential)
        self.assertEqual(findings, ["credential-assignment"])


if __name__ == "__main__":
    unittest.main()
