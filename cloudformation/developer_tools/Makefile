default: create_codebuild_and_codepipeline_instances

AWS_PROFILE=${MY_AWS_PROFILE}
VERSION=1

create_codebuild_and_codepipeline_instances:
	$(info [+] Create an instance of a codebuild service)
	aws cloudformation deploy \
	--profile ${AWS_PROFILE} \
	--stack-name codebuild-and-codepipeline-v${VERSION} \
	--template-file cfn/codebuild-and-codepipeline.yml \
	--capabilities CAPABILITY_IAM \
	--parameter-overrides GitRepoOwner=paulf-999 \
	GitRepoName=dbt_cicd_demo \
	OAuthToken=${OATH_TOKEN} \
	CodeBuildProjectName=dbt_cicd_project_demo \
	PipelineName=dbt_cicd_pipeline_demo \
	SSMParamName=/snowflake/bikestores \
	SnowflakePass=${DEMO_DBT_PASS}
