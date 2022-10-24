import aiohttp
from aiohttp import BasicAuth, TCPConnector
import aiofiles
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
import os
import pandas as pd
from loguru import logger
from SentinelDownloader.utils import GetFileFromPath

        
async def GetSingleDataFile(username, password, path_ncfile, url, session, attempts_limit):
    
    code = GetFileFromPath(path_ncfile)
    logger.info(f"... DOWNLOADING {code} ...")
    attempts = 1
    
    product_url = url + '/$value'
    while attempts < attempts_limit:
        try:
            time.sleep(10)
            async with session.get(url=product_url,auth=aiohttp.BasicAuth(username,password)) as response:
                #logger.debug(f"...GETTING {product_url}...")
                if response.status == 200:
                    with open(path_ncfile, 'wb') as f:
                        while True:
                            chunk = await response.content.read(65536)
                            if not chunk:
                                break
                            f.write(chunk)
                            del chunk

                    attempts = attempts_limit
                    logger.info(f"DOWNLOADED: {code}")

        except Exception as e:
            logger.debug(f"DOWNLOAD FAILED:\nAttempt {attempts}\nFile {code}\nException: {e}\nRESTARTING DOWNLOAD") 
            attempts +=1

async def safe_download(username, password, sem, x, y,session, attempts_limit):
    async with sem:  # semaphore limits num of simultaneous downloads
        return await GetSingleDataFile(username, password, x, y, session, attempts_limit)
    
async def asyncfunction(username, password, sem, websites, attempts_limit):
    async with sem:
        async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            tasks = [
                asyncio.ensure_future(safe_download(username, password, sem, x, y, session, attempts_limit)) for x,y in websites # creating task starts coroutine
                    ]
            ret = await asyncio.gather(*tasks) 

def async_run(username, password, sem, websites, attempts_limit = 30):
    start = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncfunction(username, password, sem, websites, attempts_limit))
    except Exception as e:
        logger.debug(e)
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    end = time.time()
    logger.info('DONE DOWNLOADING')
    logger.info(f"Took {(end - start)/60} minutes to download {len(websites)} files.")