import os
import socket
from datetime import date

import requests as req

from bask.preparation.parser import scrapedate

months = ["october", "november", "december", "january", "february", "march", "april"]


def _remove_old_scrapes(folder_path):
    """Delete old scrapes to save memory and for overview."""
    dir = os.listdir(folder_path)
    if len(dir) == 7 and scrapedate() == date.today():
        True
    else:
        folder_contents = os.listdir(folder_path)
        for item in folder_contents:
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path) and item_path.endswith(".html"):
                os.remove(item_path)


def _check_internet():
    """Check whether or not there is a internet connection.

    Return:
        True (boolean): There is a internet connection.
        False (boolean): There is no internet connection.

    """
    try:
        # Attempt to create a connection to the Cloudflare public DNS server
        conn = socket.create_connection(("1.1.1.1", 53))
        conn.close()
        return True
    except OSError:
        return False


def scraper_by_month(path, month, url_start):
    """Scrape the data by month and save it, remove old scrapes.

    Args:
        months (list): List of months to be scraped.
        url_start (url): Source url to scrape data.

    """
    if _check_internet():
        _remove_old_scrapes(path)
        if len(os.listdir(path)) != 7:
            for month in months:
                url = url_start.format(month)
                data = req.get(url)

                with open(
                    path / f"{month}_{date.today()}.html",
                    "w+",
                    encoding="utf8",
                ) as f:
                    f.write(data.text)
