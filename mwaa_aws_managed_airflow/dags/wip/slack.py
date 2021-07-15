#source: https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/example_dags/example_s3_bucket.py

import os

from airflow.models.dag import DAG
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.utils.dates import days_ago

with DAG(
        dag_id='slack_test_dag',
        schedule_interval=None,
        start_date=days_ago(2),
        max_active_runs=1,
        tags=['example'],
    ) as dag:

    slack_test = SlackWebhookOperator(
        task_id='slack_test',
        http_conn_id='slack_connection',
        webhook_token=f'{slack_token}',
        message='Hello, World!',
        channel='#airflow-integration'
    )
    