from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
default_args = {
    'owner': "Adithya",
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_postgess_v3',
    default_args=default_args,
    start_date=datetime(2024, 11, 3),
    schedule_interval='0 0 * * *'
) as dag:
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
    task1 >> task2 >> task3
