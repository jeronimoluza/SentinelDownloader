import SentinelDownloader
from SentinelDownloader import utils


def download(destination_folder, s5p_product, polygon_wkt, start_date, end_date):
    """
    This function downloads Sentinel-5P data based on the provided parameters.

    Args:
        destination_folder (str): The path to the folder where the downloaded data will be stored.
        s5p_product (str): The name of the Sentinel-5P product.
        polygon_wkt (str): The Well-Known Text (WKT) representation of the polygon within which the data will be downloaded.
        start_date (str): The start date of the date range in the format 'YYYY-MM-DD'.
        end_date (str): The end date of the date range in the format 'YYYY-MM-DD'.

    Returns:
        None
    """
    config = utils.get_config("configs/config.yaml")
    access_token, refresh_token = SentinelDownloader.token_security.get_access_token(
        config["username"], config["password"]
    )
    manifests = download(
        destination_folder,
        s5p_product,
        polygon_wkt,
        start_date,
        end_date,
        access_token,
        refresh_token,
    )
