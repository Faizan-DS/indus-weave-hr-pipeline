-- Q2: Monthly attrition rate by department
SELECT department, COUNT(emp_id) AS separations FROM stg_employees WHERE separation_date IS NOT NULL GROUP BY 1;