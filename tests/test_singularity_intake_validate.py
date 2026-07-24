from anyang_loop.singularity_intake_validate import validate_lane


def _packet(root, stem="2026-01-01-example", disposition="lane-test-ready"):
    lane = root / "lane"
    for name in ("transcripts", "source-notes", "analyses"):
        (lane / name).mkdir(parents=True)
    (lane / "transcripts" / f"{stem}.md").write_text("Rights status: internal research only\n", encoding="utf-8")
    (lane / "source-notes" / f"{stem}.source-note.md").write_text("Rights status: internal research only\n", encoding="utf-8")
    (lane / "analyses" / f"{stem}.analysis.md").write_text(
        f"What changed: example\nReusable mechanism: example\nDecision implication: test\n"
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
