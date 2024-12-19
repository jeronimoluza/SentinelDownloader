import os
import yaml
import shutil
import zipfile
import pandas as pd


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


def get_date_range(start: str, end: str, frequency: str, format: str) -> list:
    """Creates a date range corresponding to the dates of analysis

    Args:
        start (str): start date of pipeline
        end (str): end date of pipeline

    Returns:
        list: list of dates in YYYY-mm-dd format.
    """
    dates_range = pd.date_range(start, end, freq=frequency).tolist()
    return [date.date().strftime(format) for date in dates_range]


def extract_and_move(
    zip_file_path: str, extraction_folder: str, destination_folder: str
) -> None:
    """
    Extracts a zip file and moves the contents of the zip file to a specified destination folder.
    The function also removes the .nc extension from the file and the folder has the same name.

    Args:
        zip_file_path (str): The path to the zip file to be extracted.
        extraction_folder (str): The path to the folder where the zip file will be extracted.
        destination_folder (str): The path to the folder where the extracted files will be moved.

    Returns:
        None
    """
    # We add this because we want to remove .nc extension from the file and the folder has the same name. We delete the folder later
    extraction_folder += "_extraction"

    # Create the extraction folder if it doesn't exist
    if not os.path.exists(extraction_folder):
        os.makedirs(extraction_folder)

    try:
        # Extract the contents of the zip file
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extraction_folder)

        # Move files ending with ".nc" to the destination folder
        for root, dirs, files in os.walk(extraction_folder):
            for file in files:
                if file.endswith(".nc"):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(destination_folder, file)
                    shutil.move(source_path, destination_path.replace(".nc", ""))

        # Optional: Remove the extraction folder if needed
        shutil.rmtree(os.path.dirname(source_path))
    except zipfile.BadZipFile as e:
        pass

    # Remove the zip file after extraction and moving the contents
    os.remove(zip_file_path)

    # Remove the extraction folder
    os.rmdir(extraction_folder)
