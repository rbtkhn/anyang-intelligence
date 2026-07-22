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
