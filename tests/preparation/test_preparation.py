import pandas as pd
import pytest
from bask.config import TEST_DIR
from bask.preparation.scraper import scrapedate


@pytest.fixture()
def html_files():
    with open(f"src/bask/preparation/data/{month}_{scrapedate}.html") as f:
        f.read()
    return pd.read_csv(TEST_DIR / "preparation" / "data_fixture.csv")


# Loop over months?
