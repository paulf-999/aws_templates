default: create_sm_entry

AWS_PROFILE=${MY_AWS_PROFILE}
CONFIG_FILE=env/config.json

$(eval SECRETNAME=$(shell jq '.Parameters.SecretName' ${CONFIG_FILE}))
$(eval SOURCE_SYSTEM=$(shell jq '.Parameters.SrcSystem' ${CONFIG_FILE}))
$(eval ENGINE=$(shell jq '.Parameters.Engine' ${CONFIG_FILE}))
$(eval DBNAME=$(shell jq '.Parameters.DbName' ${CONFIG_FILE}))
$(eval HOST=$(shell jq '.Parameters.Host' ${CONFIG_FILE}))
$(eval PORT=$(shell jq '.Parameters.Port' ${CONFIG_FILE}))
$(eval USERNAME=$(shell jq '.Parameters.Username' ${CONFIG_FILE}))
$(eval PWD=$(shell jq '.Parameters.Pwd' ${CONFIG_FILE}))
$(eval VERSION=$(shell jq '.Parameters.Version' ${CONFIG_FILE}))

create_sm_entry:
	$(info [+] Create a secrets manager entry)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name secrets-manager-eg-db-secret-v${VERSION} \
	--template-file secrets-manager-rdbms.yml \
	--parameter-overrides SecretName=${SECRETNAME} \
	SrcSystem=${SOURCE_SYSTEM} \
	engine=${ENGINE} \
	dbname=${DBNAME} \
	host=${HOST} \
	port=${PORT} \
	username=${USERNAME} \
	password=${PWD}
