from airflow import DAG
from airflow.decorators import dag, task
from datetime import datetime, timedelta

default_args = {
    'owner': "Adithya",
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


@dag(dag_id='dag_with_taskflow_api',
     default_args=default_args,
     start_date=datetime(2024, 11, 2),
     schedule_interval='@daily')
def hello_world_etl():

    @task()
    def get_name():
        return 'Jerry'

    @task()
    def get_age():
        return 22

    @task()
    def greet(name, age):
        print(f'My name is {name} and I am {age} years old.')
    name = get_name()
    age = get_age()
    greet(name, age)


greet_dag = hello_world_etl(
    
)
