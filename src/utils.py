#!/usr/bin/python3

import yaml
from datetime import datetime
from loguru import logger
import os
import pandas as pd


def get_config(path):
    """Load configuration file
    
    Parameters
    ----------
    path : str, optional
        config.yaml path, by default 'configs/config.yaml'
    
    Returns
    -------
    dict :
        variables from config.yaml
    """
    
    config = yaml.safe_load(open(path))

    current_time_string = datetime.strftime(
                          datetime.now(),
                          '%Y-%m-%d')
    
    config.update(dict(current_millis=current_time_string))

    return config


def get_folder_dir(target, config):
    if target == 'incoming':
        return f"{config['project_dir']}{config['product']}{config['incoming_dir']}"
    elif target == 'processed':
        return f"{config['project_dir']}{config['product']}{config['processed_dir']}"
    elif target == 'manifest':
        return f"{config['project_dir']}{config['product']}{config['incoming_dir']}{config['manifest_dir']}"
    else:
        pass

def _get_file_code(filename):
    return filename.split('____')[1].split('_')[0]

def _get_date_from_code(code):
    return code.split('T')[0]

def get_downloaded_dates(incoming_dir, processed_dir):

    files_incoming_dir = os.listdir(incoming_dir)
    files_processed_dir = os.listdir(processed_dir)
    files = files_incoming_dir + files_processed_dir
    codes = [_get_file_code(x) for x in files if x.startswith('S5P')]
    dates = set([_get_date_from_code(x) for x in codes])
    return list(sorted(dates))



    
