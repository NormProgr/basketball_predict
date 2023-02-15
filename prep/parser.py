import pandas as pd
from bs4 import BeautifulSoup
from scraper import months

dfs = []
for month in months:
    with open(f"prep/data/{month}.html") as f:
        page = f.read()
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find(id="schedule")
    table_pd = pd.read_html(str(table), flavor="bs4")[0]

    dfs.append(table_pd)

df = pd.concat(dfs)


df.to_csv("./src/data/data.csv")
df.to_pickle("./src/data/data.pkl")
