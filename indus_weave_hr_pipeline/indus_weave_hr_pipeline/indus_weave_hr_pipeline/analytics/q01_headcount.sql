-- Q1: Month-end headcount by plant and department
SELECT SUBSTR(separation_date, 1, 7) AS month, department, COUNT(DISTINCT emp_id) AS headcount FROM stg_employees GROUP BY 1, 2;