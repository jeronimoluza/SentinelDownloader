from netCDF4 import Dataset
import pandas as pd
import datetime
import os
from loguru import logger
import pickle
import gc
from src.utils import _get_satellite_data_paths, _get_date_from_code
from src.async_runner import _read_urls, _clean_rutas, async_run
import concurrent.futures


def _get_all_nc_files(path):
    return [x for x in os.listdir(path) if x.startswith('S5P')]

def test_all_files(path):
    files = [os.path.join(path, x) for x in _get_all_nc_files(path)]
    
    bad_files = []
    c_success = 0
    c_corrupt = 0
    for file in files:
        if file not in worse_files:
            logger.debug(f'... TESTING FILE {file.split("/")[-1]} ...')
            try:
                with Dataset(file, 'r') as ds:
                    pass
                logger.debug(f'... SUCCESS ...')
                c_success += 1
            except Exception as e:
                #print(e)
                code = file.split("/")[-1]
                bad_files.append(code)
                logger.debug(f'... CORRUPT FILE ...')
                c_corrupt += 1
            gc.collect()
        logger.info(f'SUCCEEDED FILES -> {c_success}, CORRUPT FILES -> {c_corrupt}', end = '\r')
    return bad_files



def _get_date_ranges_from_bad(bad_files):
    dates = [pd.to_datetime(_get_date_from_code(code.split('/')[-1])) for code in bad_files]
    return min(dates), max(dates)


def download_broken():
    logger.info(f'... TESTING FOR CORRUPT FILES ...')

    dir_path, incoming_dir, processednc_dir, manifests_dir, raworc_dir, processedorc_dir = _get_satellite_data_paths(product)

    bad_files = test_all_files(incoming_dir)
    
    bad_files = bad_files + ['S5P_OFFL_L2__NO2____20190307T200007_20190307T214137_07242_01_010202_20190314T070352',
                        'S5P_OFFL_L2__NO2____20200525T192317_20200525T210447_13555_01_010302_20200527T120955']

    logger.info(f'... {len(bad_files)} CORRUPT FILES DETECTED ...')

    for file in bad_files:
        logger.debug(f'... {file.split("/")[-1]} ...')

    min_date, max_date = _get_date_ranges_from_bad(bad_files)

    dates_range = pd.date_range(start = min_date, end = max_date)

    urls = _read_urls(manifests_dir)
    urls = urls[urls['nombre'].isin(bad_files)]

    rutas = _clean_rutas(urls, incoming_dir, processednc_dir, replace_existing = True)

    logger.info(f'... RECOVERING CORRUPT FILES ...')
    logger.info(f'... DOWNLOADING ...')

    async_run(rutas)

    logger.info(f'... DONE ...')