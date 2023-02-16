import pandas as pd
from bs4 import BeautifulSoup

months = ["october", "november", "december", "january", "february", "march", "april"]


def convert_to_df(months=months):
    """Convert tables from html files to one pandas DataFrame.

    Args:
        months (list): list of months to be added to combined dataframe.

    Returns:
        df (pandas DataFrame): Concatenated df with all entries from html tables.

    """
    dfs = []
    for month in months:
        with open(f"prep/data/{month}.html") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        table = soup.find(id="schedule")
        table_pd = pd.read_html(str(table), flavor="bs4")[0]
        dfs.append(table_pd)
    df = pd.concat(dfs)
    return df


def produce_data():
    """Save pandas df with entries from html tables in src folder."""
    df = convert_to_df()
    df.to_csv("./src/bask/data/data.csv")
    df.to_pickle("./src/bask/data/data.pkl")


produce_data()
