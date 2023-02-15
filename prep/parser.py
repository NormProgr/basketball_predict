import pandas as pd
from bs4 import BeautifulSoup

# select one year and identify


# for month in months
with open("prep/data/october.html") as f:
    page = f.read()

soup = BeautifulSoup(page, "html.parser")

october_table = soup.find(id="schedule")

october_table_pd = pd.read_html(str(october_table))
