from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator


default_args = {
    'owner': "Adithya",
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id='dag_with_corn_exp_v2',
    start_date=datetime(2024, 10, 1),
    schedule_interval='0 3 * * Tue'
    # schedule_interval='0 0 * * *'
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo Jai Hanuman',
    )
    task1
