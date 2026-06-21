
# Data Engineering Practice & Demos

This repository contains example ETL pipelines and supporting scripts used for learning, practice, and demonstrations.

## Repository structure

- [extract_load/](extract_load/) — Simple extract + load examples and helpers.
	- [etl.py](extract_load/etl.py) — Main extract/load pipeline (Python).
	- [drivercheck.py](extract_load/drivercheck.py) — Utility script for environment/driver checks.
	- [etl_user_postgres_script.sql](extract_load/etl_user_postgres_script.sql) — Example Postgres ETL SQL script.
	- [sql_server_etl_user.sql](extract_load/sql_server_etl_user.sql) — Example SQL Server ETL script.
	- [requirements.txt](extract_load/requirements.txt) — Python dependencies for this folder.

- [extract_transform_load/](extract_transform_load/) — Example ETL pipeline demonstrating transformations.
	- [etl_pipeline.py](extract_transform_load/etl_pipeline.py) — Pipeline demonstrating extract → transform → load.
	- [setup.sql](extract_transform_load/setup.sql) — Example setup SQL for demo tables.
	- [requirements.txt](extract_transform_load/requirements.txt) — Python dependencies for this folder.

- [etl_apache_airflow/](etl_apache_airflow/) — Containerized incremental ETL workflow orchestrated by Apache Airflow.
	- [docker-compose.yaml](etl_apache_airflow/docker-compose.yaml) — Spin up CeleryExecutor-based Airflow environment with Redis/PostgreSQL.
	- [setup.sql](etl_apache_airflow/setup.sql) — Database configuration and schema creation scripts.
	- [dags/etl_dag.py](etl_apache_airflow/dags/etl_dag.py) — The Airflow DAG scheduling and pipeline structure.
	- [dags/etl_incremental.py](etl_apache_airflow/dags/etl_incremental.py) — Python script managing incremental load logic (Watermarking & 7-day lookbacks).

## Getting started

Requirements: Python 3.8+ and Docker (required for running the Apache Airflow orchestration).

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



