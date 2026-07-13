
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

- [elt_snowflake/](elt_snowflake/) — ELT pipeline using dbt (data build tool) on Snowflake sample data.
	- [data_pipeline_dbt/](elt_snowflake/data_pipeline_dbt/) — The dbt project directory containing models, configurations, and tests.
	- [data_pipeline_dbt/models/staging/](elt_snowflake/data_pipeline_dbt/models/staging/) — Staging models mapping raw Snowflake sources to cleaned views.
	- [data_pipeline_dbt/models/marts/](elt_snowflake/data_pipeline_dbt/models/marts/) — Marts models containing transformed fact tables and metrics.
	- [data_pipeline_dbt/macros/pricing.sql](elt_snowflake/data_pipeline_dbt/macros/pricing.sql) — Custom pricing macros.
	- [requirements.txt](elt_snowflake/requirements.txt) — Python dependencies for Snowflake and dbt.