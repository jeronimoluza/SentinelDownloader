#!/usr/bin/python3

import yaml
from datetime import datetime
from loguru import logger
import os
import pandas as pd
from netCDF4 import Dataset


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


def nc_files_list(data_dir):
    '''
    Retrieves nc files list'''
    nc_dir = f'{data_dir}ncfiles/'
    nfl = list()
    for file in os.listdir(nc_dir):
        if 'S5P_OFFL_L2__NO2' in file:
            nfl.append(file)
    
    return nfl

def nc_file_integrity(data_dir):
    '''
    Checks integrity of nc files by opening them
    Returns
    -------
    list :
        files that are complete and ready for reading'''
    
    txt_location = f'{data_dir}urls/downloaded/downloaded.txt'
    good_files = list()
    nc_dir = f'{data_dir}ncfiles/'
    for file in nc_files_list(data_dir):
        try:
            Dataset(f'{nc_dir}{file}', 'r')
            good_files.append(file)
        except:
            os.remove(f'{nc_dir}{file}')
            continue
    logger.debug(f'... {len(good_files)} DOWNLOADED AND CHECKED FILES ...')
    with open(txt_location, 'w') as f:
        for file in good_files:
            f.write(file + "\n")
        f.close()


def file_checker(data_dir):
    """Checks for downloaded files and writes list 
    to avoid downloading them again
    """
    logger.debug(f'... CHECKING FILES DOWNLOAD PROGRESS ...')
    nc_file_integrity(data_dir)
    
    
    nc_files = nc_files_list(data_dir)
    downloaded = get_downloaded_list(data_dir)
    
    files_to_skip = [file for file in nc_files if file in downloaded]
    
    return files_to_skip



    