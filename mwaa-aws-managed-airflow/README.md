## mwaa-awa-managed-airflow (WIP)

Follows the AWS quick start user guide for MWAA: https://docs.aws.amazon.com/mwaa/latest/userguide/quick-start.html

This template creates:
* a VPC inftrastructure
* S3 Bucket
* and an AWS MWAA (Managed Workflows for Apache Airflow) environment

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
* revert back to the setup, to instead create a build in a private network
