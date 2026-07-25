from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def test_recurring_revenue_baseline_has_one_current_source():
    revenue = read(
        ROOT
        / "docs/"
        "anyang-intelligence-recurring-revenue-baseline-2026-07-25.md"
    )

    assert "| Grace Gems | `$1,000` |" in revenue
    assert "| **Total MRR** | **`$1,000`** |" in revenue
    assert "Learning Core's monthly continuity subscription remains an unvalidated" in revenue
    assert "contributes `$0` to current MRR" in revenue


def test_revenue_and_cost_baselines_reconcile_without_spend_authority():
    revenue = read(
        ROOT
        / "docs/"
        "anyang-intelligence-recurring-revenue-baseline-2026-07-25.md"
    )
    costs = read(
        ROOT
        / "docs/"
        "anyang-intelligence-monthly-operating-cost-baseline-2026-07-25.md"
    )
    dashboard = read(ROOT / "projects/operating-portfolio-dashboard.md")

    for expected in (
        "| Recurring revenue | `$1,000` | `$12,000` |",
        "| Operating-cost baseline | `$14,000` | `$168,000` |",
        "| Uncovered planning requirement | `$13,000` | `$156,000` |",
        "| Recurring-revenue coverage | `7.1%` | `7.1%` |",
    ):
        assert expected in revenue

    assert "`$13,000/month` uncovered planning requirement" in costs
    assert "Current Anyang Intelligence MRR is `$1,000/month`" in dashboard
    assert "leaves a" in dashboard and "`$13,000/month` uncovered" in dashboard
    assert "authorize a funding action" in costs
