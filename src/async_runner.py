#!/usr/bin/python3
import aiohttp
from aiohttp import BasicAuth, TCPConnector
import aiofiles
from loguru import logger
import requests
import shutil
import time
import gc
import asyncio
import time
import functools
import logging
import signal
import sys
from src.utils import get_config, get_folder_dir

import os

import pandas as pd
import glob
from loguru import logger


def _get_csv_paths(path_search):
    
    path_list = [os.path.join(path_search, x) for x in os.listdir(path_search) if x.endswith('.csv')]
        
    return(path_list)

def _read_csv_file(path_csv):
    logger.debug(f"... CSV from {path_csv}...")
    data = pd.read_csv(path_csv, header=None) 
    
    return(data)

def _read_urls(data_dir):
    paths_csvs = _get_csv_paths(path_search = f"{data_dir}")
    data_lists = list()
    
    for path_csv in paths_csvs:
        data = _read_csv_file(path_csv)
        data_lists.append(data)

    data_union = pd.concat(data_lists, ignore_index=True)    
    data_union.columns = ['nombre', 'path']
    return(data_union)


def _clean_rutas(rutas, data_dir):

    # files characteristics
    rutas['data_type'] = rutas['nombre'].str[4:8]
    rutas['day'] = rutas['nombre'].str[20:28]

    # counts per data type and day
    df_counts = rutas.groupby('day').data_type.nunique().reset_index(name='counts')
    
    # filter valid urls
    result = pd.merge(rutas, df_counts, on='day')
    result = result.loc[(result['counts'] == 2) & (result['data_type'] == 'OFFL') | (result['counts'] == 1)]

    logger.debug(print(result.shape))

    result['nombre'] = f"{data_dir}" + result['nombre']

    #result.groupby('day').data_type.nunique().reset_index(name='counts')['counts'].nunique()
    clean_result = result[['path','nombre']].values

    return(clean_result)

                    
async def _get_unique_data_file_2(url2, path_ncfile, session):

    logger.info(f"... getting unique NCFILE ...")
    attempts = 0
    
    url2 = url2 + '/$value'

    while attempts < 15:
        try:
            time.sleep(10)
            async with session.get(url=url2,auth=aiohttp.BasicAuth('s5pguest','s5pguest')) as response:
                logger.debug(f"...Url {url2}...")
                if response.status == 200:
                    #f = await aiofiles.open(path_ncfile, mode='wb')
                    with open(path_ncfile, 'wb') as f:
                        while True:
                            chunk = await response.content.read(65536)
                            if not chunk:
                                break
                            f.write(chunk)
                            del chunk
                            #await f.close()

                    attempts = 15
                    logger.debug(f"downloaded: {url2}")
        except Exception as e:
            gc.collect()
            attempts +=1
            logger.debug(f"...Exception {e}...")
            logger.debug(f"...Exception file {path_ncfile}...")  

sem = asyncio.Semaphore(5)
   
async def safe_download(x, y,session):
    async with sem:  # semaphore limits num of simultaneous downloads
       #async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        return await _get_unique_data_file_2(x, y, session)
    
#added by Santiago Inmediato - Not being called yet

async def asyncfunction(websites):
        async with sem: 
            async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
                tasks = [
                    asyncio.ensure_future(safe_download(x, y, session)) for x,y in websites # creating task starts coroutine
                        ]
                ret = await asyncio.gather(*tasks) 

def async_run(websites):

    start = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncfunction(websites))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

    end = time.time()
    print("Took {} seconds to pull {} websites.".format(end - start, len(websites)))

def download_data(config):
    manifest_dir = get_folder_dir('manifest', config)
    incoming_dir = get_folder_dir('incoming', config)
    rutas = _clean_rutas(_read_urls(data_dir = manifest_dir), data_dir = incoming_dir)
    # rutas = rutas_df.iloc[:5]

    logger.info("... DOWNLOADING DATA ...")

    async_run(rutas)
    
    logger.info(f"... DONE DOWNLOADING DATA :) ...")

    return('Done!')
