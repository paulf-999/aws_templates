default: create_cfn_stack

AWS_PROFILE=${MY_AWS_PROFILE}
S3_BUCKET=mwaa-airflow-example

create_cfn_stack:
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-eg \
	--template-body file://cfn/mwaa-airflow-example.yml \
	--capabilities CAPABILITY_IAM
	sleep 60
	#wait for 60 secs (for S3 bucket to be created), then upload the file below
	aws --profile ${AWS_PROFILE} s3 cp dags/tutorial.py s3://${S3_BUCKET}/dags/
