default: create_s3_bucket create_public_vpc_mwaa create_public_mwaa gen_airflow_aws_airflow_conn_string

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
$(eval VERSION=$(shell jq '.Parameters.Version' ${CONFIG_FILE}))

create_s3_bucket:
	$(info [+] Create an initial S3 bucket, required to store dags / requirements.txt)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-s3-bucket-v${VERSION} \
	--template-file cfn/s3-bucket.yml \
	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
	--parameter-overrides S3BucketName=${S3_BUCKET}
	aws --profile ${AWS_PROFILE} s3 cp requirements.txt s3://${S3_BUCKET}/requirements.txt
	aws --profile ${AWS_PROFILE} s3 cp dags/secrets_manager_dag.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp dags/s3_bucket_dag.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp dags/get_airflow_cfg.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp dags/get_env_vars.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp dags/get_py_pkgs.py s3://${S3_BUCKET}/dags/
	#aws --profile ${AWS_PROFILE} s3 cp dags/slack.py s3://${S3_BUCKET}/dags/

create_public_vpc_mwaa:
	$(info [+] Create a public VPC)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-public-vpc-v${VERSION} \
	--template-file cfn/public-vpc.yml \
	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
	--parameter-overrides EnvironmentName=${MWAA_ENV_NAME}

create_public_mwaa:
	$(info [+] Create a public MWAA instace)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name pf-dev-v1-mwaa-airflow-public-mwaa-v${VERSION} \
	--template-file cfn/public-mwaa.yml \
	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
	--parameter-overrides EnvironmentName=${MWAA_ENV_NAME}

gen_airflow_aws_airflow_conn_string:
	$(info [+] Generate MWAA connection string)
	@# Get MWAA Web Server URL & place in variable 'AIRFLOW_UI_URL'
	aws --profile ${AWS_PROFILE} mwaa get-environment --name ${MWAA_ENV_NAME} > tmp/mwaa-env-details.json
	@$(eval AIRFLOW_UI_URL=$(shell jq '.Environment.WebserverUrl' tmp/mwaa-env-details.json))
	@$(eval MWAA_CONN_STRING=$(shell python3 py/gen_mwaa_conn_string.py ${CONN_TYPE} ${AIRFLOW_UI_URL} ${LOGIN} ${PASS} ${ROLE_ARN} ${REGION} ${AWS_PROFILE}))
	@# Create secret for MWAA Conn String)
	@aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-sm-v${VERSION} \
	--template-file cfn/secrets-manager.yml \
	--parameter-overrides SecretName="airflow/connections/mwaa-connection" \
	SrcSystem=${DATA_SRC} \
	SecretString=${MWAA_CONN_STRING}

upload_dag_eg:
	@aws --profile ${AWS_PROFILE} s3 cp dags/secrets-manager.py s3://${S3_BUCKET}/dags/
