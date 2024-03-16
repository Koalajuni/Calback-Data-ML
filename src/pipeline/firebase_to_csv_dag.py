from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.etl.extract.firebase_to_csv import firebase_to_csv
import pendulum


kst = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1, tzinfo=kst),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'firebase_to_csv_dag',
    default_args=default_args,
    description='DAG for exporting Firebase data to CSV',
    schedule_interval='@daily',
)

export_task = PythonOperator(
    task_id='export_to_csv',
    python_callable=firebase_to_csv.export_to_csv,
    dag=dag,
)

export_task
