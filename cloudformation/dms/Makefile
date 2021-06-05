default: create_dms_instance

AWS_PROFILE=${MY_AWS_PROFILE}
CONFIG_FILE=env/config.json

$(eval VPCID=$(shell jq '.Parameters.VPCId' ${CONFIG_FILE}))
$(eval DMSREPID=$(shell jq '.Parameters.DMSRepId' ${CONFIG_FILE}))
$(eval TARGET_S3_BUCKET=$(shell jq '.Parameters.TargetS3Bucket' ${CONFIG_FILE}))
$(eval VERSION=$(shell jq '.Parameters.Version' ${CONFIG_FILE}))

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
	$(info [+] Create a DMS RDBMS source EP)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name dms-target-ep-v${VERSION} \
	--template-file dms-s3-target-endpoint.yml \
	--capabilities CAPABILITY_IAM \
	--parameter-overrides BucketName=${TARGET_S3_BUCKET} \
	EndPointName=eg-target-s3-bucket
