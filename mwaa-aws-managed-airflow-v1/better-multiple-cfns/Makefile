default: create_s3_bucket create_public_vpc_mwaa create_public_mwaa

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
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-wip-s3-bucket-v${VERSION} \
	--template-body file://cfn/s3-bucket.yml \
	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
	--parameters ParameterKey=S3BucketName,ParameterValue=${S3_BUCKET}
	sleep 45
	#wait for 45 secs (for S3 bucket to be created), then upload the file below
	aws --profile ${AWS_PROFILE} s3 cp dags/s3.py s3://${S3_BUCKET}/dags/
	#aws --profile ${AWS_PROFILE} s3 cp dags/slack.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp dags/secrets-manager.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp requirements.txt s3://${S3_BUCKET}/requirements.txt
	#@aws --profile ${AWS_PROFILE} mwaa get-environment --name ${MWAA_ENV_NAME} > tmp/mwaa-env-details.json

create_public_vpc_mwaa:
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-wip-public-vpc-v${VERSION} \
	--template-body file://cfn/public-vpc.yml \
	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
	--parameters ParameterKey=EnvironmentName,ParameterValue=${MWAA_ENV_NAME}

create_public_mwaa:
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-wip-public-mwaa-v${VERSION} \
	--template-body file://cfn/public-mwaa.yml \
	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
	--parameters ParameterKey=EnvironmentName,ParameterValue=${MWAA_ENV_NAME}

upload_dag_eg:
	@aws --profile ${AWS_PROFILE} s3 cp dags/secrets-manager.py s3://${S3_BUCKET}/dags/
