from .bashquery import BashQuery
from .utils import assertDirectory, check_manifests, GetDownloadedFiles, LoadManifestsDF
from .asynciodownloader import async_run
from loguru import logger
import asyncio
from tqdm import tqdm
from shapely.geometry import Polygon, MultiPolygon
from typing import Optional, Union
from pandas import DataFrame
from geopandas import GeoDataFrame, GeoSeries
import os

__all__ = [
    'download_manifests',
    'download_data',
    'download_file'
]

def download_manifests(
    pipeline_name: str,
    manifests_dir: str,
    platformname: str,
    product: str,
    dates: list,
    geom: Union[GeoDataFrame, GeoSeries, Polygon, MultiPolygon],
    verbose = False,
    processingmode: str = 'Offline',
    username: str = 's5pguest',
    password: str = 's5pguest'):

    logger.info(f'DOWNLOADING {len(dates)} MANIFESTS')
    assertDirectory(manifests_dir)
    manifests_dir = os.path.join(manifests_dir, pipeline_name)
    assertDirectory(manifests_dir)
    geom_wkt = geom.envelope.unary_union.wkt
    
    for date in tqdm(dates):
        query_executor = BashQuery(
            manifests_dir,
            platformname,
            product,
            date,
            geom_wkt,
            processingmode,
            username,
            password
            )
        if verbose:
            query_executor.execute()
        else:
            query_executor.silent_execute()
    
    check_manifests(manifests_dir)

def download_data(
    pipeline_name: str,
    manifests_dir: str,
    downloads_dir: str,
    semaphore: int = 5,
    username: str = 's5pguest',
    password: str = 's5pguest',
    attempts_limit = 30,
    queue = None
):
    
    assertDirectory(manifests_dir)
    manifests_dir = os.path.join(manifests_dir, pipeline_name)
    assertDirectory(manifests_dir)

    assertDirectory(downloads_dir)
    downloads_dir = os.path.join(downloads_dir, pipeline_name)
    assertDirectory(downloads_dir)

    websites = LoadManifestsDF(manifests_dir)
    websites.columns = ['file', 'url']

    # We don't want to download already downloaded files.
    downloaded_files = GetDownloadedFiles(downloads_dir)
    websites = websites[~websites['file'].isin(downloaded_files)]

    websites['file'] = downloads_dir + '/' + websites['file']
    targets = websites.values

    logger.info(f'DOWNLOADING {len(targets)} FILES\nCONCURRENT DOWNLOADS LIMITED TO {semaphore}.')

    sem = asyncio.Semaphore(semaphore)
    async_run(username, password, sem, targets, attempts_limit, queue)
    logger.info('DONE DOWNLOADING')


def download_file(
    pipeline_name: str,
    filename: str,
    manifests_dir: str,
    downloads_dir: str,
    semaphore: int = 1,
    username: str = 's5pguest',
    password: str = 's5pguest',
    attempts_limit = 30

):
        
    assertDirectory(manifests_dir)
    manifests_dir = os.path.join(manifests_dir, pipeline_name)
    assertDirectory(manifests_dir)

    assertDirectory(downloads_dir)
    downloads_dir = os.path.join(downloads_dir, pipeline_name)
    assertDirectory(downloads_dir)

    websites = LoadManifestsDF(manifests_dir)
    websites.columns = ['file', 'url']

    websites = websites[websites['file'] == filename]

    websites['file'] = downloads_dir + '/' + websites['file']
    targets = websites.values

    logger.info(f'DOWNLOADING {filename}')

    sem = asyncio.Semaphore(semaphore)
    async_run(username, password, sem, targets, attempts_limit)
    logger.info('DONE DOWNLOADING')