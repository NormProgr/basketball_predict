import pandas as pd
from bs4 import BeautifulSoup


def parser(months, scrapedate):
    """Convert tables from html files to one pandas DataFrame.

    Args:
        months (list): list of months to be added to combined dataframe.

    Returns:
        df (pandas DataFrame): Concatenated df with all entries from html tables.

    """
    dfs = []
    for month in months:
        with open(f"src/bask/preparation/data/{month}_{scrapedate}.html") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        table = soup.find(id="schedule")
        table_pd = pd.read_html(str(table), flavor="bs4")[0]
        dfs.append(table_pd)
    df = pd.concat(dfs)
    return df
