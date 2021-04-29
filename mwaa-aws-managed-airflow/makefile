default: create_cfn_stack

AWS_PROFILE=${MY_AWS_PROFILE}
S3_BUCKET=mwaa-airflow-example

create_cfn_stack:
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-eg \
	--template-body file://cfn/mwaa-airflow-example.yml \
	--capabilities CAPABILITY_IAM

upload_dag_to_s3:
	aws --profile ${AWS_PROFILE} s3 cp tutorial.py s3://${S3_BUCKET}/dags/

create_iam_policy_for_airflow_developers:
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-eg-iam-policy \
	--template-body