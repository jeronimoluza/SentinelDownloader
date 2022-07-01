import os
from loguru import logger
from src.async_runner import download_data
from src.get_links import download_new_links
from src.utils import GetDataPaths
from src.utils import LoadConfig, PrintMessage


def download_pipeline(destinationFolder, product, startDate, endDate, polygonWKT):
    
    dir_path, downloadsFolder, manifestsFolder = GetDataPaths(destinationFolder, product)
    logger.info('... DOWNLOADING NEW DATA ...')
    # downloads urls 
    #dates_range = download_new_links()
    download_new_links(manifestsFolder, product, startDate, endDate, polygonWKT)
    # download data
    #download_data(dates_range)
    download_data(manifestsFolder, downloadsFolder)


config = LoadConfig('config.yaml')
print(config)
PrintMessage(config)
product = config['product']
destinationFolder = config['destinationFolder']
geometry = config['polygonWKT']
startDate = config['startDate']
endDate = config['endDate']
#print(dates)

download_pipeline(destinationFolder, product, startDate, endDate, geometry)