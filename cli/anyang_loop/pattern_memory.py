from __future__ import annotations

import hashlib
import json
import math
import os
import re
import subprocess
import tempfile
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .privacy_scan import PROHIBITED_PATH_PARTS, scan_text


SCHEMA = "anyang-pattern-memory-report/v1"
ELIGIBLE_LEARNING_STATES = {"approved", "implemented", "validated", "observed"}
PROJECT_SOURCE_NAMES = {
    "README.md",
    "executive-os-install.md",
    "operating-review.md",
    "membrane-notes.md",
}
PROHIBITED_SOURCE_PARTS = {
    "archive",
    "analyses",
    "analysis",
    "source-notes",
    "transcripts",
    "tenant-private",
    "customer-private",
    "raw-customer-transcripts",
}
MAX_RESULTS = 5
MAX_CHARS_PER_RESULT = 1000
MAX_TOTAL_CHARS = 4000
TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
LEARNING_ID_RE = re.compile(r"^RL-\d{4}-\d{3}$")

PROFESSIONAL_TERMS = {
    "attorney",
    "compliance",
    "insurance",
    "legal",
    "medical",
    "payroll",
    "tax",
}
KEEP_LOCAL_TERMS = {
    "credential",
    "exact vulnerability",
    "personal information",
    "private customer",
    "private evidence",
    "security detail",
    "tenant-private",
}
APPROVAL_TERMS = {
    "board",
    "child",
    "customer transcript",
    "donor",
    "external claim",
    "family",
    "margin",
    "pricing",
    "property access",
    "spending",
}


class PatternMemoryError(ValueError):
    pass


@dataclass(frozen=True)
class PatternSource:
    source_tier: str
    source_lane: str
    source_reference: str
    section: str
    text: str
    transformed_pattern: str
    learning_state: str | None
    evidence_references: tuple[str, ...]
    content_hash: str
    candidate_id: str
    membrane_classification: str
    required_approval: str


@dataclass(frozen=True)
class Corpus:
    candidates: tuple[PatternSource, ...]
    exclusion_counts: dict[str, int]
    warnings: tuple[str, ...]
    corpus_digest: str


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def compile_corpus(repo: str | Path | None = None) -> Corpus:
    root = Path(repo or repository_root()).resolve()
    tracked = _tracked_paths(root)
    exclusions: Counter[str] = Counter()
    candidates: list[PatternSource] = []
    warnings: set[str] = set()

    ledger = root / "os" / "recursive-learning-ledger.md"
    ledger_relative = ledger.relative_to(root).as_posix()
    if ledger_relative not in tracked:
        raise PatternMemoryError("Recursive learning ledger must be tracked")
    candidates.extend(_parse_learning_ledger(root, ledger, exclusions))

    projects = root / "projects"
    if projects.exists():
        for project in sorted(path for path in projects.iterdir() if path.is_dir()):
            for name in sorted(PROJECT_SOURCE_NAMES):
                path = project / name
                if not path.exists():
                    continue
                relative = path.relative_to(root).as_posix()
                if relative not in tracked:
                    exclusions["untracked-source"] += 1
                    continue
                if _prohibited_source(relative):
                    exclusions["prohibited-source"] += 1
                    continue
                source_candidates, source_exclusions = _parse_project_document(root, path, project.name)
                candidates.extend(source_candidates)
                exclusions.update(source_exclusions)

    if not candidates:
        raise PatternMemoryError("Pattern memory corpus contains no eligible candidates")

    if any(item.source_tier == "project-provisional" for item in candidates):
        warnings.add("Project-derived candidates are provisional and require human review before reuse.")

    candidates.sort(key=lambda item: (item.source_tier, item.source_reference, item.candidate_id))
    corpus_digest = _sha256(
        "\n".join(f"{item.candidate_id}:{item.content_hash}" for item in candidates)
    )
    return Corpus(tuple(candidates), dict(sorted(exclusions.items())), tuple(sorted(warnings)), corpus_digest)


def query_pattern_memory(
    query: str,
    target_lane: str,
    as_of: str,
    *,
    repo: str | Path | None = None,
) -> dict[str, object]:
    normalized_query = " ".join(query.split())
    normalized_lane = " ".join(target_lane.split())
    if not normalized_query or len(normalized_query) > 500:
        raise PatternMemoryError("Query must contain 1 to 500 characters")
    if not normalized_lane or len(normalized_lane) > 120:
        raise PatternMemoryError("Target lane must contain 1 to 120 characters")
    privacy_findings = sorted(set(scan_text(normalized_query + "\n" + normalized_lane)))
    if privacy_findings:
        raise PatternMemoryError("Pattern-memory request failed privacy scan: " + ", ".join(privacy_findings))
    _validate_as_of(as_of)

    corpus = compile_corpus(repo)
    ranked = _rank(corpus.candidates, normalized_query, normalized_lane)
    exclusions: Counter[str] = Counter(corpus.exclusion_counts)
    exclusions["no-lexical-match"] += len(corpus.candidates) - len(ranked)

    selected: list[dict[str, object]] = []
    total_chars = 0
    for source, score in ranked:
        if len(selected) >= MAX_RESULTS:
            exclusions["result-limit"] += 1
            continue
        remaining = MAX_TOTAL_CHARS - total_chars
        if remaining <= 0:
            exclusions["total-character-budget"] += 1
            continue
        allowed = min(MAX_CHARS_PER_RESULT, remaining)
        excerpt, truncated = _truncate(source.text, allowed)
        total_chars += len(excerpt)
        selected.append(
            {
                "candidate_id": source.candidate_id,
                "rank": len(selected) + 1,
                "score": round(score, 6),
                "source_tier": source.source_tier,
                "learning_state": source.learning_state,
                "source_lane": source.source_lane,
                "source_reference": source.source_reference,
                "section": source.section,
                "excerpt": excerpt,
                "excerpt_truncated": truncated,
                "transformed_pattern": source.transformed_pattern,
                "membrane_classification": source.membrane_classification,
                "required_approval": source.required_approval,
                "evidence_references": list(source.evidence_references),
                "content_hash": source.content_hash,
            }
        )
        if truncated:
            exclusions["per-result-character-budget"] += 1

    query_digest = _sha256(
        json.dumps(
            {"query": normalized_query, "target_lane": normalized_lane, "as_of": as_of},
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    report_id = "PMR-" + _sha256(f"{query_digest}:{corpus.corpus_digest}")[:16].upper()
    return {
        "schema": SCHEMA,
        "report_id": report_id,
        "scope": "anyang-internal/repository/internal-sanitized",
        "query": normalized_query,
        "query_digest": query_digest,
        "target_lane": normalized_lane,
        "as_of": as_of,
        "source_corpus_digest": corpus.corpus_digest,
        "authority_effect": "none",
        "disposition": "review-only",
        "candidates": selected,
        "exclusion_counts": dict(sorted((key, value) for key, value in exclusions.items() if value)),
        "warnings": list(corpus.warnings),
        "retrieval_limits": {
            "max_results": MAX_RESULTS,
            "max_chars_per_result": MAX_CHARS_PER_RESULT,
            "max_total_chars": MAX_TOTAL_CHARS,
            "returned_chars": total_chars,
        },
        "generation_provenance": {
            "engine": "deterministic-bm25-lexical-v1",
            "source_tiers": ["governed-learning", "project-provisional"],
            "embeddings": False,
            "model_inference": False,
            "automatic_promotion": False,
        },
    }


def render_pattern_memory_json(report: dict[str, object]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def render_pattern_memory_markdown(report: dict[str, object]) -> str:
    limits = report["retrieval_limits"]
    assert isinstance(limits, dict)
    lines = [
        "# Governed Pattern Memory Report",
        "",
        f"- Report ID: `{report['report_id']}`",
        f"- Schema: `{report['schema']}`",
        f"- Scope: `{report['scope']}`",
        f"- Target lane: `{report['target_lane']}`",
        f"- As of: `{report['as_of']}`",
        f"- Authority effect: `{report['authority_effect']}`",
        f"- Disposition: `{report['disposition']}`",
        f"- Query digest: `{report['query_digest']}`",
        f"- Source corpus digest: `{report['source_corpus_digest']}`",
        "",
        "This is a derived, review-only projection. It does not promote a pattern, update durable memory, or authorize action.",
        "",
        "## Query",
        "",
        str(report["query"]),
        "",
        "## Ranked candidates",
        "",
    ]
    candidates = report["candidates"]
    assert isinstance(candidates, list)
    if not candidates:
        lines.extend(["No eligible lexical match was found.", ""])
    for candidate in candidates:
        assert isinstance(candidate, dict)
        lines.extend(
            [
                f"### {candidate['rank']}. `{candidate['candidate_id']}`",
                "",
                f"- Score: `{candidate['score']}`",
                f"- Source tier: `{candidate['source_tier']}`",
                f"- Learning state: `{candidate['learning_state'] or 'not-applicable'}`",
                f"- Source lane: `{candidate['source_lane']}`",
                f"- Source reference: `{candidate['source_reference']}`",
                f"- Section: `{candidate['section']}`",
                f"- Content hash: `{candidate['content_hash']}`",
                f"- Membrane classification: `{candidate['membrane_classification']}`",
                f"- Required approval: `{candidate['required_approval']}`",
                f"- Excerpt truncated: `{str(candidate['excerpt_truncated']).lower()}`",
                "",
                "**Candidate pattern**",
                "",
                str(candidate["transformed_pattern"]),
                "",
                "**Source excerpt**",
                "",
                str(candidate["excerpt"]),
                "",
                "**Evidence references**",
                "",
            ]
        )
        evidence = candidate["evidence_references"]
        assert isinstance(evidence, list)
        lines.extend([f"- `{item}`" for item in evidence] or ["- `Missing`"])
        lines.append("")

    lines.extend(["## Exclusions and limits", ""])
    exclusions = report["exclusion_counts"]
    assert isinstance(exclusions, dict)
    lines.extend([f"- {key}: `{value}`" for key, value in exclusions.items()] or ["- None"])
    lines.extend(
        [
            f"- Returned: `{len(candidates)}` / `{limits['max_results']}` maximum results",
            f"- Returned characters: `{limits['returned_chars']}` / `{limits['max_total_chars']}`",
            "",
            "## Warnings",
            "",
        ]
    )
    warnings = report["warnings"]
    assert isinstance(warnings, list)
    lines.extend([f"- {warning}" for warning in warnings] or ["- None"])
    lines.extend(
        [
            "",
            "## Generation provenance",
            "",
            "- Engine: `deterministic-bm25-lexical-v1`",
            "- Embeddings: `false`",
            "- Model inference: `false`",
            "- Automatic promotion: `false`",
            "",
        ]
    )
    return "\n".join(lines)


def write_pattern_memory_report(
    report: dict[str, object],
    output: str | Path,
    *,
    format: str,
    force: bool = False,
    repo: str | Path | None = None,
) -> Path:
    root = Path(repo or repository_root()).resolve()
    destination = Path(output)
    if not destination.is_absolute():
        destination = root / destination
    destination = destination.resolve()
    _validate_output_path(root, destination)
    if destination.exists() and not force:
        raise FileExistsError(f"Output already exists: {destination}")
    rendered = render_pattern_memory_json(report) if format == "json" else render_pattern_memory_markdown(report)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return destination


def verify_source_reference(repo: str | Path, candidate: dict[str, object]) -> bool:
    corpus = compile_corpus(repo)
    return any(
        source.candidate_id == candidate.get("candidate_id")
        and source.source_reference == candidate.get("source_reference")
        and source.content_hash == candidate.get("content_hash")
        for source in corpus.candidates
    )


def _parse_learning_ledger(root: Path, path: Path, exclusions: Counter[str]) -> list[PatternSource]:
    text = path.read_text(encoding="utf-8")
    privacy = scan_text(text)
    if privacy:
        raise PatternMemoryError("Recursive learning ledger failed privacy scan: " + ", ".join(sorted(set(privacy))))
    candidates: list[PatternSource] = []
    seen: set[str] = set()
    in_ledger = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip() == "## Ledger":
            in_ledger = True
            continue
        if in_ledger and line.startswith("## "):
            break
        if not in_ledger:
            continue
        if not line.startswith("| RL-"):
            continue
        cells = _markdown_cells(line)
        if len(cells) != 9 or not LEARNING_ID_RE.fullmatch(cells[0]):
            raise PatternMemoryError(f"Malformed recursive-learning row at line {number}")
        learning_id, _opened, signal, learning, decision, durable, evidence, outcome, state = cells
        state = state.strip().lower()
        if learning_id in seen:
            raise PatternMemoryError(f"Duplicate recursive-learning ID: {learning_id}")
        seen.add(learning_id)
        if state not in ELIGIBLE_LEARNING_STATES:
            exclusions[f"ineligible-learning-state:{state or 'missing'}"] += 1
            continue
        source_text = "\n\n".join(
            [
                f"Signal: {signal}",
                f"Learning: {learning}",
                f"Decision: {decision}",
                f"Durable surface: {durable}",
                f"Evidence: {evidence}",
                f"Outcome: {outcome}",
            ]
        )
        classification, approval = _classify(source_text, provisional=False)
        if classification == "keep local":
            exclusions["membrane-keep-local"] += 1
            continue
        content_hash = _sha256(source_text)
        source_ref = f"{path.relative_to(root).as_posix()}#{learning_id}"
        evidence_refs = tuple(sorted(set(LINK_RE.findall(" ".join(cells[2:8])))))
        candidates.append(
            PatternSource(
                source_tier="governed-learning",
                source_lane="repository-learning",
                source_reference=source_ref,
                section=learning_id,
                text=source_text,
                transformed_pattern=learning,
                learning_state=state,
                evidence_references=evidence_refs,
                content_hash=content_hash,
                candidate_id=_candidate_id(source_ref, content_hash),
                membrane_classification=classification,
                required_approval=approval,
            )
        )
    return candidates


def _parse_project_document(root: Path, path: Path, lane: str) -> tuple[list[PatternSource], Counter[str]]:
    text = path.read_text(encoding="utf-8")
    privacy = scan_text(text)
    if privacy:
        return [], Counter({"privacy-source": 1})
    candidates: list[PatternSource] = []
    exclusions: Counter[str] = Counter()
    relative = path.relative_to(root).as_posix()
    for section, chunk in _markdown_chunks(text):
        if len(chunk) < 24:
            exclusions["short-project-chunk"] += 1
            continue
        classification, approval = _classify(chunk, provisional=True)
        if classification == "keep local":
            exclusions["membrane-keep-local"] += 1
            continue
        source_ref = f"{relative}#{_slug(section)}"
        content_hash = _sha256(chunk)
        candidates.append(
            PatternSource(
                source_tier="project-provisional",
                source_lane=lane,
                source_reference=source_ref,
                section=section,
                text=chunk,
                transformed_pattern=_transform_project_pattern(chunk, lane),
                learning_state=None,
                evidence_references=(relative,),
                content_hash=content_hash,
                candidate_id=_candidate_id(source_ref, content_hash),
                membrane_classification=classification,
                required_approval=approval,
            )
        )
    return candidates, exclusions


def _rank(
    candidates: Iterable[PatternSource], query: str, target_lane: str
) -> list[tuple[PatternSource, float]]:
    candidate_list = list(candidates)
    documents = [_tokens(" ".join([item.section, item.source_lane, item.text])) for item in candidate_list]
    query_tokens = _tokens(query)
    if not query_tokens:
        raise PatternMemoryError("Query must contain a lexical token")
    document_frequency: Counter[str] = Counter()
    for tokens in documents:
        document_frequency.update(set(tokens))
    average_length = sum(len(tokens) for tokens in documents) / max(1, len(documents))
    query_lower = query.lower()
    lane_lower = target_lane.lower()
    ranked: list[tuple[PatternSource, float]] = []
    for source, tokens in zip(candidate_list, documents):
        frequencies = Counter(tokens)
        score = 0.0
        for token in query_tokens:
            frequency = frequencies[token]
            if not frequency:
                continue
            df = document_frequency[token]
            idf = math.log(1.0 + (len(documents) - df + 0.5) / (df + 0.5))
            denominator = frequency + 1.2 * (1.0 - 0.75 + 0.75 * len(tokens) / max(1.0, average_length))
            score += idf * (frequency * 2.2) / denominator
        searchable = " ".join([source.section, source.source_lane, source.text]).lower()
        if query_lower in searchable:
            score += 4.0
        if query_lower.startswith("rl-") and query_lower in source.source_reference.lower():
            score += 12.0
        if query_lower in source.section.lower():
            score += 2.0
        if lane_lower and lane_lower in source.source_lane.lower():
            score += 1.0
        if score > 0:
            ranked.append((source, score))
    tier_order = {"governed-learning": 0, "project-provisional": 1}
    ranked.sort(
        key=lambda item: (
            -item[1],
            tier_order[item[0].source_tier],
            item[0].source_reference,
            item[0].candidate_id,
        )
    )
    return ranked


def _classify(text: str, *, provisional: bool) -> tuple[str, str]:
    lowered = text.lower()
    if any(term in lowered for term in KEEP_LOCAL_TERMS):
        return "keep local", "owner/operator"
    if any(term in lowered for term in PROFESSIONAL_TERMS):
        return "professional review required", "professional review"
    if any(term in lowered for term in APPROVAL_TERMS):
        return "approval required", "owner/operator"
    if provisional:
        return "translate first", "human membrane review"
    return "safe to transfer", "none"


def _markdown_chunks(text: str) -> Iterable[tuple[str, str]]:
    section = "Document"
    paragraph: list[str] = []
    in_code = False

    def flush() -> tuple[str, str] | None:
        if not paragraph:
            return None
        value = " ".join(part.strip() for part in paragraph if part.strip()).strip()
        paragraph.clear()
        return (section, value) if value else None

    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            item = flush()
            if item:
                yield item
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith("#"):
            item = flush()
            if item:
                yield item
            section = stripped.lstrip("#").strip() or "Document"
            continue
        if stripped.startswith("|") or stripped in {"---", "***"}:
            item = flush()
            if item:
                yield item
            continue
        if re.match(r"^(?:[-*+] |\d+[.)] )", stripped):
            item = flush()
            if item:
                yield item
            value = re.sub(r"^(?:[-*+] |\d+[.)] )", "", stripped).strip()
            if value:
                yield section, value
            continue
        if not stripped:
            item = flush()
            if item:
                yield item
            continue
        paragraph.append(stripped)
    item = flush()
    if item:
        yield item


def _tracked_paths(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise PatternMemoryError(result.stderr.strip() or "git ls-files failed")
    return {line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()}


def _prohibited_source(relative: str) -> bool:
    parts = {part.lower() for part in Path(relative).parts}
    if parts & PROHIBITED_SOURCE_PARTS:
        return True
    lowered = relative.lower()
    return any(part in lowered for part in PROHIBITED_PATH_PARTS)


def _validate_output_path(root: Path, destination: Path) -> None:
    if _is_within(destination, root):
        generated = (root / "generated-patterns").resolve()
        if not _is_within(destination, generated) or destination == generated:
            raise PatternMemoryError("Repository-local reports must be written beneath generated-patterns/")
    if destination.suffix.lower() not in {".md", ".json"}:
        raise PatternMemoryError("Pattern-memory output must use .md or .json")


def _validate_as_of(value: str) -> None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PatternMemoryError("As-of must be an ISO 8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise PatternMemoryError("As-of timestamp must include a UTC offset")


def _markdown_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def _transform_project_pattern(text: str, lane: str) -> str:
    transformed = re.sub(re.escape(lane), "the source project", text, flags=re.IGNORECASE)
    display_name = lane.replace("-", " ")
    transformed = re.sub(re.escape(display_name), "the source project", transformed, flags=re.IGNORECASE)
    return transformed


def _truncate(text: str, maximum: int) -> tuple[str, bool]:
    if len(text) <= maximum:
        return text, False
    if maximum <= 1:
        return "…"[:maximum], True
    return text[: maximum - 1].rstrip() + "…", True


def _candidate_id(source_reference: str, content_hash: str) -> str:
    return "PMC-" + _sha256(f"{source_reference}:{content_hash}")[:16].upper()


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "document"


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False
