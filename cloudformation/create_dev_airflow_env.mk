default: create_mssql_instance run_sql_cmds create_dms_job_and_components

AWS_PROFILE=${MY_AWS_PROFILE}
CONFIG_FILE=env/config.json

$(eval VPCID=$(shell jq '.Parameters.VPCId' ${CONFIG_FILE}))
$(eval DMSREPID=$(shell jq '.Parameters.DMSRepId' ${CONFIG_FILE}))
$(eval TARGET_S3_BUCKET=$(shell jq '.Parameters.TargetS3Bucket' ${CONFIG_FILE}))
$(eval VERSION=$(shell jq '.Parameters.Version' ${CONFIG_FILE}))
$(eval SECRETNAME=$(shell jq '.Parameters.SecretName' ${CONFIG_FILE}))
$(eval SOURCE_SYSTEM=$(shell jq '.Parameters.SrcSystem' ${CONFIG_FILE}))
$(eval ENGINE=$(shell jq '.Parameters.Engine' ${CONFIG_FILE}))
$(eval DBNAME=$(shell jq '.Parameters.DbName' ${CONFIG_FILE}))
$(eval HOST=$(shell jq '.Parameters.Host' ${CONFIG_FILE}))
$(eval PORT=$(shell jq '.Parameters.Port' ${CONFIG_FILE}))
$(eval USERNAME=$(shell jq '.Parameters.Username' ${CONFIG_FILE}))
$(eval PWD=$(shell jq '.Parameters.Pwd' ${CONFIG_FILE}))

#template for MSSQL commands
MSSQL_CMD=sqlcmd -S ${HOST} -U ${USER} -P "${PWD}" -y 30 -Y 30
DMS_IP_TBLS={ "rule-type": "selection", "rule-id": "1", "rule-name": "1", "object-locator": { "schema-name": "production", "table-name": "brands" }, "rule-action": "include" }

create_mssql_instance:
	$(info [+] Create an Airflow dev env)
	# 1. Create an MSSQL RDS instance
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name rds-mssql-instance-v${VERSION} \
	--template-file dms/rds/rds-mssql.yml \
	--parameter-overrides MyVPC=${VPCID} \
	MyCidrIP=${IP} \
	DBUser=${USERNAME} \
	DBPassword=${PWD}

run_sql_cmds:
	# fetch Hostname of RDS instance, to use for MSSQL commands
	$(eval HOST=$(shell aws cloudformation list-exports --profile ${AWS_PROFILE} | jq '.Exports[] | select(.Name=="MSSQLDBEndpointAddress") | .Value'))
	# run SQL commands to create sample database and load data
	${MSSQL_CMD} -i rds/sql_example/mssql/1_create_db_objs.sql
	${MSSQL_CMD} -i rds/sql_example/mssql/2_load_data.sql

create_dms_job_and_components:
	$(info [+] Create a Secrets Manager entry)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name secrets-manager-eg-db-secret-v${VERSION} \
	--template-file secrets-manager/secrets-manager-rdbms.yml \
	--parameter-overrides SecretName=${SECRETNAME} \
	SrcSystem=${SOURCE_SYSTEM} \
	engine=${ENGINE} \
	dbname=${DBNAME} \
	host=${HOST} \
	port=${PORT} \
	username=${USERNAME} \
	password=${PWD}

	$(info [+] create a DMS replication instance)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name dms-rep-instance-v${VERSION} \
	--template-file dms/dms-replication-instance.yml \
	--capabilities CAPABILITY_NAMED_IAM \
	--parameter-overrides VPCID=${VPCID} \
	DMSVpcSubnetIds=subnet-28c7354e,subnet-c18a6589 \
	DMSRepinstanceId=${DMSREPID} \
	DmsRepinstancePublicAccesibility=True \
	DmsRepinstanceClass=dms.t3.micro

	$(info [+] Create a DMS RDBMS source EP)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name dms-src-ep-v${VERSION} \
	--template-file dms/dms-rdbms-source-endpoint.yml \
	--parameter-overrides SecretName=eg-mssql-db

	$(info [+] Create a DMS RDBMS target EP)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name dms-target-ep-v${VERSION} \
	--template-file dms/dms-s3-target-endpoint.yml \
	--capabilities CAPABILITY_IAM \
	--parameter-overrides BucketName=${TARGET_S3_BUCKET} \
	EndPointName=eg-target-s3-bucket \
	BucketFolderName=eg_data_src

	$(info [+] Create a DMS task)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name dms-task-v${VERSION} \
	--template-file dms/dms-replication-task.yml \
	--parameter-overrides DmsRepTaskName=example-task \
	DmsMigrationType=full-load \
	DmsTaskTableMappings='{"rules":[${DMS_IP_TBLS}]}'

# 5. Start Airflow bits, more just for reference
start_webserver:
	$(info [+] Start the web server, default port is 8080)
	airflow webserver --port 8080

start_scheduler:
	$(info [+] Start the scheduler)
	# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
	airflow scheduler

create_airflow_variables:
	$(info [+] Create some (example) Airflow variables)
	@airflow variables set AWS_ACCESS_KEY ${AWS_ACCESS_KEY}
	@airflow variables set AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}

delete_airflow_dev_env:
	aws cloudformation --profile ${AWS_PROFILE} delete-stack --stack-name dms-task-v1
	sleep 90	
	aws cloudformation --profile ${AWS_PROFILE} delete-stack --stack-name dms-rep-instance-v1
	aws cloudformation --profile ${AWS_PROFILE} delete-stack --stack-name dms-target-ep-v1
	aws cloudformation --profile ${AWS_PROFILE} delete-stack --stack-name dms-src-ep-v1
	sleep 90
	aws cloudformation --profile ${AWS_PROFILE} delete-stack --stack-name secrets-manager-eg-db-secret-v1
	aws cloudformation --profile ${AWS_PROFILE} delete-stack --stack-name rds-mssql-instance-v1
