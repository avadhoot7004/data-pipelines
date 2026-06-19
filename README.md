
# Data Engineering Practice & Demos

This repository contains example ETL pipelines and supporting scripts used for learning, practice, and demonstrations.

## Repository structure

- `extract_load/` — Simple extract + load examples and helpers.
	- `etl.py` — Main extract/load pipeline (Python).
	- `drivercheck.py` — Utility script for environment/driver checks.
	- `etl_user_postgres_script.sql` — Example Postgres ETL SQL script.
	- `sql_server_etl_user.sql` — Example SQL Server ETL script.
	- `requirements.txt` — Python dependencies for this folder.

- `extract_transform_load/` — Example ETL pipeline demonstrating transformations.
	- `etl_pipeline.py` — Pipeline demonstrating extract → transform → load.
	- `setup.sql` — Example setup SQL for demo tables.
	- `requirements.txt` — Python dependencies for this folder.

## Getting started

Requirements: Python 3.8+ and the DB client libraries needed for the targets you plan to use.

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies for a folder you want to run. (Example for `extract_load`):

```powershell
pip install -r extract_load/requirements.txt
```

3. Configure database connection settings or environment variables as required by the scripts, then run the desired pipeline. Example:

```powershell
python extract_transform_load/etl_pipeline.py
```



