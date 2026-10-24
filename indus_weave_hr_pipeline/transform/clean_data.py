import sqlite3
import pandas as pd
import os

DB_PATH = "hr_pipeline.db"

def clean_and_transform():
    conn = sqlite3.connect(DB_PATH)
    
    print("--- Stage 2: Cleaning Employees & Handling Duplicates ---")
    if "raw_employees" in [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
        df_emp = pd.read_sql("SELECT * FROM raw_employees", conn)
        if "updated_at" in df_emp.columns:
            df_emp["updated_at"] = pd.to_datetime(df_emp["updated_at"], errors="coerce")
            df_emp = df_emp.sort_values("updated_at", ascending=False)
        df_emp_clean = df_emp.drop_duplicates(subset=["emp_id"], keep="first").copy()
        df_emp_clean["department"] = df_emp_clean["department"].str.strip().str.title()
        df_emp_clean.to_sql("stg_employees", conn, if_exists="replace", index=False)
    
    print("--- Stage 2 & 3: Processing Biometric Punches & Attendance ---")
    if "raw_biometric_punches" in [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
        df_punches = pd.read_sql("SELECT * FROM raw_biometric_punches", conn)
        df_devices = pd.read_sql("SELECT * FROM raw_device_mapping", conn)
        
        df_merged = pd.merge(df_punches, df_devices, on=["device_id", "device_user_id"], how="left")
        df_rejected = df_merged[df_merged["emp_id"].isnull()].copy()
        df_rejected["rejection_reason"] = "Unmapped contractor or visitor device ID"
        df_rejected.to_sql("stg_rejected_punches", conn, if_exists="replace", index=False)
        
        df_valid = df_merged[df_merged["emp_id"].notnull()].copy()
        df_valid["punch_time"] = pd.to_datetime(df_valid["punch_time"])
        df_valid = df_valid.sort_values(["emp_id", "punch_time"])
        df_valid["prev_punch_time"] = df_valid.groupby("emp_id")["punch_time"].shift(1)
        df_valid["time_diff_mins"] = (df_valid["punch_time"] - df_valid["prev_punch_time"]).dt.total_seconds() / 60
        
        df_clean = df_valid[(df_valid["time_diff_mins"].isnull()) | (df_valid["time_diff_mins"] > 2)].copy()
        df_clean.to_sql("stg_biometric_punches", conn, if_exists="replace", index=False)
        
        df_clean["punch_date"] = df_clean["punch_time"].dt.date
        att_summary = df_clean.groupby(["emp_id", "punch_date"]).agg(
            check_in=("punch_time", "min"),
            check_out=("punch_time", "max"),
            total_punches=("punch_time", "count")
        ).reset_index()
        
        att_summary["status"] = "Present"
        att_summary.loc[att_summary["total_punches"] == 1, "status"] = "Missing Punch"
        att_summary.to_sql("stg_attendance_daily", conn, if_exists="replace", index=False)
        
    conn.close()
    print("Stage 2 & 3 transformation completed.")

def run_analytics():
    conn = sqlite3.connect(DB_PATH)
    queries = {
        "q01_headcount.sql": "analytics/results/q01_headcount.csv",
        "q02_attrition.sql": "analytics/results/q02_attrition.csv",
        "q03_absenteeism.sql": "analytics/results/q03_absenteeism.csv",
        "q04_late_arrivals.sql": "analytics/results/q04_late_arrivals.csv",
        "q05_overtime_comparison.sql": "analytics/results/q05_overtime_comparison.csv",
        "q06_overtime_excess.sql": "analytics/results/q06_overtime_excess.csv",
        "q07_paid_zero_attendance.sql": "analytics/results/q07_paid_zero_attendance.csv",
        "q08_pay_after_separation.sql": "analytics/results/q08_pay_after_separation.csv",
        "q09_payroll_cost_mom.sql": "analytics/results/q09_payroll_cost_mom.csv",
        "q10_leave_overuse.sql": "analytics/results/q10_leave_overuse.csv"
    }
    
    os.makedirs("analytics/results", exist_ok=True)
    for q_file, out_csv in queries.items():
        q_path = os.path.join("analytics", q_file)
        if os.path.exists(q_path):
            with open(q_path, "r") as f:
                query_sql = f.read()
            try:
                df_res = pd.read_sql(query_sql, conn)
                df_res.to_csv(out_csv, index=False)
            except Exception as e:
                pd.DataFrame({"error": [str(e)]}).to_csv(out_csv, index=False)
        else:
            pd.DataFrame({"note": ["Placeholder result"]}).to_csv(out_csv, index=False)
    conn.close()

if __name__ == "__main__":
    clean_and_transform()
