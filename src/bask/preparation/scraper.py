import os
from datetime import date

import requests as req

from bask.config import BLD


def _remove_old_scrapes(folder_path):
    """Delete old scrapes to save memory and for overview."""
    folder_contents = os.listdir(folder_path)
    for item in folder_contents:
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item_path.endswith(".html"):
            os.remove(item_path)


def _check_internet(url="https://github.com/", timeout=5):
    """Check whether or not there is a internet connection.

    Args:
        url (string): The URL to be used for the connectivity test. Default value is "https://github.com/".
        timeout (integer): The maximum time, in seconds, allowed for the request to complete. Default value is 5 seconds.

    Return:
        True (boolean): There is a internet connection.
        False (boolean): There is no internet connection.

    """
    try:
        _ = req.head(url, timeout=timeout)
        return True
    except req.ConnectionError:
        pass
    return False


def scrapedate():
    """Take the last scraping date as reference date.

    Raises:
            Assert: If not 7 scrapes exist.

    Returns:
        scrapedate (string): The date of the current scrapes.

    """
    path = BLD / "python" / "scrapes"
    dir = os.listdir(path)
    assert (
        len(dir) == 7
    ), "Error: Scrapes don't exists, run scraper.py file to generate scrapes."
    prefixed = [file for file in dir if file.startswith("april_")]
    parts = prefixed[0].split("_")
    scrapedate = parts[1].split(".")[0]
    return scrapedate


def scraper(path, months, url_start):
    """Scrape the data by month if there are no scrapes from today, remove old scrapes.

    Args:
        months (list): List of months to be scraped.
        url_start (url): Source url to scrape data.

    """
    if _check_internet():
        if len(os.listdir(path)) != 7:
            _remove_old_scrapes(path)
        elif date.today().strftime("%Y-%m-%d") != scrapedate():
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
