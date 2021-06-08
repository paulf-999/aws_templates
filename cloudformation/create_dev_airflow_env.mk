default: create_airflow_dev_env

AWS_PROFILE=${MY_AWS_PROFILE}
VERSION=1
VPC=${MY_VPC}
IP=${MY_IP_CIDR}
USER=${MY_USERNAME}
PWD=${MY_PWD}

#template for MSSQL commands
MSSQL_CMD=sqlcmd -S ${HOST} -U ${USER} -P "${PWD}" -y 30 -Y 30

create_airflow_dev_env:
	make -f rds/Makefile

create_mssql_instance:
	$(info [+] Create an Airflow dev env)
	# 1. Create an MSSQL RDS instance
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name rds-mssql-instance-v${VERSION} \
	--template-file rds/rds-mssql.yml \
	--parameter-overrides MyVPC=${VPC} \
	MyCidrIP=${IP} \
	DBUser=${USER} \
	DBPassword=${PWD}

run_sql_cmds:
	# fetch Hostname of RDS instance, to use for MSSQL commands
	$(eval HOST=$(shell aws cloudformation list-exports --profile ${AWS_PROFILE} | jq '.Exports[] | select(.Name=="MSSQLDBEndpointAddress") | .Value'))
	# run SQL commands to create sample database and load data
	${MSSQL_CMD} -i rds/sql_example/mssql/1_create_db_objs.sql
	${MSSQL_CMD} -i rds/sql_example/mssql/2_load_data.sql

# 4. Start Airflow bits
start_webserver:
	$(info [+] Start the web server, default port is 8080)
	airflow webserver --port 8080

start_scheduler:
	$(info [+] Start the scheduler)
	# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
	airflow scheduler
