from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def test(**kwargs):
    print(kwargs)

with DAG(
    dag_id="test",
    start_date=datetime(2023, 10, 26),
    schedule_interval="@daily",
) as dag:
    test = PythonOperator(
        task_id="test",
        python_callable=test,
        op_kwargs={"hello": "world"},
    )

if __name__ == '__main__':
    dag.test()

