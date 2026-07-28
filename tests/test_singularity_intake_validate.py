from anyang_loop.singularity_intake_validate import validate_lane


def _packet(root, stem="2026-01-01-example", disposition="lane-test-ready", rights="internal research only"):
    lane = root / "lane"
    for name in ("transcripts", "source-notes", "analyses"):
        (lane / name).mkdir(parents=True)
    (lane / "transcripts" / f"{stem}.md").write_text(f"Rights status: {rights}\n", encoding="utf-8")
    (lane / "source-notes" / f"{stem}.source-note.md").write_text(
        "Rights status: internal research only\nIntake tier: standard\n", encoding="utf-8"
    )
    (lane / "analyses" / f"{stem}.analysis.md").write_text(
        f"Intake tier: standard\nWhat changed: example\nReusable mechanism: example\nDecision implication: test\n"
        f"Evidence still missing: test\nRecommended disposition: {disposition}\n"
        f"ROI disposition: `{disposition}`\n\n"
        "Source episode: example\nSeam: example\nTransferable question or checklist: test\n"
        "Receiving lane: internal\nMembrane classification: internal\nHuman authority required: owner\n"
        "Evidence still needed: test\nWhat stays inside Singularity Science: source\n",
        encoding="utf-8",
    )
    (lane / "roi-ledger.md").write_text(stem, encoding="utf-8")
    return lane


def test_complete_lane_passes(tmp_path):
    assert validate_lane(_packet(tmp_path)) == []


def test_missing_packet_artifact_fails(tmp_path):
    lane = _packet(tmp_path)
    (lane / "source-notes" / "2026-01-01-example.source-note.md").unlink()
    assert any(item.code == "intake-source-note-missing" for item in validate_lane(lane))


def test_invalid_disposition_fails(tmp_path):
    lane = _packet(tmp_path, disposition="adopted")
    assert any(item.code == "intake-disposition-invalid" for item in validate_lane(lane))


def test_lane_test_ready_requires_routing_packet(tmp_path):
    lane = _packet(tmp_path)
    analysis = lane / "analyses" / "2026-01-01-example.analysis.md"
    analysis.write_text("ROI disposition: `lane-test-ready`\n", encoding="utf-8")
    assert any(item.code == "intake-routing-packet-incomplete" for item in validate_lane(lane))


def test_captured_transcript_pairs_with_uncaptured_note_and_analysis(tmp_path):
    lane = _packet(tmp_path, stem="2026-01-01-captured-example")
    assert validate_lane(lane) == []


def test_public_web_capture_rights_are_accepted(tmp_path):
    assert validate_lane(_packet(tmp_path, rights="public web capture; do not republish source text")) == []


def test_prose_does_not_create_invalid_disposition(tmp_path):
    lane = _packet(tmp_path)
    analysis = lane / "analyses" / "2026-01-01-example.analysis.md"
    analysis.write_text(analysis.read_text(encoding="utf-8") + "Possible primitive candidate; preserve rhetoric.\n", encoding="utf-8")
    assert not any(item.code == "intake-disposition-invalid" for item in validate_lane(lane))


def test_retained_source_requires_review_fields(tmp_path):
    lane = _packet(tmp_path)
    analysis = lane / "analyses" / "2026-01-01-example.analysis.md"
    analysis.write_text(analysis.read_text(encoding="utf-8") + "Current status: watch\n", encoding="utf-8")
    assert any(item.code == "intake-retention-fields-missing" for item in validate_lane(lane))


def test_retained_source_with_review_fields_passes(tmp_path):
    lane = _packet(tmp_path)
    fields = (
        "Retention reason: weak but consequential signal\nCurrent status: watch\n"
        "Evidence missing: independent corroboration\nRevisit trigger: second source\n"
        "Review owner: Engineer\nNext review date: 2026-08-15\nPotential receiving lane: internal\n"
    )
    analysis = lane / "analyses" / "2026-01-01-example.analysis.md"
    analysis.write_text(analysis.read_text(encoding="utf-8") + fields, encoding="utf-8")
    assert validate_lane(lane) == []


def test_feedback_outcome_is_controlled(tmp_path):
    lane = _packet(tmp_path)
    analysis = lane / "analyses" / "2026-01-01-example.analysis.md"
    analysis.write_text(analysis.read_text(encoding="utf-8") + "Outcome after review: adopted\n", encoding="utf-8")
    assert validate_lane(lane) == []


def test_fixture_skips_production_decision_requirements(tmp_path):
    lane = _packet(tmp_path)
    analysis = lane / "analyses" / "2026-01-01-gated-fixture-example.analysis.md"
    transcript = lane / "transcripts" / "2026-01-01-gated-fixture-example.md"
    note = lane / "source-notes" / "2026-01-01-gated-fixture-example.source-note.md"
    transcript.write_text("Synthetic gated fixture; rights status: fixture-only\n", encoding="utf-8")
    note.write_text("Rights status: fixture-only\n", encoding="utf-8")
    analysis.write_text("Synthetic gated fixture; gate disposition: promote-to-singularity-source-note\n", encoding="utf-8")
    assert not any(item.code == "intake-decision-compression-incomplete" for item in validate_lane(lane))
