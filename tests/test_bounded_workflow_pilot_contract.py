from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills/bounded-workflow-pilot/SKILL.md"
ROUTE = ROOT / "skills/bounded-workflow-pilot/agents/openai.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalized(path: Path) -> str:
    return " ".join(read(path).split())


def frontmatter(path: Path) -> dict:
    _, raw, _ = read(path).split("---", 2)
    return yaml.safe_load(raw)


def test_pilot_supports_manual_and_automation_routes():
    metadata = frontmatter(CANONICAL)
    canonical = read(CANONICAL)
    assert metadata["name"] == "bounded-workflow-pilot"
    assert "manual or automation workflow experiment" in metadata["description"]
    for phrase in (
        "Accept exactly one route",
        "`manual workflow`",
        "`automation`",
        "Business Loop Pilot Handoff Packet",
        "persisted specification in `Approved for pilot`",
    ):
        assert phrase in canonical


def test_automation_route_cannot_bypass_value_proof():
    canonical = normalized(CANONICAL)
    for phrase in (
        "require one complete human-approved",
        "`automation-value-proof` packet",
        "uses the manual route to avoid automation value proof",
        "For an automation route, additionally require every input mandated by",
    ):
        assert phrase in canonical


def test_manual_route_remains_bounded_and_versioned():
    canonical = read(CANONICAL)
    for phrase in (
        "version-matched approval and persistence receipts",
        "representative run limit",
        "baseline, target, quality threshold, and burden guardrail",
        "prohibited actions and exception route",
        "Do not deploy, schedule, publish, contact customers, spend",
    ):
        assert phrase in canonical


def test_pilot_result_cannot_activate_or_deploy():
    canonical = normalized(CANONICAL)
    for phrase in (
        "`Complete`, `Too thin`, `Revised`, `Blocked`, or `Rejected`",
        "The pilot produces evidence and a recommendation",
        "cannot create an effective deployment, activation, recurring schedule",
    ):
        assert phrase in canonical


def test_pilot_metadata_and_catalog_match_updated_contract():
    route = yaml.safe_load(read(ROUTE))
    assert "$bounded-workflow-pilot" in route["interface"]["default_prompt"]
    assert "[bounded-workflow-pilot](bounded-workflow-pilot/SKILL.md)" in read(
        ROOT / "skills/README.md"
    )
    assert "persisted manual-loop handoff or automation value proof" in read(
        ROOT / "skills/README.md"
    )
