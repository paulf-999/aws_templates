import os

from airflow import DAG, settings, secrets
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.utils.dates import days_ago

from datetime import timedelta

### The steps to create this secret key can be found at: https://docs.aws.amazon.com/mwaa/latest/userguide/connections-secrets-manager.html
sm_secret_name = 'airflow/connections/mwaa-connection'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1)
}

### Gets the secret from Secrets Manager
def read_from_aws_sm_fn(**kwargs):
    ### set up Secrets Manager
    hook = AwsHook()
    client = hook.get_client_type('secretsmanager')
    response = client.get_secret_value(SecretId=sm_secret_name)
    secret_string = response["SecretString"]

    return secret_string

### 'os.path.basename(__file__).replace(".py", "")' uses the file name secrets-manager.py for a DAG ID of secrets-manager
with DAG(
        dag_id=os.path.basename(__file__).replace(".py", ""),
        tags=['python'],
        default_args=default_args,
        schedule_interval=None,
        dagrun_timeout=timedelta(hours=2)
) as dag:
    write_all_to_aws_sm = PythonOperator(
        task_id="read_from_aws_sm",
        python_callable=read_from_aws_sm_fn,
        provide_context=True
    )
