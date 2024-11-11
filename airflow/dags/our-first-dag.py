from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'Adithya',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


with DAG(
    dag_id='our_first_dag_v3',
    description='This is our first dag',
    start_date=datetime(2024, 11, 3, 12),
    schedule_interval='@daily',
    default_args=default_args
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo this is the first task.'
    )
    task2 = BashOperator(
        task_id='second_task',
        bash_command='echo hello I am after task1'
    )
    task3 = BashOperator(
        task_id='third_task',
        bash_command='echo hello I am after task2'
    )

    # task1.set_downstream(task2)
    # task3.set_upstream(task1)

    task1 >> [task2, task3]

    task1 >> task2
    task1 >> task3
