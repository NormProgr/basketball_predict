import pandas as pd
from bs4 import BeautifulSoup

# select one year and identify

with open("prep/data/april.html") as f:
    page = f.read()

soup = BeautifulSoup(page, "html.parser")

april_table = soup.find(id="schedule")

april_table_pd = pd.read_html(april_table)
