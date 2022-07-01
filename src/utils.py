#!/usr/bin/python3
import shutil
import sys
from io import StringIO
import pandas as pd
import yaml
import os
import datetime
from loguru import logger


def _bashConverter(product):
    bashDict = {
        'no2': 'L2__NO2___',
        'co': 'L2__CO___',
        'aod': 'L2__AER_AI'
    }
    return bashDict[product]

def LoadFiles(directory, extension = 'csv'):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(extension)]

def LoadConfig(configfile):
    with open(configfile, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def DateRange(startdate, enddate):
    return pd.date_range(startdate, enddate)

def gTileCode(filename):
     return filename.split('.')[2]

def gDateCode(filename):
     return filename.split('.')[1].lstrip('A')

def PrintMessage(config):
    logger.info('----- READING CONFIG.YAML ------')
    logger.info(f"DOWNLOADING {config['product'].upper()} DATA")
    logger.info(f'DOWNLOADING DATES FROM {config["startDate"]} TO {config["endDate"]}')


def GetDataPaths(destinationFolder, product):
    dir_path = os.path.join(destinationFolder, product)
    downloadsFolder = os.path.join(dir_path, 'downloaded/')
    manifestsFolder = os.path.join(dir_path, 'manifests/')
    
    try:
        os.mkdir(destinationFolder)
    except Exception as e:
        pass
    
    try:
        os.mkdir('scripts')
    except Exception as e:
        pass
    
    if os.path.exists(dir_path):
        logger.info(f'Project dir: {dir_path}')
        pass
    else:
        os.mkdir(dir_path)
        try:
            os.mkdir(downloadsFolder)
        except Exception as e:
            pass
        try:
            os.mkdir(manifestsFolder)
        except Exception as e:
            pass
        #logger.info(f'Project dir: {dir_path}')
    return dir_path, downloadsFolder, manifestsFolder

def _get_file_code(filename):
    return filename.split('____')[1].split('_')[0]

def _get_date_from_code(code):
    return code.split('____')[1].split('T')[0]

def _get_manifest_date(manifest_path):
    if manifest_path.startswith('url-list'):
        return manifest_path.split('_')[1]
    else:
        return manifest_path.split('url-list_')[-1].split('_')[0]

def FormatDate(date_param):
    """Date parameter in format '%Y-%m-%d'
    Parameters
    ----------
    date_param: 
        start date of sequence
    
    Returns
    -------
    dates_format:
        list of days from start date and end date defined at config.yaml
    """

    #date_str = datetime.strftime(date_param, '%Y-%m-%d')
    date_str = date_param.strftime('%Y-%m-%d')
    return date_str