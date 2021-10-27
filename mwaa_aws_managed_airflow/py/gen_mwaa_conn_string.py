#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : gen_mwaa_conn_string.py
* Description   : Script to generate the MWAA connection string
* Created       : 22-05-2021
* Usage         : python3 boilerplate.py ${CONN_TYPE} ${AIRFLOW_UI_URL} ${LOGIN} ${PASS} ${ROLE_ARN} ${REGION} ${AWS_PROFILE}
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import sys
from datetime import datetime
from time import time
import logging

# import custom modules
import urllib.parse

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("application_logger")
logger.setLevel(logging.INFO)
# by default, turn off log outputs. But if desired, change this arg to True
# logger.propagate = False

current_dt_obj = datetime.now()
current_date_str = current_dt_obj.strftime("%d-%m-%Y")
current_time_str = current_dt_obj.strftime("%H:%M:%S")
# can use 'current_dt_obj' to get other date parts. E.g. 'current_dt_obj.year'


def main():
    """Main entry point of the app"""
    START_TIME = time()
    logger.debug("Function called: main()")

    conn_string = "{0}://{1}:{2}@{3}?role_arn={4}&region_name={5}".format(conn_type, airflow_ui_url, login, password, role_arn, region_name)
    print(conn_string)

    logger.debug(f"Function finished: main() finished in {round(time() - START_TIME, 2)} seconds")

    return


if __name__ == "__main__":
    """This is executed when run from the command line"""
    conn_type = sys.argv[1]
    airflow_ui_url = sys.argv[2]
    login = sys.argv[3]
    password = sys.argv[4]
    role_arn = sys.argv[5]
    region_name = sys.argv[6]
    aws_profile = sys.argv[7]

    conn_string = "{0}://{1}:{2}@{3}?role_arn={4}&region_name={5}".format(conn_type, airflow_ui_url, login, password, role_arn, region_name)
    print(conn_string)

    main()
