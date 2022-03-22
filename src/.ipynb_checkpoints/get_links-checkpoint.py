#!/usr/bin/python3

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import itertools
import subprocess
from loguru import logger

from src.utils import get_config, get_folder_dir, get_downloaded_dates

# TODO: Try functions with underscore before functions

def _format_date(date_param):
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

    date_str = datetime.strftime(date_param, '%Y-%m-%d')
    return date_str

def _dates_range(date_str, date_end):
    """Creates list of daily sequence of dates in format '%Y-%m-%d'
    Parameters
    ----------

    date_str: 
        start date of sequence
    date_end: 
        end date of sequence
    
    Returns
    -------
    dates_range:
        list of days from start date and end date defined at config.yaml
    """

    dates_range = pd.date_range(date_str, date_end).tolist()

    return(dates_range)

def _create_date(date_str, date_end, reversed = True):
    """Creates list of daily sequence of dates in format '%Y-%m-%d'
    Parameters
    ----------
    date_str: 
        start date of sequence
    date_end: 
        end date of sequence
    number_years:
        number of years previous to range of dates
    
    Returns
    -------
    dates_format:
        list of days from start date and end date defined at config.yaml
    """
    dates_range = _dates_range(date_str, date_end)
    dates_index = pd.DatetimeIndex(dates_range)
    dates_format = list(map(_format_date, dates_index))
    if reversed:
        dates_format.reverse()

    return dates_format

    

def _download_csv_link(date_param, geom_param, current_millis, data_dir):
    """Creates csv file with links to download
    Parameters
    ----------
    date_param: 
        date definition in query
    geom_pol: 
        polygon definition in query
    current_millis:
        date of download
    data_dir:
        path to save data
    """

    logger.info(f"... Getting {date_param} links...")

    cmd_text = f"""sh scripts/dhusget.sh -u "s5pguest" -p "s5pguest" \
    -d "https://s5phub.copernicus.eu/dhus" \
    -l "100" \
    -C "{data_dir}url-list_{date_param}_{current_millis}.csv" \
    -q "data/raw/OSquery-result.xml" \
    -F 'platformname:Sentinel-5 AND producttype:L2__NO2___  AND \
    (beginPosition:[{date_param}T00:00:00.000Z TO {date_param}T23:59:59.999Z] AND \
    endPosition:[{date_param}T00:00:00.000Z TO {date_param}T23:59:59.999Z]) AND \
    ( footprint:"Intersects({geom_param})")'"""
        
    print(cmd_text)
    #subprocess.Popen(cmd_text, shell=True, executable='/bin/bash')
    subprocess.call(cmd_text, shell=True, executable='/bin/bash' )
    # TODO: Try calling the query without messages.
    # subprocess.call(cmd_text, shell=True, executable='/bin/bash', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    
    
    return('Done')

def download_links(config):
    """ Download air pollution data links.
    
    This function runs de bash file from nasa to run query and download
    url list to download data files. 

    The previous code for this process is at
    `/home/dmartinez/private/no2_final/creador_archivos.do`.

    Parameters
    ----------
    config: 
        configurationg file configs/config.yaml
    
    Returns
    -------
    None:
        csv written to `data/urllists`
    """
    dates_range = _create_date(date_str = config['download']['date_str'], 
                               date_end = config['download']['date_end'])

    incoming_dir = get_folder_dir('incoming', config)
    manifest_dir = get_folder_dir('manifest', config)
    processed_dir = get_folder_dir('processed', config)


    downloaded_dates = get_downloaded_dates(incoming_dir, processed_dir)

    print('Before:',len(dates_range))
    print(downloaded_dates)
    dates_range = [x for x in dates_range if x.replace('-','') not in downloaded_dates]
    print('After:',len(dates_range))
    

    #print(dates_range)
   
    logger.info(f"... DOWNLOADING URLS ...")

    for date_param in dates_range:
        result = _download_csv_link(date_param    = date_param, 
                              geom_param      = config['download']['geom_polygon'], 
                              current_millis  = config['current_millis'],
                              data_dir = manifest_dir 
                              )


    logger.info(f"... DONE DOWNLOADING URLS! ...")

    return('Done')
    