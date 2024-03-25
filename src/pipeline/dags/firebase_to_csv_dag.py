from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from etl.extract.firebase_to_csv import export_user_to_csv, export_meetings_to_csv
from etl.extract.firebase_events_to_csv import export_events_to_csv
import pendulum

kst = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'firebase_to_csv_dag',
    default_args=default_args,
    description='DAG for exporting Firebase data to CSV',
    start_date=datetime(2022, 1, 1, tzinfo=kst),
    schedule='@daily',
) as dag:

    userExport_task = PythonOperator(
        task_id='export_user_to_csv',
        python_callable=export_user_to_csv,
        op_kwargs={
            'output_csv_path': '/Users/hyounjun/Desktop/Calback-Data-ML/data/raw/user_collection/output.csv'},
        dag=dag,
    )

    meetingsExport_task = PythonOperator(
        task_id='export_meetigns_to_csv',
        python_callable=export_meetings_to_csv,
        op_kwargs={
            'output_csv_path': '/Users/hyounjun/Desktop/Calback-Data-ML/data/raw/meetings_collection/output.csv'},
        dag=dag,
    )

    export_events_task = PythonOperator(
        task_id='export_events_to_csv',
        python_callable=export_events_to_csv,
        op_kwargs={
            'output_csv_path': '/Users/hyounjun/Desktop/Calback-Data-ML/data/raw/events/output.csv',
            'date': '{{ ds }}'
        },
        dag=dag,
    )

userExport_task >> meetingsExport_task >> export_events_task
