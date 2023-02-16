import pandas as pd
from bs4 import BeautifulSoup
from scraper import months, today


def convert_to_df(months=months, scrapedate=today):
    """Convert tables from html files to one pandas DataFrame.

    Args:
        months (list): list of months to be added to combined dataframe.

    Returns:
        df (pandas DataFrame): Concatenated df with all entries from html tables.

    """
    dfs = []
    for month in months:
        with open(f"prep/data/{month}_{scrapedate}.html") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        table = soup.find(id="schedule")
        table_pd = pd.read_html(str(table), flavor="bs4")[0]
        dfs.append(table_pd)
    df = pd.concat(dfs)
    return df


def produce_data(name=f"data_{today}"):
    """Save pandas df with entries from html tables in src folder."""
    df = convert_to_df()
    df.to_pickle(f"./src/bask/data/{name}.pkl")


produce_data()
