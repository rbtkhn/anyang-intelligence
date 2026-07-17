from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_GUIDANCE = [
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "cli" / "README.md",
    ROOT / "docs" / "analytical-interfaces.md",
    ROOT / "docs" / "data-handling-policy.md",
    ROOT / "docs" / "data-store-roles.md",
    ROOT / "docs" / "operating-substrate-migration-plan.md",
    ROOT / "docs" / "recursive-self-enhancement-checklist.md",
    ROOT / "playbooks" / "weekly-executive-review.md",
    ROOT / "skills" / "coffee" / "SKILL.md",
    ROOT / "skills" / "dream" / "SKILL.md",
    ROOT / "skills" / "review-ai-harness" / "SKILL.md",
]


def test_active_guidance_has_no_obsolete_runtime_assumptions() -> None:
    for path in ACTIVE_GUIDANCE:
        text = path.read_text(encoding="utf-8")
        assert "python -m pytest" not in text.lower(), path
        assert not re.search(r"C:\\Users\\[^\\]+.*python(?:\.exe)?", text, re.IGNORECASE), path
        assert "codex-primary-runtime" not in text, path


def test_ci_has_one_canonical_validation_inventory() -> None:
    workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
    assert "python tools/validate_repo.py" in workflow
    assert "pip install" not in workflow
    assert "pytest" not in workflow
    assert "anyang_loop" not in workflow


def test_active_skills_route_repo_commands_through_launchers() -> None:
    coffee = (ROOT / "skills" / "coffee" / "SKILL.md").read_text(encoding="utf-8")
    dream = (ROOT / "skills" / "dream" / "SKILL.md").read_text(encoding="utf-8")
    harness = (ROOT / "skills" / "review-ai-harness" / "SKILL.md").read_text(encoding="utf-8")
    assert ".\\tools\\run.ps1 coffee" in coffee
    assert ".\\tools\\run.ps1 dream" in dream
    assert ".\\tools\\run.ps1 project harness" in harness
    assert ".\\tools\\validate.ps1" in coffee
    assert ".\\tools\\validate.ps1" in dream


def test_agent_runtime_contract_routes_validation_through_canonical_launcher() -> None:
    contract = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()

    assert ".\\tools\\validate.ps1" in contract
    assert "python3 tools/validate_repo.py" in contract
    assert "do not invoke pytest directly" in contract
