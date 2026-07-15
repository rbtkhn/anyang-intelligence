from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_direct_pytest_uses_repo_local_base_temp():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "[tool.pytest.ini_options]" in pyproject
    assert 'addopts = "--basetemp=.pytest_cache/pytest-local"' in pyproject


def test_ci_matrix_uses_a_distinct_repo_local_base_temp():
    workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

    expected = "--basetemp=.pytest-ci-${{ matrix.os }}-${{ matrix.python-version }}"
    assert expected in workflow
