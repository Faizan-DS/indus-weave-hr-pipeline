import glob
import hashlib
import os
import sqlite3
from datetime import datetime
import pandas as pd 
# Define DB path
DB_PATH = "hr_pipeline.db"

# Flexible path search for DATA folder regardless of working directory
POSSIBLE_DATA_PATHS = [
    "DATA",
    "../DATA",
    "../../DATA",
    r"H:\SMIT-CDE\Hackathon\DATA",
]


def get_data_dir():
    for p in POSSIBLE_DATA_PATHS:
        if os.path.exists(p) and os.path.isdir(p):
            return p
    return "DATA"  # default fallback


RAW_DIR = get_data_dir()


def compute_row_hash(row):
    """Generates an MD5 hash for each row to ensure idempotency."""
    row_string = "".join(str(val) for val in row.values)
    return hashlib.md5(row_string.encode("utf-8")).hexdigest()


def profile_and_load():
    # Fix: Only call makedirs if a directory path exists
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    # Search for all raw CSV and JSON files
    files = glob.glob(os.path.join(RAW_DIR, "*.csv")) + glob.glob(
        os.path.join(RAW_DIR, "*.json")
    )

    if not files:
        print(f"[WARNING] No CSV/JSON files found in directory: {RAW_DIR}")
        print("Please ensure your raw data files are inside the 'DATA' folder.")

    print(
        f"Found {len(files)} raw files to ingest from '{os.path.abspath(RAW_DIR)}'."
    )

    for file_path in files:
        filename = os.path.basename(file_path)
        table_name = "raw_" + os.path.splitext(filename)[0]

        print(f"\n--- Ingesting: {filename} ---")
        if filename.endswith(".csv"):
            df = pd.read_csv(file_path, dtype=str)
        else:
            df = pd.read_json(file_path, dtype=str)

        print(f"Rows: {len(df)}, Columns: {len(df.columns)}")

        # Add load metadata
        df["_source_file"] = filename
        df["_loaded_at"] = datetime.now().isoformat()
        df["_row_hash"] = df.apply(compute_row_hash, axis=1)

        # Idempotent write
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {len(df)} rows into table '{table_name}'.")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    profile_and_load()