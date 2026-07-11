from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .lint import has_errors, validate_loop
from .parser import load_loop_file


CORE_FILES = ("README.md", "executive-os-install.md")
GENERATED_FILES = ("risk-register.md", "decision-log.md", "operating-review.md", "30-day-plan.md", "membrane-notes.md")
INSTALL_SECTIONS = (
    "Context Map",
    "Executive Memory Objects",
    "Decision System",
    "Operating Review Cadence",
    "Risk and Governance Boundary",
    "30-Day Installation Plan",
    "Success Criteria",
)


@dataclass
class InstallValidationResult:
    path: Path
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_install_path(path: str | Path) -> list[InstallValidationResult]:
    root = Path(path)
    if is_customer_folder(root) and not is_customer_collection(root):
        return [validate_customer_folder(root, strict=True)]
    results: list[InstallValidationResult] = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and is_customer_folder(child):
            results.append(validate_customer_folder(child, strict=False))
    if not results:
        results.append(InstallValidationResult(root, ["No customer folders found."], []))
    return results


def is_customer_folder(path: Path) -> bool:
    return (path / "README.md").exists() or (path / "executive-os-install.md").exists()


def is_customer_collection(path: Path) -> bool:
    return any(child.is_dir() and (child / "executive-os-install.md").exists() for child in path.iterdir())


def validate_customer_folder(path: Path, strict: bool) -> InstallValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    for filename in CORE_FILES:
        if not (path / filename).exists():
            errors.append(f"Missing required file: {filename}")
    for filename in GENERATED_FILES:
        if not (path / filename).exists():
            (errors if strict else warnings).append(f"Missing generated support file: {filename}")

    install_path = path / "executive-os-install.md"
    if install_path.exists():
        install = install_path.read_text(encoding="utf-8")
        for section in INSTALL_SECTIONS:
            if section.lower() not in install.lower():
                (errors if strict else warnings).append(f"Install doc missing generated section name: {section}")
        if "human" not in install.lower() or "authority" not in install.lower():
            errors.append("Install doc must preserve human authority language.")
        if "governance" not in install.lower():
            (errors if strict else warnings).append("Install doc should include explicit governance language.")
    if strict and (path / "membrane-notes.md").exists():
        membrane = (path / "membrane-notes.md").read_text(encoding="utf-8").lower()
        if "transfer" not in membrane or "private" not in membrane:
            errors.append("Membrane notes must describe transfer and private-context boundaries.")

    loop_dir = path / "loop-examples"
    if loop_dir.exists():
        for loop_path in sorted(loop_dir.glob("*.y*ml")):
            try:
                loop = load_loop_file(loop_path)
            except Exception as exc:  # noqa: BLE001 - validation should report all parse failures.
                errors.append(f"Loop parse failed for {loop_path.name}: {exc}")
                continue
            diagnostics = validate_loop(loop)
            if has_errors(diagnostics):
                errors.append(f"Loop validation failed for {loop_path.name}")
    elif strict:
        errors.append("Missing loop-examples directory.")
    else:
        warnings.append("Missing loop-examples directory.")

    return InstallValidationResult(path, errors, warnings)
