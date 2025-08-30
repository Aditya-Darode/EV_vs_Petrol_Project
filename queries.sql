-- ========================================================
-- EV vs Petrol Cars in India (2019–2025)
-- SQL Queries executed in Google BigQuery
-- ========================================================
-- Note:
-- Replace `your_project_id` with your actual Google Cloud Project ID.
-- Replace `your_dataset_name` with the dataset you created in BigQuery 
-- These queries were used to transform raw PyTrends data into 
-- insights and generate processed CSVs for visualization.
-- ========================================================


-- --------------------------------------------------------
-- 1. Monthly Trend (Optional)
-- Purpose:
--   Aggregate raw daily Google Trends data into MONTHLY averages
--   to visualize EV vs Petrol adoption trends over time.
-- Output:
--   ev_avg (average EV search interest per month)
--   petrol_avg (average Petrol search interest per month)
-- --------------------------------------------------------
SELECT
  DATE_TRUNC(date, MONTH) AS month,
  AVG(`Electric Cars`) AS ev_avg,
  AVG(`Petrol Cars`) AS petrol_avg
FROM `your_project_id.your_dataset_name.ev_vs_petrol_timeseries`
GROUP BY month
ORDER BY month;


-- --------------------------------------------------------
-- 2. Year-over-Year Growth (MAIN QUERY)
-- Purpose:
--   Calculate Year-over-Year % Growth for EV and Petrol.
--   This is the ACTUAL query used to generate 
--   ev_vs_petrol_yoy.csv (used in Python + Streamlit charts).
-- Output:
--   year | total_ev | total_petrol | ev_yoy_pct | petrol_yoy_pct
-- --------------------------------------------------------
WITH yearly AS (
  SELECT 
    EXTRACT(YEAR FROM date) AS year,
    SUM(`Electric Cars`) AS total_ev,
    SUM(`Petrol Cars`) AS total_petrol
  FROM `your_project_id.your_dataset_name.ev_vs_petrol_timeseries`
  GROUP BY year
  ORDER BY year
),
yoy AS (
  SELECT
    year,
    total_ev,
    total_petrol,
    ROUND(100 * (total_ev - LAG(total_ev) OVER (ORDER BY year)) 
          / LAG(total_ev) OVER (ORDER BY year), 2) AS ev_yoy_pct,
    ROUND(100 * (total_petrol - LAG(total_petrol) OVER (ORDER BY year)) 
          / LAG(total_petrol) OVER (ORDER BY year), 2) AS petrol_yoy_pct
  FROM yearly
)
SELECT * 
FROM yoy;


-- --------------------------------------------------------
-- 3. Top States by EV Interest (Optional)
-- Purpose:
--   Rank Indian states by EV search interest share (%).
--   Useful for regional adoption insights.
-- Output:
--   state | ev | petrol | ev_share_pct
-- --------------------------------------------------------
SELECT
  geoName AS state,
  `Electric Cars` AS ev,
  `Petrol Cars` AS petrol,
  ROUND(SAFE_DIVIDE(`Electric Cars`, `Electric Cars` + `Petrol Cars`) * 100, 2) AS ev_share_pct
FROM `your_project_id.your_dataset_name.ev_vs_petrol_regions`
ORDER BY ev_share_pct DESC
LIMIT 10;
