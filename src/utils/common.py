"""
This is a common program file to perform all the
commonly used tasks that are repeatedly used.

Author: Biswajit Mohapatra
"""


import time
import pandas as pd
import json
import os
import yaml
from application_logger.logging import App_Logger

file_object = open("logs/common.txt","a+")
logging = App_Logger(file_object)

def read_yaml(path_to_yaml: str) -> dict:
    try:
        # read yaml file
        logging.log(f"Reading {path_to_yaml}.")
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
        logging.log(f"{path_to_yaml} was read successfuly!")
        return content
    except OSError as os:
        logging.log(f"Error encountered while reading {path_to_yaml} file.\nErrorMessage :: {os}")
        raise("Exception",os)
    except TypeError as te:
        logging.log(f"Error encountered while reading {path_to_yaml} file.\nErrorMessage :: {te}")
        raise("Exception",te)
    except Exception as ex:
        logging.log(f"Error encountered while reading {path_to_yaml} file.\nErrorMessage :: {te}")
        raise("Exception",ex)
