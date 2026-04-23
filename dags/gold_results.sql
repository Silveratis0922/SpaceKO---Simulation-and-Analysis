SELECT
    COUNT(*)                                                                                       AS nb_tournaments,
    ROUND(AVG(estimate_dotation)::numeric, 2)                                                      AS avg_estimate_dotation,
    ROUND(AVG(total_dotation)::numeric, 2)                                                         AS avg_total_dotation,
    ROUND(AVG(total_dotation - estimate_dotation)::numeric, 2)                                     AS avg_variance,
    ROUND(AVG(total_dotation / estimate_dotation)::numeric, 4)                                     AS avg_ratio,
    SUM(CASE WHEN total_dotation > estimate_dotation THEN 1 ELSE 0 END)                            AS nb_above_estimate,
    ROUND(SUM(CASE WHEN total_dotation > estimate_dotation THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_above_estimate
FROM {{source('public', 'silver_results')}}