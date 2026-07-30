from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "operating-substrate" / "skills" / "singularity-science" / "SKILL.md"
MIRROR = ROOT / ".codex" / "skills" / "singularity-science" / "SKILL.md"
ALIAS = ROOT / "operating-substrate" / "skills" / "singularity-intake" / "SKILL.md"
MOONSHOTS_TRANSCRIPTS = (
    ROOT
    / "operating-substrate"
    / "projects"
    / "singularity-science"
    / "archive"
    / "moonshots"
    / "transcripts"
)


def test_canonical_skill_has_singular_activation_and_full_scope():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "name: singularity-science" in text
    assert "preferred_activation: singularity" in text
    assert "legacy_activation: singularity-intake" in text
    assert "nate-herk" in text
    assert "source-cluster" in text
    assert "validated reusable primitive" in text


def test_codex_skill_mirror_matches_repository_canonical():
    assert MIRROR.read_text(encoding="utf-8") == CANONICAL.read_text(encoding="utf-8")


def test_legacy_skill_is_only_a_compatibility_alias():
    text = ALIAS.read_text(encoding="utf-8")
    assert "canonical_skill: singularity-science" in text
    assert "Use `singularity` for new work" in text


def test_moonshots_transcript_provenance_has_no_machine_local_attachment_paths():
    for path in MOONSHOTS_TRANSCRIPTS.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert r"C:\Users" not in text, path
        assert "C:/Users" not in text, path
        assert r"\.codex\attachments" not in text, path
        assert ".codex/attachments" not in text, path
