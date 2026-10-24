-- Q3: Absenteeism rate by plant and month
SELECT status, COUNT(*) AS total FROM stg_attendance_daily GROUP BY 1;