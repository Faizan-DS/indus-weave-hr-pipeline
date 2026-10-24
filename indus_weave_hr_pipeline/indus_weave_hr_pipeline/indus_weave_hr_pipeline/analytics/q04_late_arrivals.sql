-- Q4: Top 10 employees with most late arrivals
SELECT emp_id, COUNT(*) AS late_count FROM stg_attendance_daily WHERE late_minutes > 0 GROUP BY 1 ORDER BY 2 DESC LIMIT 10;