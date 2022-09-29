#!/usr/bin/env python3
"""
Python Version  : 3.8
* Name          : s3_event_lambda_trigger.py
* Description   : Script to trigger moving of existing files in an S3 bucket to an archive folder.
                  This lambda function is triggered on an S3 PUT event.
* Created       : 26-02-2021
* Usage         : python3 eg_s3_event_lambda_trigger.py
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

    for s3_obj in s3_bucket.objects.all():
        file_path = s3_obj.key.split("/")

        if len(file_path) == 1:
            s3_file = file_path = s3_obj.key.split("/")[0]
            logging.debug(f"s3_file = {s3_file}")
            if s3_file != file_uploaded:
                logging.debug(f"Filename is different, copy {s3_file} into the /archive folder")
                print("rename the file!")
                logging.debug(f"copy_from args = s3_resource.Object({bucket_name}, archive/{s3_file}).copy_from(CopySource={bucket_name}/{s3_file})")
                s3_resource.Object(bucket_name, f"archive/{s3_file}").copy_from(CopySource=f"{bucket_name}/{s3_file}")

    logging.debug(f"Function finished: lambda_handler() finished in {round(time() - START_TIME, 2)} seconds")
