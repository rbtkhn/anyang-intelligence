from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path
import re

import yaml


DEFAULT_MANIFEST = "analytical-interfaces.yaml"
ADMINISTRATIVE_TITLES = {"analysis", "report", "essay", "daily brief", "project update", "notes", "discussion"}
GENERIC_HEADINGS = {"analysis", "discussion", "findings", "conclusion", "what happens next"}
PLACEHOLDER_RE = re.compile(r"\[(?:working title|title|label|question|tbd)[^\]]*\]|<[^>]+>|\bTBD\b", re.IGNORECASE)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#{2,6}\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class InterfaceDiagnostic:
    code: str
    path: Path
    message: str


@dataclass(frozen=True)
class GovernedDocument:
    path: Path
    document_type: str = "reader-facing"
    template: bool = False
    require_title_rationale: bool = True
    require_lead_judgment: bool = True
    require_controlling_object: bool = True
    require_uncertainty: bool = True
    require_forecast: bool = False
    require_deliberative_questions: bool = False


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_manifest(path: str | Path | None = None) -> tuple[Path, list[GovernedDocument], list[str]]:
    manifest_path = Path(path) if path else repository_root() / DEFAULT_MANIFEST
    manifest_path = manifest_path.resolve()
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    root = manifest_path.parent
    defaults = data.get("defaults", {})
    documents: list[GovernedDocument] = []
    for entry in data.get("documents", []):
        options = {**defaults, **entry}
        pattern = options.pop("path")
        matches = sorted(root.glob(pattern))
        if not matches and not any(char in pattern for char in "*?["):
            matches = [root / pattern]
        for document_path in matches:
            documents.append(GovernedDocument(path=document_path.resolve(), **options))
    return root, documents, list(data.get("exemptions", []))


def validate_manifest(
    manifest: str | Path | None = None, target: str | Path | None = None
) -> list[InterfaceDiagnostic]:
    root, documents, exemptions = load_manifest(manifest)
    if target:
        target_path = Path(target).resolve()
        documents = [doc for doc in documents if doc.path == target_path or target_path in doc.path.parents]
        if target_path.is_file() and not documents:
            documents = [GovernedDocument(path=target_path)]
    diagnostics: list[InterfaceDiagnostic] = []
    for document in documents:
        relative = _relative_posix(document.path, root)
        if any(Path(relative).match(pattern) or fnmatchcase(relative, pattern) for pattern in exemptions):
            continue
        if not document.path.exists():
            diagnostics.append(InterfaceDiagnostic("missing-governed-document", document.path, "Governed document does not exist."))
            continue
        diagnostics.extend(validate_document(document.path.read_text(encoding="utf-8"), document))
    return diagnostics


def validate_document(text: str, document: GovernedDocument) -> list[InterfaceDiagnostic]:
    diagnostics: list[InterfaceDiagnostic] = []
    titles = H1_RE.findall(text)
    if len(titles) != 1:
        diagnostics.append(InterfaceDiagnostic("h1-count", document.path, "Reader-facing Markdown must contain exactly one H1."))
        return diagnostics
    title = titles[0].strip().strip("`*_ ")
    if PLACEHOLDER_RE.search(title):
        diagnostics.append(InterfaceDiagnostic("placeholder-title", document.path, "Replace the placeholder H1 with a distinctive analytical title."))
    if title.casefold() in ADMINISTRATIVE_TITLES or title.casefold().endswith(" analysis template"):
        diagnostics.append(InterfaceDiagnostic("administrative-title", document.path, "The H1 may not consist only of a document type."))

    for heading in HEADING_RE.findall(text):
        normalized = heading.strip().strip("`*_ ").casefold()
        if normalized in GENERIC_HEADINGS:
            diagnostics.append(InterfaceDiagnostic("generic-heading", document.path, f"Replace generic analytical heading: {heading.strip()}"))

    if document.require_title_rationale:
        _require_labeled_value(text, document, diagnostics, "title-rationale", "Title rationale")
    if document.require_lead_judgment:
        _require_section(text, document, diagnostics, "lead-judgment", "Lead Judgment")
    if document.require_controlling_object:
        _require_section(text, document, diagnostics, "controlling-object", "Controlling Object")
    if document.require_uncertainty:
        _validate_uncertainty(text, document, diagnostics)
    if document.require_forecast:
        for field in (
            "Observable claim", "Causal mechanism", "Time boundary", "Strengthening evidence",
            "Weakening evidence", "Resolution criteria", "Principal alternative", "Permitted unresolved state",
        ):
            _require_labeled_value(text, document, diagnostics, "forecast-field", field)
    if document.require_deliberative_questions:
        _validate_questions(text, document, diagnostics)
    return diagnostics


def _require_section(
    text: str, document: GovernedDocument, diagnostics: list[InterfaceDiagnostic], code: str, heading: str
) -> None:
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not match or not _meaningful(match.group("body"), document.template):
        diagnostics.append(InterfaceDiagnostic(code, document.path, f"Add a non-empty '{heading}' section."))


def _require_labeled_value(
    text: str, document: GovernedDocument, diagnostics: list[InterfaceDiagnostic], code: str, label: str
) -> None:
    match = re.search(
        rf"^\s*(?:[-*]\s+)?(?:\*\*)?{re.escape(label)}\s*:(?:\*\*)?\s*(.+)$",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    if not match or not _meaningful(match.group(1), document.template):
        diagnostics.append(InterfaceDiagnostic(code, document.path, f"Add a nontrivial '{label}:' value."))


def _validate_uncertainty(text: str, document: GovernedDocument, diagnostics: list[InterfaceDiagnostic]) -> None:
    section = re.search(r"^##\s+Uncertainty\s*$\n(?P<body>.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    body = section.group("body") if section else ""
    cause_named = bool(re.search(r"status\s+and\s+cause|cause\s*:", body, re.IGNORECASE))
    reduction_named = bool(re.search(r"evidence\s+that\s+would\s+reduce|reduce\s+the\s+uncertainty", body, re.IGNORECASE))
    if not section or not cause_named or not reduction_named:
        diagnostics.append(InterfaceDiagnostic("uncertainty-cause", document.path, "Uncertainty must name its cause and evidence that would reduce it."))


def _validate_questions(text: str, document: GovernedDocument, diagnostics: list[InterfaceDiagnostic]) -> None:
    questions = [line.strip(" -*") for line in text.splitlines() if "?" in line and not PLACEHOLDER_RE.search(line)]
    discriminators = ("whether", "enough", "without", "justify", "unless", "threshold", "tradeoff", "versus", "vs.")
    if not questions or not any(any(word in question.casefold() for word in discriminators) for question in questions):
        diagnostics.append(InterfaceDiagnostic("nondiscriminating-question", document.path, "Add a completed question containing a disputed premise, tradeoff, mechanism, or threshold."))


def _meaningful(value: str, template: bool) -> bool:
    compact = re.sub(r"\s+", " ", value).strip().strip("`*_ -")
    if len(compact) < 12:
        return False
    if not template and PLACEHOLDER_RE.search(compact):
        return False
    return True


def _relative_posix(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
