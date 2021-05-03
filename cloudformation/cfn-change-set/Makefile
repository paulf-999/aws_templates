default: example

CHANGE_NAME=eg-change-s3-name
CFN_STACK_NAME=example-stack-name

example:
	aws cloudformation create-stack \
	--profile ${MY_AWS_PROFILE} \
	--stack-name ${CFN_STACK_NAME} \
	--template-body file://../s3/s3-bucket.yml \
	--parameters ParameterKey=S3BucketName,ParameterValue=pf-test-260288

create_change_set:
	# create the cfn change set
	aws cloudformation create-change-set \
	--profile ${MY_AWS_PROFILE} \
	--stack-name ${CFN_STACK_NAME} \
	--change-set-name ${CHANGE_NAME} \
	--use-previous-template \
	--parameters ParameterKey=S3BucketName,ParameterValue=pf-test-99926021988
	sleep 10
	# then execute the cfn change set
	aws cloudformation execute-change-set \
	--profile ${MY_AWS_PROFILE} \
	--stack-name ${CFN_STACK_NAME} \
	--change-set-name ${CHANGE_NAME} \

cfn_stack_exists:
	aws cloudformation wait stack-exists \
	--profile ${MY_AWS_PROFILE} \
	--stack-name beepbeep \
