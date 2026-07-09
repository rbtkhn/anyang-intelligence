from pathlib import Path
import tempfile

from anyang_loop.catalog_import import import_catalog, render_catalog_completion_report
from anyang_loop.install_cli import main


def write_catalog_manifest(path: Path) -> Path:
    manifest = path / "customers" / "elementary-school" / "catalog" / "khan-catalog-manifest.yaml"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "catalog_entries:\n"
        "  - stable_id: khan-main-math\n"
        "    source_product: khan_academy_main_catalog\n"
        "    title: Khan Academy math\n"
        "    subject_domain: Math\n"
        "    age_grade_band: kindergarten through high school\n"
        "    standards_tags:\n"
        "      - common-core\n"
        "    content_type: domain\n"
        "    source_url: https://www.khanacademy.org/math\n"
        "    source_note: Official main Khan Academy math landing area.\n"
        "    evidence_status: official-public-web\n"
        "    import_method: public-web-manifest\n"
        "    operator_notes: Broader reinforcement directory.\n"
        "  - stable_id: khan-kids-reading-literacy\n"
        "    source_product: khan_kids_curated_catalog\n"
        "    title: Khan Kids reading and literacy\n"
        "    subject_domain: Reading and literacy\n"
        "    age_grade_band: ages 2-8\n"
        "    standards_tags:\n"
        "      - head-start-elof\n"
        "      - common-core\n"
        "    content_type: domain\n"
        "    source_url: https://khankids.zendesk.com/hc/en-us/articles/360014856151-Learning-Topics-Using-Khan-Academy-Kids-in-Educational-Settings\n"
        "    source_note: Official Khan Kids learning topics article.\n"
        "    evidence_status: manual-curated\n"
        "    import_method: manual-curated\n"
        "    operator_notes: Starter-tool recommendation layer.\n"
        "  - stable_id: khan-main-missing-source\n"
        "    source_product: khan_academy_main_catalog\n"
        "    title: Missing Provenance\n"
        "    subject_domain: Math\n"
        "    age_grade_band: elementary\n"
        "    standards_tags: []\n"
        "    content_type: domain\n"
        "    source_url: \"\"\n"
        "    source_note: \"\"\n"
        "    evidence_status: official-public-web\n"
        "    import_method: public-web-manifest\n"
        "    operator_notes: This should fail provenance validation.\n",
        encoding="utf-8",
    )
    return manifest


def test_catalog_import_dry_run_and_report():
    tmp_path = Path(tempfile.mkdtemp())
    manifest = write_catalog_manifest(tmp_path)

    assert main(["import-catalog", "--manifest", str(manifest), "--dry-run"]) == 1
    assert not (manifest.parent / "imported" / "khan_academy_main_catalog" / "khan-main-math.md").exists()

    report = render_catalog_completion_report(import_catalog(manifest, dry_run=True))
    assert "Missing provenance rows: 1" in report
    assert "| khan_academy_main_catalog | 2 | 1 | 1 | 50% |" in report
    assert "| khan_kids_curated_catalog | 1 | 1 | 0 | 100% |" in report


def test_catalog_import_writes_files_and_ledger():
    tmp_path = Path(tempfile.mkdtemp())
    manifest = write_catalog_manifest(tmp_path)

    assert main(["import-catalog", "--manifest", str(manifest)]) == 1

    main_entry = manifest.parent / "imported" / "khan_academy_main_catalog" / "khan-main-math.md"
    kids_entry = manifest.parent / "imported" / "khan_kids_curated_catalog" / "khan-kids-reading-literacy.md"
    ledger = manifest.parent / "catalog-import-ledger.md"

    assert main_entry.exists()
    assert kids_entry.exists()
    assert ledger.exists()

    main_text = main_entry.read_text(encoding="utf-8")
    assert "source_product: khan_academy_main_catalog" in main_text
    assert "## Recommendation Boundary" in main_text
    assert "does not prove mastery" in main_text

    ledger_text = ledger.read_text(encoding="utf-8")
    assert "missing-source" in ledger_text
    assert "imported" in ledger_text


def test_catalog_import_duplicate_detection_and_no_overwrite():
    tmp_path = Path(tempfile.mkdtemp())
    manifest = tmp_path / "customers" / "elementary-school" / "catalog" / "khan-catalog-manifest.yaml"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "catalog_entries:\n"
        "  - stable_id: khan-main-math\n"
        "    source_product: khan_academy_main_catalog\n"
        "    title: Khan Academy math\n"
        "    subject_domain: Math\n"
        "    age_grade_band: kindergarten through high school\n"
        "    standards_tags: []\n"
        "    content_type: domain\n"
        "    source_url: https://www.khanacademy.org/math\n"
        "    source_note: Official main Khan Academy math landing area.\n"
        "    evidence_status: official-public-web\n"
        "    import_method: public-web-manifest\n",
        encoding="utf-8",
    )

    assert main(["import-catalog", "--manifest", str(manifest)]) == 0
    imported = manifest.parent / "imported" / "khan_academy_main_catalog" / "khan-main-math.md"
    original_text = imported.read_text(encoding="utf-8")

    manifest.write_text(
        "catalog_entries:\n"
        "  - stable_id: khan-main-math\n"
        "    source_product: khan_academy_main_catalog\n"
        "    title: Updated Khan Academy math\n"
        "    subject_domain: Math\n"
        "    age_grade_band: kindergarten through high school\n"
        "    standards_tags: []\n"
        "    content_type: domain\n"
        "    source_url: https://www.khanacademy.org/math\n"
        "    source_note: Official main Khan Academy math landing area.\n"
        "    evidence_status: official-public-web\n"
        "    import_method: public-web-manifest\n",
        encoding="utf-8",
    )
    assert main(["import-catalog", "--manifest", str(manifest)]) == 0
    assert imported.read_text(encoding="utf-8") == original_text


def test_catalog_import_validation_failures(capsys):
    tmp_path = Path(tempfile.mkdtemp())
    manifest = tmp_path / "customers" / "elementary-school" / "catalog" / "khan-catalog-manifest.yaml"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "catalog_entries:\n"
        "  - stable_id: invalid-product\n"
        "    source_product: not-a-real-product\n"
        "    title: Invalid Product\n"
        "    subject_domain: Math\n"
        "    age_grade_band: elementary\n"
        "    standards_tags: []\n"
        "    content_type: domain\n"
        "    source_url: https://example.com/invalid\n"
        "    source_note: Invalid product test.\n"
        "    evidence_status: official-public-web\n"
        "    import_method: public-web-manifest\n"
        "  - stable_id: \"\"\n"
        "    source_product: khan_academy_main_catalog\n"
        "    title: Missing Stable ID\n"
        "    subject_domain: Math\n"
        "    age_grade_band: elementary\n"
        "    standards_tags: []\n"
        "    content_type: domain\n"
        "    source_url: https://www.khanacademy.org/math\n"
        "    source_note: Missing id test.\n"
        "    evidence_status: official-public-web\n"
        "    import_method: public-web-manifest\n"
        "  - stable_id: wrong-kids-method\n"
        "    source_product: khan_kids_curated_catalog\n"
        "    title: Wrong Kids Method\n"
        "    subject_domain: Books\n"
        "    age_grade_band: ages 2-8\n"
        "    standards_tags: []\n"
        "    content_type: domain\n"
        "    source_url: https://khankids.zendesk.com/hc/en-us\n"
        "    source_note: Wrong import method test.\n"
        "    evidence_status: manual-curated\n"
        "    import_method: public-web-manifest\n",
        encoding="utf-8",
    )

    assert main(["import-catalog", "--manifest", str(manifest)]) == 1
    captured = capsys.readouterr()
    assert "Invalid source_product: not-a-real-product." in captured.out
    assert "Missing required fields: stable_id." in captured.out
    assert "khan_kids_curated_catalog rows may not use import_method public-web-manifest." in captured.out
