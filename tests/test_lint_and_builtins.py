from anyang_loop.builtins import get_builtin
from anyang_loop.lint import has_errors, validate_loop
from anyang_loop.model import LoopDefinition


def test_builtins_validate_without_errors():
    for name in ("canonical-executive-loop", "recursive-improvement-loop"):
        loop = get_builtin(name)
        assert loop is not None
        diagnostics = validate_loop(loop)
        assert not has_errors(diagnostics)


def test_missing_required_field_is_error():
    loop = LoopDefinition(
        name="bad-loop",
        signal="signal",
        memory_objects=[],
        decision="",
        action="action",
        evidence="evidence",
        cadence="weekly",
        learning_update="update memory",
        governance_boundary="human approval",
    )
    diagnostics = validate_loop(loop)
    assert has_errors(diagnostics)
    assert any(item.code == "missing-field" for item in diagnostics)


def test_lint_warns_on_evidence_gap():
    loop = LoopDefinition(
        name="thin-loop",
        signal="weekly signal",
        memory_objects=["memory"],
        decision="prepare decision",
        action="owner reviews action",
        evidence="TBD",
        cadence="weekly",
        learning_update="update memory",
        governance_boundary="human owner approval",
    )
    diagnostics = validate_loop(loop)
    assert any(item.code == "evidence-gap" for item in diagnostics)

