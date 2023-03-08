import os

import pandas as pd
from bs4 import BeautifulSoup


def scrapedate():
    """Take the last scraping date as reference date.

    Raises:
            Assert:

    Returns:
        scrapedate (string): The date of the current scrape.

    """
    path = "bld/python/scrapes"
    dir = os.listdir(path)
    if len(dir) != 0:
        prefixed = [filename for filename in dir if filename.startswith("april_")]
        # assert (
        # ), "Error: No data exists, run scraper.py file to generate scrapes."
        parts = prefixed[0].split("_")
        scrapedate = parts[1].split(".")[0]
        return scrapedate


def parser(months, scrapedate):
    """Convert tables from html files to one pandas DataFrame.

    Args:
        months (list): List of months to be added to combined dataframe.
        scrapedate (pandas datetime): Date of the last scrape.

    Returns:
        df (pandas DataFrame): Concatenated df with entries from html tables for all months.

    """
    dfs = []
    for month in months:
        with open(
            f"bld/python/scrapes/{month}_{scrapedate}.html",
            encoding="utf8",
        ) as f:  # added encoding, does it lead to failure?
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        table = soup.find(id="schedule")
        table_pd = pd.read_html(str(table), flavor="bs4")[0]
        dfs.append(table_pd)
    df = pd.concat(dfs)
    return df
