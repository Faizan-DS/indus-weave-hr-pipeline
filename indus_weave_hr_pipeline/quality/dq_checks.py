import sqlite3
import pandas as pd

DB_PATH = "hr_pipeline.db"

def run_quality_checks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS dq_results;")
    cursor.execute("""
        CREATE TABLE dq_results (
            check_name TEXT,
            table_name TEXT,
            status TEXT,
            details TEXT
        )
    """)
    
    checks = [
        ("Check employee table not empty", "stg_employees", "SELECT COUNT(*) > 0 FROM stg_employees"),
        ("Check attendance daily table exists", "stg_attendance_daily", "SELECT COUNT(*) >= 0 FROM stg_attendance_daily")
    ]
    
    for check_name, table_name, query in checks:
        try:
            cursor.execute(query)
            passed = cursor.fetchone()[0]
            status = "PASS" if passed else "FAIL"
            details = "Condition met successfully."
        except Exception as e:
            status = "FAIL"
            details = str(e)
            
        cursor.execute("INSERT INTO dq_results VALUES (?, ?, ?, ?)", (check_name, table_name, status, details))
        print(f"DQ Check [{status}] - {check_name} ({table_name})")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_quality_checks()
