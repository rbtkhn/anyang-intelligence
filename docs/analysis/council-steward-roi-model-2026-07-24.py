"""Scenario model for the proposed Executive Council Steward position.

The model is assumption-driven because no measured Steward pilot baseline
exists yet. It intentionally excludes revenue uplift and catastrophic-risk
avoidance so that the estimate rests on time savings and routine rework only.
"""

from __future__ import annotations

import json


SCENARIOS = [
    {
        "scenario": "Conservative",
        "probability": 0.30,
        "reviews_per_month": 6,
        "minutes_saved_per_review": 15,
        "rework_events_avoided_per_month": 0.5,
        "hours_per_rework_event": 1.0,
        "human_review_hours_per_month": 2.0,
        "labor_value_per_hour": 75.0,
        "runtime_cost_per_month": 100.0,
        "setup_hours": 4.0,
    },
    {
        "scenario": "Base",
        "probability": 0.50,
        "reviews_per_month": 12,
        "minutes_saved_per_review": 30,
        "rework_events_avoided_per_month": 1.5,
        "hours_per_rework_event": 2.0,
        "human_review_hours_per_month": 2.0,
        "labor_value_per_hour": 100.0,
        "runtime_cost_per_month": 150.0,
        "setup_hours": 4.0,
    },
    {
        "scenario": "Upside",
        "probability": 0.20,
        "reviews_per_month": 18,
        "minutes_saved_per_review": 45,
        "rework_events_avoided_per_month": 3.0,
        "hours_per_rework_event": 3.0,
        "human_review_hours_per_month": 2.5,
        "labor_value_per_hour": 125.0,
        "runtime_cost_per_month": 250.0,
        "setup_hours": 5.0,
    },
]


def evaluate(scenario: dict[str, float | str]) -> dict[str, float | str]:
    reconstruction_hours = (
        float(scenario["reviews_per_month"])
        * float(scenario["minutes_saved_per_review"])
        / 60
    )
    rework_hours = (
        float(scenario["rework_events_avoided_per_month"])
        * float(scenario["hours_per_rework_event"])
    )
    benefit_hours_per_month = reconstruction_hours + rework_hours
    labor_value = float(scenario["labor_value_per_hour"])
    monthly_gross_benefit = benefit_hours_per_month * labor_value
    monthly_recurring_cost = (
        float(scenario["human_review_hours_per_month"]) * labor_value
        + float(scenario["runtime_cost_per_month"])
    )
    setup_cost = float(scenario["setup_hours"]) * labor_value
    year_one_benefit = monthly_gross_benefit * 12
    year_one_cost = setup_cost + monthly_recurring_cost * 12
    year_one_net_benefit = year_one_benefit - year_one_cost
    year_one_roi = year_one_net_benefit / year_one_cost
    monthly_net_after_setup = monthly_gross_benefit - monthly_recurring_cost
    payback_months = (
        setup_cost / monthly_net_after_setup
        if monthly_net_after_setup > 0
        else None
    )
    break_even_benefit_hours_per_month = (
        year_one_cost / 12 / labor_value
    )

    return {
        **scenario,
        "reconstruction_hours_saved_per_month": round(reconstruction_hours, 2),
        "rework_hours_avoided_per_month": round(rework_hours, 2),
        "benefit_hours_per_month": round(benefit_hours_per_month, 2),
        "monthly_gross_benefit": round(monthly_gross_benefit, 2),
        "monthly_recurring_cost": round(monthly_recurring_cost, 2),
        "year_one_benefit": round(year_one_benefit, 2),
        "year_one_cost": round(year_one_cost, 2),
        "year_one_net_benefit": round(year_one_net_benefit, 2),
        "year_one_roi": round(year_one_roi, 4),
        "payback_months": round(payback_months, 2)
        if payback_months is not None
        else None,
        "break_even_benefit_hours_per_month": round(
            break_even_benefit_hours_per_month, 2
        ),
    }


scenario_results = [evaluate(scenario) for scenario in SCENARIOS]

expected_year_one_benefit = sum(
    float(row["probability"]) * float(row["year_one_benefit"])
    for row in scenario_results
)
expected_year_one_cost = sum(
    float(row["probability"]) * float(row["year_one_cost"])
    for row in scenario_results
)
expected_year_one_net_benefit = (
    expected_year_one_benefit - expected_year_one_cost
)
expected_year_one_roi = expected_year_one_net_benefit / expected_year_one_cost

weighted_expected = {
    "expected_year_one_benefit": round(expected_year_one_benefit, 2),
    "expected_year_one_cost": round(expected_year_one_cost, 2),
    "expected_year_one_net_benefit": round(expected_year_one_net_benefit, 2),
    "expected_year_one_roi": round(expected_year_one_roi, 4),
    "assumption_weighted_probability_of_positive_roi": 0.70,
}

model_output = {
    "as_of": "2026-07-24",
    "portfolio_projects": 6,
    "repository_project_files_observed": 458,
    "scenarios": scenario_results,
    "weighted_expected": weighted_expected,
    "excluded_from_value": [
        "revenue uplift",
        "major privacy or authority incident avoidance",
        "customer trust or retention effects",
        "cross-project learning value beyond routine time savings",
    ],
}

if __name__ == "__main__":
    print(json.dumps(model_output, indent=2))
