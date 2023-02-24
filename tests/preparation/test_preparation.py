import os
from datetime import datetime

import pandas as pd
import pytest
from bask.config import TEST_DIR
from bask.preparation.parser import parser, scrapedate
from bask.preparation.scraper import months


@pytest.fixture()
def html_files():
    with open(f"src/bask/preparation/data/{month}_{scrapedate()}.html") as f:
        f.read()
    return pd.read_csv(TEST_DIR / "preparation" / "data_fixture.csv")


# Loop over months?
def test_scraper_by_month():
    """Test whether the correct amount of files is generated.

    Raises:
        Assert: Raises an error if the 7 months long basketball season is not represented by 7 html files.
        If not, the function scraper_by_month or _remove_old_scrapes does not work as intended.

    """
    prefixed = [
        filename
        for filename in os.listdir("src/bask/preparation/data")
        if filename.endswith(".html")
    ]
    assert len(prefixed) == 7, "Error: Not the right number of .html files."


def test_parser():
    """Test if the right amount of months is parsed.

    Raises:
        Assert: Raises an error if not the 7 months by name are represented in the data.

    """
    df = parser(months, scrapedate())
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
