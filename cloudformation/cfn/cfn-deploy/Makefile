default: example

CHANGE_NAME=eg-change-s3-name
CFN_STACK_NAME=example-stack-name

example:
	aws cloudformation deploy \
	--profile ${MY_AWS_PROFILE} \
	--stack-name ${CFN_STACK_NAME} \
	--template-file ../s3/s3-bucket.yml \
	--parameter-overrides S3BucketName=pf-test-260288111