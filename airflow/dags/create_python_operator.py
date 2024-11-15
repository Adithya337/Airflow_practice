from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'retries': 5,
    'owner': "Adithya",
    'retry_delay': timedelta(minutes=5)
}


def greet(age, ti):
    # name = ti.xcom_pull(task_ids='Get_name')
    f_name = ti.xcom_pull(task_ids='Get_name', key='first_name')
    l_name = ti.xcom_pull(task_ids='Get_name', key='last_name')
    print(f'My name is {f_name} {l_name} and my age is {age}.')


def get_name(ti): #Task instance parameter
    # return 'Jerry'
    ti.xcom_push(key='first_name', value='Adithya')
    ti.xcom_push(key='last_name', value='Vardhan')


with DAG(
    default_args=default_args,
    dag_id='Python_operator_v5',
    description='Our first dag with python operator',
    start_date=datetime(2024, 11, 4),
    schedule='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'age': 22}
    )
    task2 = PythonOperator(
        task_id='Get_name',
        python_callable=get_name
    )
    task2 >> task1
