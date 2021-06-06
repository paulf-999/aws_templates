default: create_dms_instance

AWS_PROFILE=${MY_AWS_PROFILE}
CONFIG_FILE=env/config.json

$(eval VPCID=$(shell jq '.Parameters.VPCId' ${CONFIG_FILE}))
$(eval DMSREPID=$(shell jq '.Parameters.DMSRepId' ${CONFIG_FILE}))
$(eval TARGET_S3_BUCKET=$(shell jq '.Parameters.TargetS3Bucket' ${CONFIG_FILE}))
$(eval VERSION=$(shell jq '.Parameters.Version' ${CONFIG_FILE}))

#template = { "rule-type": "selection", "rule-id": "1", "rule-name": "1", "object-locator": { "schema-name": "dbo", "table-name": "CustomerBin" }, "rule-action": "include" }
DMS_IP_TBLS={ "rule-type": "selection", "rule-id": "1", "rule-name": "1", "object-locator": { "schema-name": "production", "table-name": "brands" }, "rule-action": "include" }

create_dms_instance:
	$(info [+] Create a public VPC)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name dms-rep-instance-v${VERSION} \
	--template-file dms-replication-instance.yml \
	--capabilities CAPABILITY_NAMED_IAM \
	--parameter-overrides VPCID=${VPCID} \
	DMSVpcSubnetIds=subnet-28c7354e,subnet-c18a6589 \
	DMSRepinstanceId=${DMSREPID} \
	DmsRepinstancePublicAccesibility=True \
	DmsRepinstanceClass=dms.t3.micro

create_dms_src_rdbms_ep:
	$(info [+] Create a DMS RDBMS source EP)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name dms-src-ep-v${VERSION} \
	--template-file dms-rdbms-source-endpoint.yml \
	--parameter-overrides SecretName=eg-mssql-db

create_dms_target_s3_ep:
	$(info [+] Create a DMS RDBMS target EP)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name dms-target-ep-v${VERSION} \
	--template-file dms-s3-target-endpoint.yml \
	--capabilities CAPABILITY_IAM \
	--parameter-overrides BucketName=${TARGET_S3_BUCKET} \
	EndPointName=eg-target-s3-bucket \
	BucketFolderName=eg_data_src

create_dms_task:
	$(info [+] Create a DMS task)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name dms-task-v${VERSION} \
	--template-file dms-replication-task.yml \
	--parameter-overrides DmsRepTaskName=example-task \
	DmsMigrationType=full-load \
	DmsTaskTableMappings='{"rules":[${DMS_IP_TBLS}]}'
