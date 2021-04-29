## mwaa-awa-managed-airflow (WIP)

Follows the AWS quick start user guide for MWAA: https://docs.aws.amazon.com/mwaa/latest/userguide/quick-start.html

This template creates:
* a VPC inftrastructure
* S3 Bucket
* and an AWS MWAA (Managed Workflows for Apache Airflow) environment

### How-to run:

The steps involved in building and executing this involve:

1) At the top of the `makefile`, provide values for the variables:
    * `AWS_PROFILE`: to indicate what AWS_PROFILE to use
    * `S3_BUCKET`: to specify the name of the S3 bucket to create
2) Following this, run the makefile by typing `make`!

### To do:

* Setup simple example airflow DAGs, e.g. to fetch data from:
    * S3
    * DMS
    * other
* revert back to the setup, to instead create a build in a private network
