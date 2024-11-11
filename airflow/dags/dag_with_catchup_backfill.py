from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Adithya',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id='dag_with_catchup_backfill_v1',
    default_args=default_args,
    start_date=datetime(2024, 10, 28),
    schedule='@daily',
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo Hello my name is Adithya'
    )

'''
docker exec -it d1868bef5e0d bash
airflow dags backfill -s 2024-10-28 -e 2024-11-04 dag_with_catchup_backfill_v1
exit
'''
