PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS dw_dim_employee;
CREATE TABLE dw_dim_employee (
    employee_key INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    department TEXT,
    grade TEXT,
    valid_from TEXT,
    valid_to TEXT,
    is_current INTEGER
);

DROP TABLE IF EXISTS dw_dim_department;
CREATE TABLE dw_dim_department (
    department_key INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id TEXT NOT NULL,
    department_name TEXT,
    plant_location TEXT
);

DROP TABLE IF EXISTS dw_dim_shift;
CREATE TABLE dw_dim_shift (
    shift_key INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_code TEXT NOT NULL,
    shift_start TIME,
    shift_end TIME
);

DROP TABLE IF EXISTS dw_dim_date;
CREATE TABLE dw_dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date TEXT NOT NULL,
    day_of_week TEXT,
    month INTEGER,
    year INTEGER
);

DROP TABLE IF EXISTS dw_fact_attendance_daily;
CREATE TABLE dw_fact_attendance_daily (
    attendance_key INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_key INTEGER,
    date_key INTEGER,
    status TEXT,
    worked_hours REAL,
    overtime_hours REAL,
    late_minutes INTEGER,
    FOREIGN KEY (employee_key) REFERENCES dw_dim_employee(employee_key),
    FOREIGN KEY (date_key) REFERENCES dw_dim_date(date_key)
);
