import os

import pandas as pd
import pytest
from bask.config import TEST_DIR
from bask.preparation.parser import scrapedate


@pytest.fixture()
def html_files():
    with open(f"src/bask/preparation/data/{month}_{scrapedate()}.html") as f:
        f.read()
    return pd.read_csv(TEST_DIR / "preparation" / "data_fixture.csv")


# Loop over months?
def test_number_html():
    prefixed = [
        filename
        for filename in os.listdir("src/bask/preparation/data")
        if filename.endswith(".html")
    ]
    assert len(prefixed) == 7, "Error: Not the right number of .html files."
