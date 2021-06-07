default: create_airflow_dev_env

AWS_PROFILE=${MY_AWS_PROFILE}
VERSION=1
VPC=${MY_VPC}
IP=${MY_IP_CIDR}
USER=${MY_USERNAME}
PWD=${MY_PWD}

#MSSQL_CMD=sqlcmd -S ${HOST} -U ${USER} -P "${PWD}" -y 30 -Y 30

create_airflow_dev_env:
	make -f rds/Makefile

create_mssql_instance:
	$(info [+] Create an initial S3 bucket, required to store dags / requirements.txt)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name rds-mssql-instance-v${VERSION} \
	--template-file rds/rds-mssql.yml \
	--parameter-overrides MyVPC=${VPC} \
	MyCidrIP=${IP} \
	DBUser=${USER} \
	DBPassword=${PWD}
