#default: create_mwaa_s3_bucket create_cfn_stack gen_airflow_aws_airflow_conn_string
default: create_cfn_stack

AWS_PROFILE=${MY_AWS_PROFILE}
CONFIG_FILE=env/config.json

$(eval AWS_ACCOUNT_ID=$(shell jq '.Parameters.AwsAccountId' ${CONFIG_FILE}))
$(eval MWAA_ENV_NAME=$(shell jq '.Parameters.MWAAEnvName' ${CONFIG_FILE}))
$(eval S3_BUCKET=$(shell jq '.Parameters.S3Bucket' ${CONFIG_FILE}))
$(eval IAM_ROLE=$(shell jq '.Parameters.IamRoleName' ${CONFIG_FILE}))
$(eval CONN_TYPE=$(shell jq '.Parameters.ConnType' ${CONFIG_FILE}))
$(eval DATA_SRC=$(shell jq '.Parameters.SrcSystem' ${CONFIG_FILE}))
$(eval LOGIN=$(shell jq '.Parameters.Login' ${CONFIG_FILE}))
$(eval PASS=$(shell jq '.Parameters.Password' ${CONFIG_FILE}))
$(eval ROLE_ARN=$(shell jq '.Parameters.RoleARN' ${CONFIG_FILE}))
$(eval REGION=$(shell jq '.Parameters.Region' ${CONFIG_FILE}))

create_cfn_stack:
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-v1-orig \
	--template-body file://cfn/mwaa-airflow-example.yml \
	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
	--parameters ParameterKey=EnvironmentName,ParameterValue=${MWAA_ENV_NAME} \
	ParameterKey=S3BucketName,ParameterValue=${S3_BUCKET}
	sleep 45
	#wait for 45 secs (for S3 bucket to be created), then upload the file below
	aws --profile ${AWS_PROFILE} s3 cp dags/s3.py s3://${S3_BUCKET}/dags/
	#aws --profile ${AWS_PROFILE} s3 cp dags/slack.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp dags/secrets-manager.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp requirements.txt s3://${S3_BUCKET}/requirements.txt
	#@aws --profile ${AWS_PROFILE} mwaa get-environment --name ${MWAA_ENV_NAME} > tmp/mwaa-env-details.json

gen_airflow_aws_airflow_conn_string:
	$(info [+] Generate MWAA connection string)
	@# Get MWAA Web Server URL & place in variable 'AIRFLOW_UI_URL'
	@aws --profile ${AWS_PROFILE} mwaa get-environment --name ${MWAA_ENV_NAME} > tmp/mwaa-env-details.json
	@$(eval AIRFLOW_UI_URL=$(shell jq '.Environment.WebserverUrl' tmp/mwaa-env-details.json))
	@$(eval MWAA_CONN_STRING=$(shell python3 py/gen_mwaa_conn_string.py ${CONN_TYPE} ${AIRFLOW_UI_URL} ${LOGIN} ${PASS} ${ROLE_ARN} ${REGION} ${AWS_PROFILE}))
	@# Create secret for MWAA Conn String)
	@aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-sm-eg \
	--template-file cfn/secrets-manager.yml \
	--parameter-overrides SecretName="airflow/connections/mwaa-connection" \
	SrcSystem=example \
	SecretString=${MWAA_CONN_STRING}

upload_dag_eg:
	@aws --profile ${AWS_PROFILE} s3 cp dags/secrets-manager.py s3://${S3_BUCKET}/dags/
