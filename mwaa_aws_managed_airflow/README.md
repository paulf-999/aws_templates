# Boilerplate for AWS MWAA (i.e. AWS managed service for Airflow)

This is a streamlined version of the [AWS quick start user guide for AWS MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/quick-start.html).

---

## Contents

1. High-level summary
2. Getting started
    * Prerequisites
    * Installation
    * How-to run
3. Additional info - overview of customisations to AWS MWAA quick start
4. Hints and Tips
5. To-do's

---

## 1. High-level summary

These scripts provide a streamlined version of the [AWS quick start user guide for AWS MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/quick-start.html). Where executing the `Makefile` creates the following:

* An S3 Bucket and uploads the prerequisite `requirements.txt` (containing the required `airflow-aws` package - required for AWS MWAA)
* a (public) VPC infrastructure (private VPC implementation to follow)
* an AWS MWAA (Managed Workflows for Apache Airflow) environment
* and the configurations required to allow usage of SecretsManager within Airflow

These customisations are described in greater detail within the section, '
##### Technologies used

AWS CLI, CloudFormation, AWS MWAA, SecretsManager, AWS infrastructure/networking components (VPC, subnets, security groups etc.)

---

## 2. Getting started

### Prerequisites

Before you begin, ensure you have met the following requirements:

* You're using a Mac / Linux machine
* You have admin access to an AWS account, with AWS CLI installed

### Installation

Update the values for the input parameters within `env/config_eg.json`, to use whatever desired names you wish to use.

### How-to run

The steps involved in building and executing this involve:

1) At the top of the `Makefile`, provide a value for the variable `AWS_PROFILE` - to indicate what AWS_PROFILE to use
2) Change the input parameters within the config file, `env/config.json` (`config_eg.json` is a stripped back example, in case I've hidden config.json)
3) Following this, run the Makefile by typing `make`!

---

## 3. Additional info - overview of customisations to AWS MWAA quick start

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
* I.e. components described in the following link have been added to the CFN template / `Makefile`: https://docs.aws.amazon.com/mwaa/latest/userguide/connections-secrets-manager.html
* Specifically:
    * The MWAA execution role has been amended to include the policy, `SecretsManagerReadWrite`
    * The Secrets Manager backend has been created as an Apache Airflow configuration option
    * and finally, the `Makefile` orchestrates:
        * the generation of the Apache Airflow AWS connection string
        * adds an entry to Secrets Manager for this connection string (using a CFN template)

---

## 4. Hints and Tips

### Local MWAA environment

* To run a local Airflow environment to develop and test DAGs, custom plugins, and dependencies before deploying to Amazon MWAA, it's recommended you install and use the MWAA CLI utility
* To run the CLI, see the [aws-mwaa-local-runner](https://github.com/aws/aws-mwaa-local-runner) on GitHub

## 5. To do's:

* demonstrate an Airflow DAG that converts CSV to parquet
* create a private network alternative (see: https://docs.aws.amazon.com/mwaa/latest/userguide/vpc-create.html#vpc-create-template-private-only)
