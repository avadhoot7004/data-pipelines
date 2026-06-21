from airflow import DAG 
from airflow.operators.python import PythonOperator 
from datetime import datetime, timedelta 
import sys 
 
# Tell Airflow where to find your ETL script 
sys.path.insert(0, '/opt/airflow') 
#from etl_incremental import run_incremental_etl 

from etl_incremental import (
    run_incremental_etl,
    log_row_count
)

default_args = { 
    'owner': 'data-engineering-student', 
    'retries': 1, 
    'retry_delay': timedelta(minutes=1) 
} 
 
with DAG( 
    dag_id='ecommerce_incremental_etl', 
    default_args=default_args, 
    description='Incremental ETL: orders_db + products_db -> analytics_db', 
    schedule='*/5 * * * *',   # every 5 minutes  
    start_date=datetime(2024, 1, 1), 
    catchup=False,                   # do not backfill old runs 
    tags=['training', 'etl', 'postgres'] 
) as dag: 
 
    run_etl = PythonOperator( 
        task_id='run_incremental_etl', 
        python_callable=run_incremental_etl 
    ) 

    log_count = PythonOperator(
    task_id='log_row_count',
    python_callable=log_row_count
    )
 
    run_etl >> log_count  # set task dependencies so log_count runs after run_etl

