import os
import geopandas as gpd
import pandas as pd
from shapely import wkt
from loguru import logger
import yaml

__all__ = [
    'get_config',
    'WKTtoGDF',
    'GetFileFromPath',
    'GetDateRange',
    'assertDirectory',
    'load_extension_files',
    'GetDownloadedFiles',
    'LoadManifestsDF',
    'check_manifests',
    'clean_dirs'
]

def get_config(path):
    """Load configuration file
    Parameters
    ----------
    path : str
        config path
    Returns
    -------
    dict
        variables from config.yaml
    """

    config = yaml.load(open(path), Loader=yaml.SafeLoader)
    return config

def WKTtoGDF(geom_wkt: str):
    return gpd.GeoDataFrame([wkt.loads(geom_wkt)], columns = ['geometry'])

def GetFileFromPath(path: str):
    return path.split('/')[-1]

def GetDateRange(start: str , end: str) -> list:
    """creates a date range corresponding to the dates of analysis

    Args:
        start (str): start date of pipeline
        end (str): end date of pipeline

    Returns:
        list: list of dates in YYYY-mm-dd format.
    """
    dates_range = pd.date_range(start, end).tolist()
    return [date.date().strftime('%Y-%m-%d') for date in dates_range]

def GetTimeWindow(
    years: list,
    months: list,
    days:list
    ):
    pass

def assertDirectory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def clean_dirs(paths: list):
    for p in paths:
        os.system(f'rm -r {p}')

def load_extension_files(path: str, extension: str):
    return [os.path.join(path, file) for file in os.listdir(path) if file.endswith(extension)]

def GetDownloadedFiles(downloads_dir):
    return [file for file in os.listdir(downloads_dir) if file.startswith('S5P')]

def LoadManifestsDF(manifests_path):
    manifests_dfs = []
    files = load_extension_files(manifests_path, extension = 'csv')
    c = 0
    
    for file in files:
        try:
            df = pd.read_csv(file, header = None)
            manifests_dfs.append(df)
        except pd.errors.EmptyDataError as e:
            #logger.debug(e)
            c += 1
            continue
    
    if len(files) == c:
        logger.debug('ALL MANIFESTS ARE EMPTY')
    else:
        logger.debug(f'{c} MANIFESTS ARE EMPTY')
    return pd.concat(manifests_dfs)

def check_manifests(manifest_dir: str):
    files = load_extension_files(manifest_dir, extension = 'csv')
    c = 0
    for file in files:
        try:
            data = pd.read_csv(file, header = None)
        except Exception as e:
            logger.debug(e)
            c += 1
    if len(files) == c:
        logger.debug('ALL MANIFESTS ARE EMPTY')
    else:
        logger.debug(f'{c} MANIFESTS ARE EMPTY')
    logger.info(f'SUCCESSFULLY DOWNLOADED {len(files)} MANIFESTS')