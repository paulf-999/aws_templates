import os

from airflow import DAG
from datetime import datetime, timedelta
from operators.mssql_to_s3_operator import MsSQLToS3Operator

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': datetime(2018, 1, 1),
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}


with DAG(
        dag_id=os.path.basename(__file__).replace(".py", ""),
        tags=['python'],
        schedule_interval='@once',
        default_args=default_args
) as dag:
	pf_test = MsSQLToS3Operator(
        task_id="pf_test",
    	dag=dag
	)