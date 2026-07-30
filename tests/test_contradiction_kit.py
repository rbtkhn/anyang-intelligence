from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "templates" / "contradiction-preflight-kit"
BUILDER_PATH = ROOT / "tools" / "build_contradiction_preflight_kit.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("contradiction_kit_builder", BUILDER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def test_tracked_kit_verifies_and_generated_kernel_matches() -> None:
    builder = load_builder()
    manifest = builder.verify(KIT)

    assert manifest["kit_id"] == "contradiction-preflight-transplant-v1"
    assert manifest["authority_effect"] == "none"
    assert len(manifest["source_contract_commit"]) == 40
    assert manifest["generated_files"] == sorted(builder.GENERATED_FILES)
    for relative, source in builder.GENERATED_FILES.items():
        assert (KIT / relative).read_bytes() == source.read_bytes()


def test_kit_build_is_deterministic(tmp_path: Path) -> None:
    builder = load_builder()
    first = tmp_path / "first"
    second = tmp_path / "second"

    first_manifest = builder.build(first)
    second_manifest = builder.build(second)

    assert first_manifest == second_manifest
    assert tree_bytes(first) == tree_bytes(second)
    assert builder.verify(first) == first_manifest
    assert builder.verify(second) == second_manifest


def test_standalone_cli_runs_without_anyang_package_imports() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "contradiction_check.py",
            "--packet",
            "contradiction-packet.example.yaml",
            "--format",
            "json",
        ],
        cwd=KIT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["disposition"] == "continue"
    assert payload["authority_effect"] == "none"
    core = (KIT / "contradiction_kernel" / "core.py").read_text(encoding="utf-8")
    assert "from anyang_loop" not in core


def test_transplant_contract_preserves_authority_and_discovery_boundaries() -> None:
    readme = " ".join(
        (KIT / "README.md").read_text(encoding="utf-8").lower().split()
    )
    contract = " ".join(
        (KIT / "AGENT_CONTRACT.md").read_text(encoding="utf-8").lower().split()
    )

    for phrase in (
        "does not search repository prose",
        "destination repository",
        "do not turn the checker into a semantic repository scanner",
        "do not edit the generated kernel copy directly",
    ):
        assert phrase in readme
    for phrase in (
        "smallest relevant controlling surface",
        "authority_effect: none",
        "durable correction",
        "exact menu selections",
    ):
        assert phrase in contract
