from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


PROHIBITED_PATH_PARTS = ("tenant-private", "customer-private", "raw-customer-transcripts")
PROHIBITED_FILENAMES = ("intake-operator-summary", "30-day-plan-input-draft")
CONTENT_RULES = {
    "known-child-identifier": re.compile(r"\bAbigail\b", re.IGNORECASE),
    "email-address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "us-phone-number": re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)"),
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential-assignment": re.compile(r"(?i)\b(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}"),
}
TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".py", ".csv", ".tsv"}
SYNTHETIC_FIXTURE_MARKERS = (
    "privacy_class: synthetic-fixture",
    "synthetic/pseudonymous fixture",
)


@dataclass(frozen=True)
class PrivacyFinding:
    path: str
    rule: str
    line: int | None


def tracked_files(repo_root: str | Path) -> list[Path]:
    root = Path(repo_root).resolve()
    files: list[str] = []
    for args in (("ls-files",), ("ls-files", "--others", "--exclude-standard")):
        result = subprocess.run(
            ["git", *args], cwd=root, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
        files.extend(line for line in result.stdout.splitlines() if line.strip())
    return [root / line for line in sorted(set(files))]


def scan_repo(repo_root: str | Path) -> list[PrivacyFinding]:
    root = Path(repo_root).resolve()
    findings: list[PrivacyFinding] = []
    for path in tracked_files(root):
        if not path.exists():
            # A tracked deletion is already quarantined in the working tree.
            continue
        relative = path.relative_to(root).as_posix()
        lowered = relative.lower()
        for part in PROHIBITED_PATH_PARTS:
            if part in lowered:
                findings.append(PrivacyFinding(relative, f"prohibited-path:{part}", None))
        for name in PROHIBITED_FILENAMES:
            if name in lowered:
                findings.append(PrivacyFinding(relative, f"prohibited-filename:{name}", None))
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        synthetic_fixture = _is_synthetic_fixture(lines)
        for number, line in enumerate(lines, 1):
            for rule, pattern in CONTENT_RULES.items():
                if rule == "known-child-identifier" and synthetic_fixture:
                    continue
                if pattern.search(line):
                    findings.append(PrivacyFinding(relative, rule, number))
    return findings


def scan_text(text: str) -> list[str]:
    """Return content-rule names without echoing potentially sensitive text."""
    return [rule for rule, pattern in CONTENT_RULES.items() if pattern.search(text)]


def _is_synthetic_fixture(lines: list[str]) -> bool:
    sample = "\n".join(lines[:20]).lower()
    return any(marker in sample for marker in SYNTHETIC_FIXTURE_MARKERS)


def render_findings(findings: list[PrivacyFinding]) -> str:
    if not findings:
        return "Privacy scan passed: no prohibited tracked content found.\n"
    lines = ["Privacy scan failed:"]
    for finding in findings:
        location = f":{finding.line}" if finding.line else ""
        lines.append(f"- {finding.path}{location} [{finding.rule}]")
    return "\n".join(lines) + "\n"
