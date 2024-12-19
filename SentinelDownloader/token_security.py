from loguru import logger
import requests
import time
import os
import json


def get_access_token(username: str, password: str) -> tuple[str, str]:
    """
    This function retrieves an access token and a refresh token from the Copernicus Data Store (CDS)
    using the provided username and password. The tokens are used for authentication and authorization
    when accessing CDS data.

    Args:
        username (str): The username for the CDS account.
        password (str): The password for the CDS account.

    Returns:
        tuple[str, str]: A tuple containing the access token and the refresh token.

    Raises:
        Exception: If the access token creation fails, an exception is raised with the response from the server.
    """
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Access token creation failed. Reponse from the server was: {r.json()}"
        )
    response = r.json()
    return response["access_token"], response["refresh_token"]


def reftoken(rtkn: str) -> tuple[str, str]:
    """
    This function refreshes the access token and the refresh token using the provided refresh token.
    If the tokens are not present in the response, it logs an error message, sleeps for 1 hour, and then calls itself recursively.

    Args:
        rtkn (str): The refresh token used to refresh the access token and the refresh token.

    Returns:
        tuple[str, str]: A tuple containing the refreshed access token and the refreshed refresh token.

    Raises:
        None
    """
    response = json.loads(
        os.popen(
            f"curl --location --request POST 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token' \
            --header 'Content-Type: application/x-www-form-urlencoded' \
            --data-urlencode 'grant_type=refresh_token' \
            --data-urlencode 'refresh_token={rtkn}' \
            --data-urlencode 'client_id=cdse-public'"
        ).read()
    )
    if "access_token" not in response.keys() or "refresh_token" not in response.keys():
        logger.error("Token Error:")
        logger.error(response)
        time.sleep(3600)
        return reftoken(rtkn)
    access_token = response["access_token"]
    refresh_token = response["refresh_token"]
    return access_token, refresh_token
