#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : lambda_function.py
* Description   : Boilerplate lambda_function script
* Created       : 26-02-2021
* Usage         : python3 lambda_function.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import sys
from datetime import datetime
from time import time
import logging
import boto3

#import custom modules

#set logging
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format='%(message)s',level=logging.INFO)

current_dt_obj = datetime.now()
current_date_str = current_dt_obj.strftime('%d-%m-%Y')
current_time_str = current_dt_obj.strftime('%H:%M:%S')
#can use 'current_dt_obj' to get other date parts. E.g. 'current_dt_obj.year'

def lambda_handler(event, context):
    """Main entry point of the lambda function"""
    START_TIME = time()
    logging.debug(f"Function called: lambda_handler()")
    #program logic here
    logging.debug(f"Function finished: lambda_handler() finished in {round(time() - START_TIME, 2)} seconds")

    return event

if __name__ == "__main__":
    """ This is executed when run from the command line """
    event = {}
    event['example'] = "example_value"

    lambda_handler(event, 'example_conext')
