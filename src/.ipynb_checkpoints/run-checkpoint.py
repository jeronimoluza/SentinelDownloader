import os
from loguru import logger

from src.utils import get_config
from src.get_links import download_links
from src.async_runner import download_data
#from src


def download_pipeline(config):
    
    logger.info('... DOWNLOAD START ...')
    # downloads urls 
    # download_links(config)
    download_links(config)
    # download data
    download_data(config)


def run_pipeline():
    config = get_config('config/config_local.yaml')
    path = config['project_dir']
    os.chdir(path)
    print(os.getcwd())
    download_pipeline(config)