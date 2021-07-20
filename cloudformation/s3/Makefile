AWS_PROFILE=${MY_AWS_PROFILE}
VERSION=1

create_s3_bucket:
	$(info [+] Create an S3 bucket)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name s3-bucket-v${VERSION} \
	--template-file s3-bucket.yml \
	--parameter-overrides S3BucketName=example-bucket-unique-name
