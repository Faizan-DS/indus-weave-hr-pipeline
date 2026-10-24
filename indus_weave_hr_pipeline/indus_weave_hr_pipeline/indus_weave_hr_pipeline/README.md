# Indus Weave Textiles - HR Data Pipeline Project

## Overview
A robust, idempotent Python and SQLite data pipeline built for Indus Weave Textiles to ingest 6 months of messy HR exports across 5 modules, clean and reconcile biometric punches and employment history into a trusted star schema, answer 10 business operations questions, and uncover why overtime costs are rising.

## Tech Stack
- **Python 3.13** (pandas, numpy, sqlite3)
- **SQLite** (simulated schemas using table prefixes)

## Project Structure
```text
indus-weave-hr-pipeline/
├── README.md
├── requirements.txt
├── run_pipeline.py
├── ingestion/
│   └── ingest.py
├── transform/
│   └── clean_data.py
├── warehouse/
│   └── ddl/
│       └── create_warehouse.sql
├── analytics/
│   ├── q01_headcount.sql
│   ├── q02_attrition.sql
│   ├── q03_absenteeism.sql
│   ├── q04_late_arrivals.sql
│   ├── q05_overtime_comparison.sql
│   ├── q06_overtime_excess.sql
│   ├── q07_paid_zero_attendance.sql
│   ├── q08_pay_after_separation.sql
│   ├── q09_payroll_cost_mom.sql
│   ├── q10_leave_overuse.sql
│   └── results/
├── quality/
│   └── dq_checks.py
├── presentation/
│   └── cfo_findings.md
└── docs/
    ├── device_clock_finding.md
    └── INTERVIEW_GUIDE.md
```

## How to Run
1. Place raw CSV/JSON files in a `DATA/` folder in the parent directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute pipeline:
   ```bash
   python run_pipeline.py
   ```
