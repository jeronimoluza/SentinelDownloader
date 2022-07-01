#!/usr/bin/python3
import os
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import itertools
import subprocess
from loguru import logger
from src.utils import GetDataPaths, _bashConverter, DateRange, FormatDate


def _download_csv_link(date_param, geom_param, current_millis, data_dir, product):
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
    date_param = FormatDate(date_param)
    logger.info(f"... Getting {date_param} links...")

    bashProduct = _bashConverter(product)

    cmd_text = f"""sh $PWD/scripts/dhusget.sh -u "s5pguest" -p "s5pguest" \
    -d "https://s5phub.copernicus.eu/dhus" \
    -l "100" \
    -C "{data_dir}url-list_{date_param}_{current_millis}.csv" \
    -q "OSquery-result.xml" \
    -F 'platformname:Sentinel-5 AND producttype:{bashProduct}  AND processingmode:Offline \
    (beginPosition:[{date_param}T00:00:00.000Z TO {date_param}T23:59:59.999Z] AND \
    endPosition:[{date_param}T00:00:00.000Z TO {date_param}T23:59:59.999Z]) AND \
    ( footprint:"Intersects({geom_param})")'"""
        

    subprocess.call(cmd_text, shell=True, executable='/bin/bash')    
    
    return('Done')

def download_new_links(manifestsFolder, product, startDate, endDate, polygonWKT):
        
    dates_range = DateRange(startDate, endDate)
            
    current_millis = datetime.datetime.today().date().strftime('%Y-%m-%d')
    
    for date in dates_range:
        _download_csv_link(date, polygonWKT, current_millis, manifestsFolder, product)
   
    logger.info(f"... DOWNLOADING URLS ...")
    
    #return dates_range
