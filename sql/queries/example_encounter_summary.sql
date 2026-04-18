-- Example: monthly encounter counts by type (parameterize database/schema).
-- :start_date / :end_date would be bound by your runner or BI tool.

SELECT
    DATE_TRUNC('month', encounter_start_ts) AS encounter_month,
    encounter_type_code,
    COUNT(*) AS encounter_count
FROM fact_encounter
WHERE encounter_start_ts >= :start_date
  AND encounter_start_ts < :end_date
GROUP BY 1, 2
ORDER BY 1, 2;
