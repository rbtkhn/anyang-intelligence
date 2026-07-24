from anyang_loop.recurrence_validate import validate_directory, validate_packet


VALID = """# Review
- Review ID: `REC-1`
- Review date: 2026-07-24
- New source: [source](source.md)
- Archive lane: `test`
- Canonical ledger: [ledger](ledger.md)
- Source identity and provenance: complete
- Rights status: internal

## Seam review
| Seam ID | New seam | Matched prior seams | Independence assessment | Recurrence count | Judgment | Evidence strength | Uncertainty | Disposition |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| `SEAM-1` | context | prior | independent | 2 | strengthening | medium | test | verify |

## Required next actions
- Evidence gap: test
## Performance baseline
- Comparison minutes: unavailable
"""


def make_packet(tmp_path, text=VALID):
    path = tmp_path / "review.md"
    path.write_text(text, encoding="utf-8")
    (tmp_path / "source.md").write_text("source", encoding="utf-8")
    (tmp_path / "ledger.md").write_text("ledger", encoding="utf-8")
    return path


def test_valid_packet_passes(tmp_path):
    assert validate_packet(make_packet(tmp_path)) == []


def test_missing_field_fails(tmp_path):
    assert any(item.code == "recurrence-field-missing" for item in validate_packet(make_packet(tmp_path, VALID.replace("- Rights status: internal\n", ""))))


def test_duplicate_seam_fails(tmp_path):
    duplicate = VALID + "\n| `SEAM-1` | duplicate | prior | independent | 2 | none | low | test | drop |\n"
    assert any(item.code == "recurrence-seam-duplicate" for item in validate_packet(make_packet(tmp_path, duplicate)))


def test_missing_link_fails(tmp_path):
    assert any(item.code == "recurrence-link-missing" for item in validate_packet(make_packet(tmp_path, VALID.replace("(source.md)", "(missing.md)"))))


def test_empty_directory_fails(tmp_path):
    assert any(item.code == "recurrence-packets-missing" for item in validate_directory(tmp_path))
