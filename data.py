# from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow import DAG
from airflow.operators.python import PythonOperator


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
    run_spark_job = SparkSubmitOperator(
        task_id = "run_spark_job",
        application = "app.py",
        conn_id = "spark_conn",
        verbose = False,
        total_executor_cores=1,
        executor_memory='2g',
        driver_memory='2g',
        num_executors=1,
        executor_cores=1
    )
    task1 = PostgresOperator(
        task_id='create_postgress_table',
        postgres_conn_id='postgres_localhost',
        sql="""
create table if not exists dag_runs(dt date,dag_id character varying,primary key(dt,dag_id))
"""
    )
    task2 = PostgresOperator(
        task_id='delete_in_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
delete from dag_runs where  dt='{{ds}}' and dag_id = '{{dag.dag_id}}'
"""
    )
    task3 = PostgresOperator(
        task_id='insert_into_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
insert into dag_runs(dt,dag_id) values ('{{ds}}','{{dag.dag_id}}')
"""
    )

    # task1.set_downstream(task2)
    # task3.set_upstream(task1)

    task1 >> [task2, task3]

    task1 >> task2
    task1 >> task3
