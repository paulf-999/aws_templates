## mwaa-awa-managed-airflow (WIP)

Follows the following AWS user guide: https://docs.aws.amazon.com/mwaa/latest/userguide/quick-start.html

This template creates:
* a VPC inftrastructure
* S3 Bucket
* and an AWS MWAA (Managed Workflows for Apache Airflow) environment

### How-to run:

The steps involved in building and executing this involve:

1) Providing the name of your AWS_PROFILE to the variable `AWS_PROFILE`
2) Providing the desired name of the S3 bucket to create
3) and run `make`!

### To do:

* Setup simple example airflow DAGs, e.g. to fetch data from:
    * S3
    * DMS
    * other
* revert back to the setup, to instead create a build in a private network
