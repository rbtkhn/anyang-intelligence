from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_project_state_update_is_cataloged_with_standard_route_metadata():
    skill_path = ROOT / "skills" / "project-state-update" / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    _, frontmatter_text, _ = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    assert frontmatter["name"] == "project-state-update"
    assert "project fact" in frontmatter["description"]

    catalog = (ROOT / "skills" / "README.md").read_text(encoding="utf-8")
    assert "[project-state-update](project-state-update/SKILL.md)" in catalog

    route = yaml.safe_load((skill_path.parent / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    assert route["interface"]["display_name"] == "Project State Update"
    assert "$project-state-update" in route["interface"]["default_prompt"]
