# Interview Guide & Quick Reference

## 30-Second Elevator Pitch
"We built a robust, idempotent ETL pipeline in Python and SQLite for Indus Weave Textiles to ingest 6 months of messy HR exports across 5 modules, clean and reconcile biometric punches and employment history into a trusted star schema, and uncover why overtime costs were rising—proving our findings with automated data quality checks."

## Key Definitions
- **ETL:** Extract, Transform, Load.
- **Idempotent:** Running the pipeline multiple times produces the exact same result without duplicating rows.
- **SCD Type 2:** Slowly Changing Dimension Type 2, tracking historical changes by maintaining valid_from and valid_to date ranges.
- **Star Schema:** Dimensional data model consisting of central fact tables surrounded by dimension tables.
- **LAG Window Function:** SQL function used to compare current row values with previous rows (used for 2-minute duplicate punch rule).
