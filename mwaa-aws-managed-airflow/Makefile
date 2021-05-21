default: create_cfn_stack

AWS_PROFILE=${MY_AWS_PROFILE}
CONFIG_FILE=env/config.json

$(eval AWS_ACCOUNT_ID=$(shell jq '.Parameters.AwsAccountId' ${CONFIG_FILE}))
$(eval S3_BUCKET=$(shell jq '.Parameters.S3Bucket' ${CONFIG_FILE}))
$(eval IAM_ROLE=$(shell jq '.Parameters.IamRoleName' ${CONFIG_FILE}))
$(eval CONN_TYPE=$(shell jq '.Parameters.ConnType' ${CONFIG_FILE}))
$(eval DATA_SRC=$(shell jq '.Parameters.SrcSystem' ${CONFIG_FILE}))
$(eval AIRFLOW_UI_URL=$(shell jq '.Parameters.AirflowUIURL' ${CONFIG_FILE}))
$(eval LOGIN=$(shell jq '.Parameters.Login' ${CONFIG_FILE}))
$(eval PASS=$(shell jq '.Parameters.Password' ${CONFIG_FILE}))
$(eval ROLE_ARN=$(shell jq '.Parameters.RoleARN' ${CONFIG_FILE}))
$(eval REGION=$(shell jq '.Parameters.Region' ${CONFIG_FILE}))

create_cfn_stack:
	$(info [+] Create an instance of MWAA)
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-eg \
	--template-body file://cfn/mwaa-airflow-example.yml \
	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
	--parameters ParameterKey=S3BucketName,ParameterValue=${S3_BUCKET} \
	ParameterKey=MwaaExecRoleName,ParameterValue=${IAM_ROLE}
	sleep 45
	#wait for 45 secs (for S3 bucket to be created), then upload the file below
	aws --profile ${AWS_PROFILE} s3 cp dags/s3.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp dags/slack.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp dags/secrets-manager.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp requirements.txt s3://${S3_BUCKET}/requirements.txt

gen_airflow_aws_airflow_conn_string:
	$(info [+] Generate MWAA connection string)
	@python3 py/gen_mwaa_conn_string.py ${CONN_TYPE} ${AIRFLOW_UI_URL} ${LOGIN} ${PASS} ${ROLE_ARN} ${REGION} ${AWS_PROFILE}

add_sm_entry:
	$(info [+] Create secret for DB creds)
	@aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name edp-secrets-manager-chequeguard-db \
	--template-file cfn/secrets-manager.yml \
	--parameter-overrides SecretName="airflow/connections/mwaa-connection" \
