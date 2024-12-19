import token_security
from loguru import logger
import requests
import utils
import time
import os
from tqdm import tqdm

import pandas as pd

destination_folder = (
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "downloads/"
)


def download(
    collection_name: str,
    string_match: str,
    polygon_wkt: str,
    start_date: str,
    end_date: str,
    access_token: str,
    refresh_token: str,
) -> None:

    logger.info("Getting manifests")

    dates = utils.get_date_range(
        start=start_date,
        end=end_date,
        frequency="D",
        format="%Y-%m-%d",
    )

    urls = []
    for date in dates:
        url = f"""https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=OData.CSC.Intersects(area=geography'SRID=4326;{polygon_wkt}') and contains(Name,'{string_match}') and ContentDate/Start gt {date}T00:00:00.000Z and ContentDate/Start lt {date}T23:59:59.999Z"""
        urls.append(url)
    headers = {"Authorization": f"Bearer {access_token}"}

    session = requests.Session()
    session.headers.update(headers)

    # df = []
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    logger.info(f"Downloading data to {destination_folder}")
    for u in tqdm(urls):
        r = requests.get(u)

        count = 0
        while r.status_code != 200:
            time.sleep(3)
            r = requests.get(u)
            count += 1
            if count == 5:
                logger.critical("Can't connect to server")
                raise "Can't connect to server"
                break

        json = r.json()
        manifests = pd.DataFrame.from_dict(json["value"])

        for ix, row in manifests.iterrows():
            if os.path.exists(f"{destination_folder}/{row['Name']}".replace(".nc", "")):
                continue
            logger.info(f"Downloading {row['Name']}")
            url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({row['Id']})/$value"

            response = session.get(url, headers=headers, stream=True)
            if response.status_code != 200:
                logger.critical(response.status_code)

            with open(f"{destination_folder}/{row['Name']}.zip", "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            utils.extract_and_move(
                f"{destination_folder}/{row['Name']}.zip",
                f"{destination_folder}",
                destination_folder,
            )
            # time.sleep(15)
            access_token, refresh_token = token_security.reftoken(refresh_token)
            headers = {"Authorization": f"Bearer {access_token}"}
            session.headers.update(headers)
