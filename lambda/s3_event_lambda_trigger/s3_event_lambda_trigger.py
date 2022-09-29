#!/usr/bin/env python3
"""
Python Version  : 3.8
* Name          : s3_event_lambda_trigger.py
* Description   : Boilerplate s3 event lambda_function script
* Created       : 26-02-2021
* Usage         : python3 s3_event_lambda_trigger.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import sys
from time import time
import boto3
import logging
from urllib.parse import unquote_plus

# set logging
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format="%(message)s", level=logging.INFO)

# create an S3 resource
s3_resource = boto3.resource("s3")


def lambda_handler(event, context):
    """Main entry point of the lambda function"""
    START_TIME = time()
    logging.debug(f"Function called: lambda_handler()")

    # parse the desired event items
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file_uploaded = unquote_plus(event["Records"][0]["s3"]["object"]["key"]).split("/")[-1]  # unquote_plus handles any s3 'percent encoding' characters
    logging.info(f"\n##########\nInput args:\ns3_bucket_name: {bucket_name}\nfile_uploaded: {file_uploaded}\n##########")

    s3_bucket = s3_resource.Bucket(bucket_name)

    logging.debug(f"Function finished: lambda_handler() finished in {round(time() - START_TIME, 2)} seconds")
