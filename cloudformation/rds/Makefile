default: create_mssql_instance

AWS_PROFILE=${MY_AWS_PROFILE}
VERSION=1

create_mssql_instance:
	$(info [+] Create an initial S3 bucket, required to store dags / requirements.txt)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name rds-mssql-instance-v${VERSION} \
	--template-file rds-mssql.yml \

