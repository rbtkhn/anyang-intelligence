WITH scenarios (
    scenario,
    sort_order,
    probability,
    reviews_per_month,
    minutes_saved_per_review,
    rework_events_avoided_per_month,
    hours_per_rework_event,
    human_review_hours_per_month,
    labor_value_per_hour,
    runtime_cost_per_month,
    setup_hours
) AS (
    VALUES
        ('Conservative', 1, 0.30, 6, 15, 0.5, 1.0, 2.0, 75.0, 100.0, 4.0),
        ('Base',         2, 0.50, 12, 30, 1.5, 2.0, 2.0, 100.0, 150.0, 4.0),
        ('Upside',       3, 0.20, 18, 45, 3.0, 3.0, 2.5, 125.0, 250.0, 5.0)
),
evaluated AS (
    SELECT
        *,
        reviews_per_month * minutes_saved_per_review / 60.0
            + rework_events_avoided_per_month * hours_per_rework_event
            AS benefit_hours_per_month,
        setup_hours * labor_value_per_hour
            + 12.0 * (
                human_review_hours_per_month * labor_value_per_hour
                + runtime_cost_per_month
            )
            AS year_one_cost
    FROM scenarios
),
scenario_results AS (
    SELECT
        scenario AS outcome,
        'Scenario' AS outcome_type,
        sort_order,
        probability,
        reviews_per_month,
        minutes_saved_per_review,
        rework_events_avoided_per_month,
        hours_per_rework_event,
        human_review_hours_per_month,
        labor_value_per_hour,
        runtime_cost_per_month,
        setup_hours,
        benefit_hours_per_month,
        12.0 * benefit_hours_per_month * labor_value_per_hour
            AS year_one_benefit,
        year_one_cost,
        12.0 * benefit_hours_per_month * labor_value_per_hour
            - year_one_cost
            AS year_one_net_benefit,
        (
            12.0 * benefit_hours_per_month * labor_value_per_hour
            - year_one_cost
        ) / year_one_cost
            AS year_one_roi,
        year_one_cost / 12.0 / labor_value_per_hour
            AS break_even_benefit_hours_per_month
    FROM evaluated
),
weighted_expected AS (
    SELECT
        'Weighted expected' AS outcome,
        'Probability-weighted' AS outcome_type,
        4 AS sort_order,
        1.0 AS probability,
        NULL AS reviews_per_month,
        NULL AS minutes_saved_per_review,
        NULL AS rework_events_avoided_per_month,
        NULL AS hours_per_rework_event,
        NULL AS human_review_hours_per_month,
        NULL AS labor_value_per_hour,
        NULL AS runtime_cost_per_month,
        NULL AS setup_hours,
        NULL AS benefit_hours_per_month,
        SUM(probability * year_one_benefit) AS year_one_benefit,
        SUM(probability * year_one_cost) AS year_one_cost,
        SUM(probability * year_one_net_benefit) AS year_one_net_benefit,
        SUM(probability * year_one_net_benefit)
            / SUM(probability * year_one_cost)
            AS year_one_roi,
        NULL AS break_even_benefit_hours_per_month
    FROM scenario_results
)
SELECT *
FROM (
    SELECT * FROM scenario_results
    UNION ALL
    SELECT * FROM weighted_expected
)
ORDER BY sort_order;
