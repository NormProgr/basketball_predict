import pandas as pd
from bs4 import BeautifulSoup


def parser(months, scrapedate, path):
    """Convert tables from html files to one pandas DataFrame.

    Args:
        months (list): List of months to be added to combined data frame.
        scrapedate (pandas datetime): Date of the last scrape.

    Returns:
        df (pandas DataFrame): Concatenated df with entries from all months of the
            season.

    """
    dfs = []
    for month in months:
        with open(
            path / f"{month}_{scrapedate}.html",
            encoding="utf8",
        ) as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        table = soup.find(id="schedule")
        table_pd = pd.read_html(str(table), flavor="bs4")[0]
        dfs.append(table_pd)
    df = pd.concat(dfs)
    return df
