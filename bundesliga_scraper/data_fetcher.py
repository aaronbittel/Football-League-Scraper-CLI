"""Module for fetching requested data and extracting information from HTML using 
request
"""

import requests
from bs4 import BeautifulSoup


def fetch_html(url: str) -> BeautifulSoup:
    """Fetching the html for the given url

    Args:
        url (str): url

    Returns:
        BeautifulSoup: Beautifulsoup object
    """
    response = requests.get(url, timeout=10)

    # TODO Handle response.status_code != 200

    return BeautifulSoup(response.text, "html.parser")
