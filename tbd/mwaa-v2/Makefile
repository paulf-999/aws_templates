#default: create_mwaa_s3_bucket create_cfn_stack gen_airflow_aws_airflow_conn_string

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

#1: Create the S3 bucket
create_mwaa_s3_bucket:
	$(info [+] Create an instance of MWAA)
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-s3-bucket-v${VERSION} \
	--template-body file://cfn/s3-bucket.yml \
	--parameters ParameterKey=S3BucketName,ParameterValue=${S3_BUCKET}
	sleep 45
	aws --profile ${AWS_PROFILE} s3 cp dags/s3.py s3://${S3_BUCKET}/dags/
	#aws --profile ${AWS_PROFILE} s3 cp dags/slack.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp dags/secrets-manager.py s3://${S3_BUCKET}/dags/
	aws --profile ${AWS_PROFILE} s3 cp requirements.txt s3://${S3_BUCKET}/requirements.txt
	#@aws --profile ${AWS_PROFILE} mwaa get-environment --name ${MWAA_ENV_NAME} > tmp/mwaa-env-details.json

#2: Create Public VPC network for MWAA instance
create_public_vpc_for_mwaa:
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-public-vpc-v${VERSION} \
	--template-body file://cfn/v1-public-vpc.yml \
	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
	--parameters ParameterKey=EnvironmentName,ParameterValue=${MWAA_ENV_NAME}

#WIP - Create VPC network for MWAA instance
#create_private_vpc_for_mwaa:
#	aws cloudformation deploy \
#	--profile ${AWS_PROFILE} \
#	--stack-name mwaa-airflow-private-vpc-v${VERSION} \
#	--template-file cfn/private-vpc.yml \
#	--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
#	--parameter-overrides EnvironmentName=${MWAA_ENV_NAME}
#TODO: cfn template the following: https://docs.aws.amazon.com/mwaa/latest/userguide/vpc-vpe-create-access.html

#3: Create public MWAA instance
create_mwaa_public_env:
	aws cloudformation create-stack \
	--profile ${AWS_PROFILE} \
	--stack-name mwaa-airflow-public-env-v${VERSION} \
	--template-body file://cfn/mwaa-public-environment.yml \
	--capabilities CAPABILITY_NAMED_IAM \
	--parameters ParameterKey=EnvironmentName,ParameterValue=${MWAA_ENV_NAME} \
	ParameterKey=MwaaExecRoleName,ParameterValue=${IAM_ROLE}

#WIP - create private MWAA instance
#create_mwaa_private_env:
#	aws cloudformation deploy \
#	--profile ${AWS_PROFILE} \
#	--stack-name mwaa-airflow-private-env-v${VERSION} \
#	--template-file cfn/mwaa-private-environment.yml \
#	--capabilities CAPABILITY_NAMED_IAM \
#	--parameter-overrides EnvironmentName=${MWAA_ENV_NAME} \
#	MwaaExecRoleName=${IAM_ROLE}
