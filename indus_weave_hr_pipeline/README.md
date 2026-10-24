<<<<<<< HEAD
# Indus Weave Textiles - HR Data Pipeline Project

## Overview
A robust, idempotent Python and SQLite data pipeline built for Indus Weave Textiles to ingest 6 months of messy HR exports across 5 modules, clean and reconcile biometric punches and employment history into a trusted star schema, answer 10 business operations questions, and uncover why overtime costs are rising.

## Tech Stack
- **Python 3.13** (pandas, numpy, sqlite3)
- **SQLite** (simulated schemas using table prefixes)

## Project Structure
=======
# Indus Weave HR Data Pipeline

**Restoring trust in HR and payroll analytics: a Python + SQL pipeline that reconciles biometric attendance, overtime requests and payroll for a 1,200-employee textile manufacturer.**

Built for the PeopleOps Data Hackathon (HR Pipeline Case Study). All data is synthetic.

---

## Table of contents

1. [The problem](#1-the-problem)
2. [Headline results](#2-headline-results)
3. [Architecture](#3-architecture)
4. [Repository structure](#4-repository-structure)
5. [Tech stack](#5-tech-stack)
6. [Setup and how to run](#6-setup-and-how-to-run)
7. [Pipeline stages in detail](#7-pipeline-stages-in-detail)
8. [Data issues found and how they are fixed](#8-data-issues-found-and-how-they-are-fixed)
9. [Business rules implemented](#9-business-rules-implemented)
10. [Data model](#10-data-model)
11. [Data quality checks](#11-data-quality-checks)
12. [Overtime reconciliation: method](#12-overtime-reconciliation-method)
13. [Project status](#13-project-status)
14. [Roadmap](#14-roadmap)
15. [Team](#15-team)

---

## 1. The problem

Indus Weave Textiles has about 1,200 employees across a head office and three plants (Korangi, SITE and Faisalabad). It moved HR onto a cloud HCM platform where attendance, shifts, leave, overtime, payroll and recruitment each live in a separate module and export their own files.

The overtime bill has risen for six months. HR says attendance looks normal. Payroll pays overtime from **approved overtime requests**, not from **actual biometric punches**. Every module tells a slightly different story, so nobody trusts anyone's numbers.

This project turns six months of messy exports (1 April to 30 September 2026) into one trusted model, then uses it to explain where the overtime money goes.

## 2. Headline results

All figures are reproduced by `analytics/overtime_reconciliation.py` from the raw files.

| Metric | Result |
|---|---|
| Raw biometric punches | 345,280 |
| Unmapped punches rejected (contractors, visitors) | 6,962 |
| Duplicate punches removed (2-minute rule) | 16,175 |
| Clean punches used | 322,143 |
| Overtime computed from punches | **35,911.0 h** |
| Overtime approved in requests | **36,401.5 h** |
| Overtime paid in payroll | **36,401.5 h** |
| Net gap (approved minus punches) | +490.5 h |
| Approved above what punches show, day by day | **4,683.0 h** |
| Worked but never approved | 4,192.5 h |
| Cost of the 4,683 h at 2x base hourly rate | **PKR 2,296,614** |
| Total overtime paid in payroll | PKR 19,003,890 |

Monthly breakdown:

| Month | Punch OT (h) | Approved OT (h) | Paid OT (h) | Approved above punches (h) | Cost (PKR) |
|---|---|---|---|---|---|
| Apr 2026 | 5,974.5 | 5,525.5 | 5,525.5 | 269.5 | 121,569 |
| May 2026 | 6,046.0 | 5,806.5 | 5,806.5 | 477.0 | 217,226 |
| Jun 2026 | 5,812.0 | 5,889.0 | 5,889.0 | 730.0 | 340,161 |
| Jul 2026 | 6,067.5 | 6,249.0 | 6,249.0 | 892.5 | 441,767 |
| Aug 2026 | 6,180.5 | 6,513.0 | 6,513.0 | 1,024.5 | 509,003 |
| Sep 2026 | 5,830.5 | 6,418.5 | 6,418.5 | 1,289.5 | 666,887 |
| **Total** | **35,911.0** | **36,401.5** | **36,401.5** | **4,683.0** | **2,296,614** |

**What this means**

- Payroll pays exactly what is approved. Approved hours and paid hours are identical, which confirms payroll never checks punches.
- The net gap of 490.5 h looks small because unapproved overtime on some days offsets unsupported approvals on others. Day by day, **hours approved above what punches show grow every month**, from 270 h in April to 1,290 h in September. That is the cost driver.
- Recommended control: pay overtime only when the approved request, the punch-computed overtime and the payroll line all match (a three-way match).

## 3. Architecture

```
HCM exports (12 files, CSV + nested JSON, 5 modules)
        |
        v
 raw schema        Stage 1  Python load, all columns as text, + load metadata
        |
        v
 staging schema    Stages 2-3  cleaned, typed tables; attendance_daily
        |
        v
 warehouse schema  Stage 4  star schema, SCD Type 2 employee dimension
        |
        v
 business answers  Stage 5  10 SQL questions -> CSV results

 Stage 6: data quality checks run after every load and log to dq_results
```

SQLite has no real schemas, so layers are separated with table prefixes: `raw_`, `stg_` and `dw_`.

## 4. Repository structure

>>>>>>> a02e102d47083ab73d993f133b023f0c6c68eeb7
```text
indus-weave-hr-pipeline/
├── README.md
├── requirements.txt
<<<<<<< HEAD
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
=======
├── run_pipeline.py                 # one-command rebuild
├── ingestion/
│   └── ingest.py                   # Stage 1: raw load
├── transform/
│   └── clean_data.py               # Stages 2-3: clean + business logic
├── warehouse/
│   └── ddl/create_warehouse.sql    # Stage 4: star schema DDL
├── analytics/
│   ├── q01_headcount.sql ... q10_leave_overuse.sql
│   ├── overtime_reconciliation.py  # punches vs approved vs paid (slide 9 numbers)
│   └── results/                    # CSV output
├── quality/
│   └── dq_checks.py                # Stage 6: checks -> dq_results
├── presentation/
│   ├── cfo_findings.md
│   └── indus_weave_pipeline_10slides.pptx
>>>>>>> a02e102d47083ab73d993f133b023f0c6c68eeb7
└── docs/
    ├── device_clock_finding.md
    └── INTERVIEW_GUIDE.md
```

<<<<<<< HEAD
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
=======
## 5. Tech stack

- Python 3 (pandas, numpy, sqlite3)
- SQLite (the brief allows it when PostgreSQL is not available)
- SQL with CTEs and window functions for analytics

## 6. Setup and how to run

### Prerequisites

- Python 3.10 or newer
- The 12 raw files and `data_dictionary.md`, supplied by the hackathon mentors (not stored in this repo)

### Install

```bash
git clone <your-repo-url>
cd indus-weave-hr-pipeline
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Add the data

Place the raw files in a `DATA/` folder **one level above** the repo (the path the ingestion script reads), or pass your own location to the reconciliation script:

```text
parent-folder/
├── DATA/
│   ├── employees.csv
│   ├── employment_history.csv
│   ├── departments.csv
│   ├── shifts.json
│   ├── shift_roster.csv
│   ├── device_mapping.csv
│   ├── biometric_punches.csv
│   ├── holidays.csv
│   ├── leave_requests.json
│   ├── overtime_requests.csv
│   ├── payroll_lines.csv
│   └── applications.csv
└── indus-weave-hr-pipeline/
```

Raw files are never edited by hand. Every fix lives in code.

### Run the pipeline

```bash
python run_pipeline.py
```

This runs ingestion, cleaning, warehouse DDL, the analytics queries and the data quality checks in order, and builds `hr_pipeline.db`.

### Reproduce the overtime numbers

```bash
python analytics/overtime_reconciliation.py --data-dir ../DATA
```

This prints the cleaning log and the monthly punches vs approved vs paid table, and writes `analytics/results/overtime_reconciliation_monthly.csv`.

## 7. Pipeline stages in detail

### Stage 1: Ingest (`ingestion/ingest.py`)

- Reads every CSV and JSON file with all columns as text (`dtype=str`), so nothing is guessed or altered on load.
- Adds `_source_file`, `_loaded_at` and `_row_hash` to each table.
- Writes to `raw_<filename>` tables. Reruns replace the tables, so running twice never creates duplicate rows.

### Stages 2 and 3: Clean and apply business logic (`transform/clean_data.py`)

- **Employees:** keep the row with the latest `updated_at` per `emp_id`; trim text and fix casing.
- **Punches:** map device user to employee by `device_id` + `device_user_id`; park unmapped punches in `stg_rejected_punches` with a reason; remove duplicates within 2 minutes using a `LAG`-style comparison with the previous punch.
- **Attendance:** `stg_attendance_daily` pairs the first and last punch per employee and day and assigns a status.

The complete shift-aware logic (night shifts, roster gap filling, holidays, leave, overtime rules) is in `analytics/overtime_reconciliation.py`.

### Stage 4: Warehouse (`warehouse/ddl/create_warehouse.sql`)

Star schema with primary and foreign keys enforced (`PRAGMA foreign_keys = ON`). See [Data model](#10-data-model).

### Stage 5: Analytics (`analytics/`)

One `.sql` file per business question, with results saved as CSV in `analytics/results/`:

| # | Question |
|---|---|
| 1 | Month-end headcount by plant and department |
| 2 | Monthly attrition rate by department |
| 3 | Absenteeism rate by plant and month, excluding approved leave |
| 4 | Top 10 employees by late arrivals, with department |
| 5 | Overtime from punches vs approved vs paid, by department and month |
| 6 | Departments where paid overtime exceeds computed overtime by more than 15% |
| 7 | Employees paid in a month with zero attendance |
| 8 | Employees still paid after their separation date |
| 9 | Payroll cost per employee by department, with month-over-month change |
| 10 | Employees whose approved Annual leave exceeds their full-year entitlement |

### Stage 6: Data quality (`quality/dq_checks.py`)

Checks run after the load and write PASS or FAIL rows to `dq_results`. See [Data quality checks](#11-data-quality-checks).

## 8. Data issues found and how they are fixed

| Issue | Evidence | Fix |
|---|---|---|
| 50 duplicate employee rows | 1,316 rows, 1,266 unique `emp_id` | Keep the latest `updated_at` |
| Three date formats | `YYYY-MM-DD`, `DD/MM/YYYY`, `DD-Mon-YYYY` | Parse each format in turn, store ISO dates |
| Messy department names | Mixed case, stray spaces, old names after renames | Trim and normalise; map through `departments.csv` |
| Unreliable `effective_to` in history | Overlaps and gaps for 37 employees | Ignore it; a record is valid until the day before the next one starts (SCD Type 2) |
| Unmapped punches | 6,962 punches with no device mapping | Reject to `stg_rejected_punches` with a reason |
| Duplicate punches | 16,175 punches within 2 minutes of the previous one | Drop them |
| **Device clock drift** | `DEV-SITE-01` runs 60 minutes fast from 1 July 2026 | Subtract 1 hour from its punches from that date |
| Night shifts crossing midnight | Check-out falls on the next calendar day | Attach each punch to the nearest shift window (previous, same or next day) |
| Missing roster weeks | Employees with gaps in `shift_roster.csv` | Carry the previous week's shift forward |
| Missing check-outs | Days with a single punch | Status `Missing Punch`, no overtime |

### How the device clock fault was found

For each device, take each employee's first morning punch and measure its minutes after the 06:00 day-shift start. The median is about 4 minutes for every device, except `DEV-SITE-01`, which shows about 4 minutes before July and about 64 minutes from 1 July onward, a jump of exactly one hour. 49,160 punches were corrected.

## 9. Business rules implemented

The rules come from `data_dictionary.md`. Where data disagrees with a rule, the rule wins.

- Duplicate employees: latest `updated_at` wins.
- Department history: valid until the day before the next record.
- Monthly figures belong to the department on the last day of the month.
- A missing roster week means the same shift as the previous week.
- Punches by the same employee within 2 minutes count as one.
- A night-shift punch belongs to the date the shift started.
- First punch is check-in, last punch is check-out; one punch is `Missing Punch`.
- Late arrival: more than 10 minutes after shift start. Early departure: more than 10 minutes before shift end. Counted on `Present` working days only.
- Overtime on a working day: minutes after shift end, rounded down to whole half-hours (29 min = 0 h, 45 min = 0.5 h, 75 min = 1.0 h).
- Work on a Sunday or plant holiday is all overtime: (check-out minus check-in), rounded down to half-hours.
- Leave counts only if both approval steps (Manager, then HR) say `Approved` and `cancelled_at` is empty.
- Only overtime requests with `status = Approved` count as approved overtime.
- Payroll `OVERTIME` line `units` equals hours paid; payroll cost is the sum of `EARNING` lines.

Attendance status priority: Weekly Off, Holiday, On Leave, Present, Missing Punch, Absent.

## 10. Data model

Star schema in the warehouse layer.

**Dimensions**

| Table | Purpose |
|---|---|
| `dw_dim_employee` | SCD Type 2 employee history: `valid_from`, `valid_to`, `is_current` |
| `dw_dim_department` | Department and plant hierarchy |
| `dw_dim_shift` | DAY, EVE, NIGHT, GEN shift times |
| `dw_dim_date` | Calendar |

**Facts**

| Table | Grain |
|---|---|
| `dw_fact_attendance_daily` | One row per employee per scheduled day |
| Leave day, approved overtime and payroll line facts | Planned (see [Project status](#13-project-status)) |

SCD Type 2 joins use `fact.work_date BETWEEN dim.valid_from AND dim.valid_to`.

## 11. Data quality checks

Checks write to `dq_results (check_name, table_name, status, details)`.

Designed check families:

- Uniqueness and not-null on every primary key
- Referential integrity: every fact row has a matching dimension row
- Reconciliation: raw rows = staging rows + rejected rows, for every table
- Accepted values for attendance status, leave type and pay component
- Business sanity: no negative worked hours, no shift longer than 16 hours, no overlapping SCD2 ranges

The reconciliation script confirms the sanity rules on the clean data: no negative worked hours and no shift longer than 16 hours.

## 12. Overtime reconciliation: method

`analytics/overtime_reconciliation.py` runs these steps:

1. Dedupe employees and parse the three date formats.
2. Map punches to employees, correct the `DEV-SITE-01` clock, reject unmapped punches and remove duplicates within 2 minutes.
3. Expand the weekly roster to daily shifts, filling missing weeks from the previous week.
4. Assign each punch to a shift date and build one row per employee and shift date (first and last punch).
5. Look up the employee's plant on that date from employment history, then flag Sundays and plant holidays.
6. Remove approved leave days and compute overtime in half-hour steps.
7. Compare, per employee and day, computed overtime against approved requests, and against payroll `OVERTIME` units by month.
8. Price the hours at the Factory Act rate, **2 x base hourly rate**, where the hourly rate is `basic salary / 208` using the employee's payroll basic for that month. This is exactly the formula payroll uses for its overtime amounts.

Currency is PKR. The data contains no exchange rate, so no USD figure is given.

## 13. Project status

| Component | Status |
|---|---|
| Raw ingestion with load metadata | Implemented |
| Employee dedupe, punch mapping, rejected punches, 2-minute rule | Implemented |
| Device clock correction, night shifts, roster gap filling, overtime rules | Implemented in `analytics/overtime_reconciliation.py` |
| Overtime reconciliation and cost (slide 9) | Implemented and reproducible |
| Warehouse DDL | Partial: 5 of 8 tables |
| Staging for leave, payroll, roster and SCD Type 2 | In progress |
| Analytics queries Q1 to Q10 | In progress: some queries are placeholders |
| Data quality checks | Partial: structure in place, full check set in progress |
| Bonus: one-command rebuild | Implemented (`run_pipeline.py`) |
| Bonus: incremental load, recruitment funnel, dashboard | Planned |

### Known limitations

- The ingestion script reads from `../DATA` and rebuilds tables on every run (full reload, not incremental).
- `_row_hash` currently includes the load timestamp, so it changes between runs.
- `leave_requests.json` is nested; full flattening into request, approval step and leave day tables is in progress.

## 14. Roadmap

- Complete staging, warehouse facts and all ten analytics queries on the warehouse tables
- Full automated data quality suite with reconciliation for every table
- Incremental loads for new months of punches
- Orchestration with Apache Airflow
- Migration to PostgreSQL, then a cloud warehouse (Snowflake or BigQuery)
- Dashboard on the warehouse tables

## 15. Team

| Name | Role |
|---|---|
| _Add team member_ | _Role_ |
| _Add team member_ | _Role_ |
| _Add team member_ | _Role_ |

---

*All data in this project is synthetic. No real employee is represented.*
>>>>>>> a02e102d47083ab73d993f133b023f0c6c68eeb7
