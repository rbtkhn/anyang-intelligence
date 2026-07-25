from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_protocol_defines_initial_message_types_and_shadow_pilot():
    text = read("docs/executive-interface-protocol.md")
    for value in ("task", "response", "escalation", "receipt", "shadow-mode", "No message type"):
        assert value in text


def test_task_and_response_templates_preserve_observation_boundary():
    task = read("templates/executive-task.md")
    response = read("templates/interface-response.md")
    for value in ("Message ID:", "Authority source:", "Allowed actions:", "Prohibited actions:", "Status:"):
        assert value in task
    for value in ("Direct observations:", "Explicit stakeholder statements:", "Interpretation:", "Unknowns:", "Confidence:"):
        assert value in response


def test_grace_gems_protocol_preserves_client_boundary():
    card = read("projects/grace-gems/authority-card.md")
    assert "Communication Protocol" in card
    assert "No message" in card


def test_external_request_states_require_distinct_evidence():
    protocol = read("docs/executive-interface-protocol.md")
    normalized = " ".join(protocol.split())

    for state in ("`Prepared`", "`Authorized to send`", "`Sent`", "`Answered`"):
        assert state in protocol
    assert "authorization is not transmission" in normalized
    assert "transmission is not delivery or response" in normalized
    assert "Do not create a separate receipt family" in normalized
    assert "Prepared-but-unsent requests" in protocol


def test_grace_gems_evidence_request_is_authorized_but_not_sent():
    handoff = read(
        "projects/grace-gems/"
        "hannah-three-review-evidence-routing-handoff-2026-07-24.md"
    )
    packet = read(
        "projects/grace-gems/"
        "hannah-three-review-evidence-request-packet-2026-07-24.md"
    )
    queue = read("docs/executive-assistant-queue.md")

    assert "**Current supported request state:** `Authorized to send`" in handoff
    assert "| `Sent` | `not supported` |" in handoff
    assert "| `Answered` | `not supported` |" in handoff
    assert "Executive Assistant Communication Receipt is missing" in handoff
    assert "Packet delivery: `not sent; delivery receipt required`" in packet
    assert "GG-EA-EVIDENCE-ROUTE-2026-07-24-01" not in queue
