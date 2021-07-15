import os

from airflow import DAG, settings, secrets
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False
}

def test(**kwargs):
    ### set up DMS
    hook = AwsHook()
    client = hook.get_client_type('dms')
    dms_client.start_replication_task(
        ReplicationTaskArn={HERE},
        StartReplicationTaskType={HERE}
    )['ReplicationTask']
    return client
