"""Build or verify the sealed Council Steward pilot source manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/council-steward-source-manifest-2026-07-24.json"
CANONICAL_SOURCES = [
    "authority-envelope.yaml",
    "docs/authority-model.md",
    "docs/executive-council-identity.md",
    "docs/executive-council-three-receipt-pilot.md",
    "docs/executive-council-pilot-tracker.md",
    "docs/executive-council-role-contract.md",
    "docs/council-steward-role-contract.md",
    "docs/governance.md",
    "docs/membranes.md",
    "docs/data-handling-policy.md",
    "docs/executive-interface-protocol.md",
    "docs/council-steward-reconciliation-decision-2026-07-24.md",
    "templates/chief-executive-brief.md",
    "templates/approval-receipt.md",
    "templates/executive-assistant-action-receipt.md",
    "templates/executive-council-transaction-record.md",
    "templates/executive-council-pilot-receipt.md",
]
RESTRICTED_PATH_HASHES = {
    "3B49418FE4F6BEAF6D5EAC251C734347EBF6BD8F3C2913A09868BD74F4F0FF58"
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def path_sha256(relative_path: str) -> str:
    return hashlib.sha256(relative_path.encode("utf-8")).hexdigest().upper()


def manifest_identity(relative_path: str) -> tuple[str, str]:
    identity_hash = path_sha256(relative_path)
    if identity_hash in RESTRICTED_PATH_HASHES:
        return "path_ref", f"sha256:{identity_hash}"
    return "path", relative_path


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def authorized_paths() -> list[str]:
    visible_projects = git(
        "ls-files", "--cached", "--others", "--exclude-standard", "--", "projects"
    ).splitlines()
    paths = set(CANONICAL_SOURCES)
    paths.update(
        path.replace("\\", "/")
        for path in visible_projects
        if path and (ROOT / path).is_file()
    )
    missing = [path for path in paths if not (ROOT / path).is_file()]
    if missing:
        raise FileNotFoundError(f"Authorized sources missing: {missing}")
    return sorted(paths)


def build(output: Path, manifest_id: str) -> dict:
    files = []
    aggregate = hashlib.sha256()
    for relative_path in authorized_paths():
        absolute_path = ROOT / relative_path
        identity_key, identity_value = manifest_identity(relative_path)
        item = {
            identity_key: identity_value,
            "sha256": sha256(absolute_path),
            "bytes": absolute_path.stat().st_size,
        }
        if identity_key == "path_ref":
            item["path_class"] = "restricted-project-path"
        files.append(item)
        aggregate.update(
            f"{identity_value}\0{item['sha256']}\0{item['bytes']}\n".encode("utf-8")
        )

    manifest = {
        "version": 1,
        "manifest_id": manifest_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository_head": git("rev-parse", "HEAD"),
        "working_tree": "dirty snapshot; each authorized file sealed individually",
        "scope": {
            "canonical_sources": CANONICAL_SOURCES,
            "project_root": "projects/",
            "project_visibility": (
                "Git-tracked and untracked non-ignored regular files"
            ),
            "private_or_external_systems": "excluded",
        },
        "file_count": len(files),
        "aggregate_sha256": aggregate.hexdigest().upper(),
        "files": files,
    }
    output.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify(output: Path) -> dict:
    manifest = json.loads(output.read_text(encoding="utf-8"))
    errors = []
    aggregate = hashlib.sha256()
    expected_paths = authorized_paths()
    expected_identities = [manifest_identity(path)[1] for path in expected_paths]
    manifest_identities = [
        item.get("path") or item.get("path_ref") for item in manifest["files"]
    ]
    if manifest_identities != expected_identities:
        errors.append("Authorized path set differs from sealed manifest.")

    for item in manifest["files"]:
        identity = item.get("path") or item.get("path_ref")
        if "path" in item:
            relative_path = item["path"]
        else:
            candidates = [
                path
                for path in expected_paths
                if manifest_identity(path)[1] == item.get("path_ref")
            ]
            if len(candidates) != 1:
                errors.append(f"Restricted path reference is not unique: {identity}")
                continue
            relative_path = candidates[0]
        absolute_path = ROOT / relative_path
        if not absolute_path.is_file():
            errors.append(f"Missing authorized source: {identity}")
            continue
        actual_hash = sha256(absolute_path)
        actual_bytes = absolute_path.stat().st_size
        if actual_hash != item["sha256"]:
            errors.append(f"Hash mismatch: {identity}")
        if actual_bytes != item["bytes"]:
            errors.append(f"Size mismatch: {identity}")
        aggregate.update(
            f"{identity}\0{item['sha256']}\0{item['bytes']}\n".encode("utf-8")
        )

    if aggregate.hexdigest().upper() != manifest["aggregate_sha256"]:
        errors.append("Aggregate hash mismatch.")
    if manifest["file_count"] != len(manifest["files"]):
        errors.append("File-count mismatch.")
    if errors:
        raise SystemExit("\n".join(errors))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--manifest-id", default="EC-STEWARD-SOURCE-2026-07-24-01"
    )
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    manifest = verify(output) if args.verify else build(output, args.manifest_id)
    print(
        json.dumps(
            {
                "manifest": str(output.relative_to(ROOT)),
                "file_count": manifest["file_count"],
                "aggregate_sha256": manifest["aggregate_sha256"],
                "status": "verified" if args.verify else "sealed",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
