# MWAA: i.e. AWS-managed-airflow (WIP)

Slightly streamlined version of the AWS quick start user guide for MWAA: https://docs.aws.amazon.com/mwaa/latest/userguide/quick-start.html

## Contents

* Overview
* Customisations
    * S3 bucket creation and prerequisite `requirements.txt`
    * Connectivity to AWS Secrets Manager
* How-to run
* Input parameters
* To-dos

## Overview 

This template creates:
* a VPC inftrastructure
* S3 Bucket (see note below)
* and an AWS MWAA (Managed Workflows for Apache Airflow) environment

## Customisations

### S3 bucket creation and prerequisite `requirements.txt`

* I've revised the quick start CFN template to instead create the S3 bucket in a separate prerequisite CFN stack
* This way, the required `requirements.txt` (that importantly captures, "apache-airflow-backport-providers-amazon") can be uploaded to the S3 bucket right away
* This in turn means that the CFN template can be deployed as a changeset - allowing for ongoing updates to the CFN stack to be made

### Connectivity to AWS Secrets Manager

* Components have been added to provide ready-made connectivity to Secrets Manager.
* I.e. components described in the following link have been added to the CFN template / `makefile`: https://docs.aws.amazon.com/mwaa/latest/userguide/connections-secrets-manager.html
* Specifically:
    * The MWAA execution role has been amended to include the policy, `SecretsManagerReadWrite`
    * The Secrets Manager backend has been created as an Apache Airflow configuration option
    * and finally, the `makefile` orchestrates:
        * the generation of the Apache Airflow AWS connection string
        * adds an entry to Secrets Manager for this connection string (using a CFN template)

### How-to run:

The steps involved in building and executing this involve:

1) At the top of the `makefile`, provide a value for the variable:
    * `AWS_PROFILE`: to indicate what AWS_PROFILE to use
2) Following this, run the makefile by typing `make`!

### To do:

* Setup simple example airflow DAGs, e.g. to fetch data from:
    * secrets_manager
        1) configure secrets manager: (in progress)
        https://docs.aws.amazon.com/mwaa/latest/userguide/connections-secrets-manager.html
        2) using a SM key for an airflow connection
        https://docs.aws.amazon.com/mwaa/latest/userguide/samples-secrets-manager.html
    * DMS
    * other
* revert back to the setup, to instead create a build in a private network (see: https://docs.aws.amazon.com/mwaa/latest/userguide/vpc-create.html#vpc-create-template-private-only)
