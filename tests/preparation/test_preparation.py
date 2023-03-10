import os
from datetime import datetime

import pandas as pd
import pytest
import requests as req
from bask.config import BLD, TEST_DIR
from bask.preparation.parser import parser
from bask.preparation.scraper import _check_internet, scrapedate


@pytest.fixture()
def html_files():
    with open(f"src/bask/preparation/data/{month}_{scrapedate()}.html") as f:
        f.read()
    return pd.read_csv(TEST_DIR / "preparation" / "data_fixture.csv")


# Loop over months?
def test_scraper():
    """Test whether the correct amount of files is generated.

    Raises:
        Assert: Raises an error if the 7 months long basketball season is not represented by 7 html files.
        If not, the function scraper_by_month or _remove_old_scrapes does not work as intended.

    """
    prefixed = [
        filename
        for filename in os.listdir("bld/python/scrapes")
        if filename.endswith(".html")
    ]
    assert len(prefixed) == 7, "Error: Not the right number of .html files."


def test_parser():
    """Test if the right amount of months is parsed.

    Raises:
        Assert: Raises an error if not the 7 months by name are represented in the data.

    """
    path = BLD / "python" / "scrapes"
    months = [
        "october",
        "november",
        "december",
        "january",
        "february",
        "march",
        "april",
    ]
    df = parser(months, scrapedate(), path)
    parts = []
    for date_str in df["Date"]:
        mon = date_str.split(" ")[1]
        parts.append(mon)
    parts = set(parts)
    assert len(parts) == len(
        months,
    ), f"Error: Wrong number of months in data frame. Data frame includes {parts}."


def test_scrapedate():
    """Check whether scrapedate function returns the right format.

    Raises:
        Assert: Raises an error if the expected format of date and the used format are different.

    """
    expected_format = "%Y-%m-%d"
    scrape = scrapedate()
    assert datetime.strptime(
        scrape,
        expected_format,
    ), f"Error: scrapedate {scrape} is not a valid date."


def test_check_internet(url="https://github.com/", timeout=5):
    """Check whether there is an internet connection.

    Args:
        url (string): The URL to be used for the connectivity test. Default value is "https://github.com/".
        timeout (integer): The maximum time, in seconds, allowed for the request to complete. Default value is 5 seconds.


    Raises:
        Assert: Raises an error if there is an internet connection to the one url but not to the other.

    """
    check = _check_internet()
    try:
        _ = req.head(url, timeout=timeout)
        snd_check = True
    except OSError:
        snd_check = False
    assert check == snd_check, "Internet connection is not available."
