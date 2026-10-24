"""
Master Orchestration Script for Indus Weave HR Pipeline.
Runs Stages 1 through 6 sequentially and rebuilds hr_pipeline.db.
"""

import os
import subprocess
import sys

def run_step(description, command):
    print(f"\n[PIPELINE] === {description} ===")
    result = subprocess.run([sys.executable, command], capture_output=False)
    if result.returncode != 0:
        print(f"[ERROR] Step failed: {description}")
        sys.exit(1)

def main():
    print("Starting Indus Weave HR Data Pipeline Build...")
    os.makedirs("analytics/results", exist_ok=True)
    
    # Stage 1: Ingestion
    run_step("Stage 1: Ingesting Raw Data", "ingestion/ingest.py")
    
    # Stage 2 & 3: Cleaning & Business Logic
    run_step("Stage 2 & 3: Cleaning Data & Applying Business Logic", "transform/clean_data.py")
    
    # Stage 4: Warehouse Star Schema DDL
    print("\n[PIPELINE] === Stage 4: Creating Warehouse Star Schema ===")
    import sqlite3
    conn = sqlite3.connect("hr_pipeline.db")
    with open("warehouse/ddl/create_warehouse.sql", "r") as f:
        conn.executescript(f.read())
    conn.close()
    print("Warehouse schema created successfully.")
    
    # Stage 5: Analytics Queries
    print("\n[PIPELINE] === Stage 5: Answering 10 Business Questions ===")
    subprocess.run([sys.executable, "-c", "import transform.clean_data as td; td.run_analytics()"])
    
    # Stage 6: Data Quality Checks
    run_step("Stage 6: Running Data Quality Checks", "quality/dq_checks.py")
    
    print("\n[PIPELINE] Pipeline Execution Completed Successfully!")

if __name__ == "__main__":
    main()
