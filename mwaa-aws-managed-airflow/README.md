# MWAA: i.e. AWS-managed-airflow

## Overview

Streamlined version of the AWS quick start user guide for MWAA (https://docs.aws.amazon.com/mwaa/latest/userguide/quick-start.html). These scrips create: 

* an S3 Bucket and uploads the prerequisite requirements.txt (containing the required airflow-aws package, needed for Airflow with AWS)
* a (public) VPC inftrastructure (private VPC is WIP)
* an AWS MWAA (Managed Workflows for Apache Airflow) environment
* and the SecretsManager configurations

## Contents

1. Customisations
    * S3 bucket creation and prerequisite `requirements.txt`
    * Split out the single 'big bang' AWS MWAA quickstart CFN into 3 logically grouped CFNs
    * Connectivity to AWS Secrets Manager
2. How-to run
3. To-dos

## 1. Customisations

### S3 bucket creation and prerequisite `requirements.txt`

* I've revised the quick start CFN template to instead create the S3 bucket in a separate prerequisite CFN stack
* This way, the required `requirements.txt` (that importantly captures, "apache-airflow-backport-providers-amazon") can be uploaded to the S3 bucket right away
* This in turn means that the CFN template can be deployed as a changeset - allowing for ongoing updates to the CFN stack to be made

### Split out the Quickstart CFN into 3 CFNs

The big bang, single CFN used for the AWS quick start user guide for MWAA (https://docs.aws.amazon.com/mwaa/latest/userguide/quick-start.html) isn't very user friendly and difficult to understand dependencies.

As a result, I've Slightly streamlined version of the AWS quick start user guide for MWAA: 

* As a result, I split the CFN into 3:
    * 1 for the prerequisite S3 bucket
    * 1 for the networking components needed for a public VPC (private VPC is WIP)
    * and 1 for the MWAA env

### Connectivity to AWS Secrets Manager

* Components have been added to provide ready-made connectivity to Secrets Manager.
* I.e. components described in the following link have been added to the CFN template / `makefile`: https://docs.aws.amazon.com/mwaa/latest/userguide/connections-secrets-manager.html
* Specifically:
    * The MWAA execution role has been amended to include the policy, `SecretsManagerReadWrite`
    * The Secrets Manager backend has been created as an Apache Airflow configuration option
    * and finally, the `makefile` orchestrates:
        * the generation of the Apache Airflow AWS connection string
        * adds an entry to Secrets Manager for this connection string (using a CFN template)

## 2. How-to run:

The steps involved in building and executing this involve:

1) At the top of the `makefile`, provide a value for the variable:
    * `AWS_PROFILE`: to indicate what AWS_PROFILE to use
2) Change the input parameters within the config file, `env/config.json` (config_eg.json is a stripped back example, in case I've hidden config.json)
3) Following this, run the makefile by typing `make`!

## 3. To do:

* Setup simple example airflow DAGs, e.g. to fetch data from:
    * secrets_manager
        1) configure secrets manager: (done)
        https://docs.aws.amazon.com/mwaa/latest/userguide/connections-secrets-manager.html
        2) using a SM key for an airflow connection (in progress)
        https://docs.aws.amazon.com/mwaa/latest/userguide/samples-secrets-manager.html
    * DMS
    * DBT
    * Slack (done - but will create version to instead use an Airflow variable)
    * convert CSV to parquet
    * other
* revert back to the setup, to create a private network alternative (see: https://docs.aws.amazon.com/mwaa/latest/userguide/vpc-create.html#vpc-create-template-private-only)
