"""Build or verify the standalone contradiction-preflight transplant kit."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "templates" / "contradiction-preflight-kit"
CANONICAL_KERNEL = ROOT / "cli" / "anyang_loop" / "contradiction_kernel"
GENERATED_FILES = {
    "contradiction_kernel/__init__.py": CANONICAL_KERNEL / "__init__.py",
    "contradiction_kernel/core.py": CANONICAL_KERNEL / "core.py",
}
STATIC_FILES = (
    "AGENT_CONTRACT.md",
    "README.md",
    "contradiction-packet.example.yaml",
    "contradiction_check.py",
    "host_policy.py",
    "pyproject.toml",
    "tests/test_smoke.py",
)
MANIFEST_NAME = "MANIFEST.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def source_contract_commit() -> str:
    result = subprocess.run(
        [
            "git",
            "log",
            "-1",
            "--format=%H",
            "--",
            "cli/anyang_loop/contradiction_kernel/core.py",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    commit = result.stdout.strip()
    if len(commit) != 40:
        raise RuntimeError("Canonical kernel has no committed source identity")
    return commit


def _copy_static(output: Path) -> None:
    if output == DEFAULT_OUTPUT:
        return
    for relative in STATIC_FILES:
        source = DEFAULT_OUTPUT / relative
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def _copy_generated(output: Path) -> None:
    for relative, source in GENERATED_FILES.items():
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def _manifest(output: Path) -> dict:
    files = []
    for relative in sorted((*STATIC_FILES, *GENERATED_FILES)):
        path = output / relative
        body = path.read_bytes()
        item = {
            "path": relative,
            "sha256": sha256_bytes(body),
            "bytes": len(body),
        }
        if relative in GENERATED_FILES:
            item["generated_from"] = GENERATED_FILES[relative].relative_to(ROOT).as_posix()
        files.append(item)
    aggregate = hashlib.sha256()
    for item in files:
        aggregate.update(
            f"{item['path']}\0{item['sha256']}\0{item['bytes']}\n".encode("utf-8")
        )
    return {
        "schema_version": 1,
        "kit_id": "contradiction-preflight-transplant-v1",
        "source_contract_commit": source_contract_commit(),
        "authority_effect": "none",
        "generated_files": sorted(GENERATED_FILES),
        "file_count": len(files),
        "aggregate_sha256": aggregate.hexdigest(),
        "files": files,
    }


def build(output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    _copy_static(output)
    _copy_generated(output)
    manifest = _manifest(output)
    (output / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify(output: Path) -> dict:
    errors = []
    expected_paths = sorted((*STATIC_FILES, *GENERATED_FILES))
    for relative in expected_paths:
        path = output / relative
        if not path.is_file():
            errors.append(f"Missing kit file: {relative}")
    for relative, source in GENERATED_FILES.items():
        target = output / relative
        if target.is_file() and target.read_bytes() != source.read_bytes():
            errors.append(f"Generated kernel copy drifted: {relative}")
    manifest_path = output / MANIFEST_NAME
    if not manifest_path.is_file():
        errors.append(f"Missing kit file: {MANIFEST_NAME}")
    if errors:
        raise SystemExit("\n".join(errors))
    actual = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = _manifest(output)
    if actual != expected:
        raise SystemExit("Transplant kit manifest does not match current files")
    return actual


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    manifest = verify(output) if args.verify else build(output)
    print(
        json.dumps(
            {
                "kit": str(output),
                "file_count": manifest["file_count"],
                "aggregate_sha256": manifest["aggregate_sha256"],
                "status": "verified" if args.verify else "built",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
