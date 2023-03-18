"""Tasks for managing the data."""

import pandas as pd
import pytask
import yaml

from bask.config import BLD, SRC
from bask.data_management import clean_data
from bask.preparation.scraper import scrapedate

datasets = ["benchmark", "benchmark_pred", "model", "model_pred"]

for time in datasets:

    @pytask.mark.depends_on(
        {
            "scripts": ["clean_data.py"],
            "data_info": SRC / "data_management" / "data_info.yaml",
            "data": BLD / "python" / "parsed" / f"data_{scrapedate()}.pkl",
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "data" / f"data_{time}.pkl")
    def task_clean_split_data(depends_on, produces, time=time):
        """Split the cleaned data into four data sets for analysis."""
        data_info = yaml.safe_load(open(depends_on["data_info"]))
        data = pd.read_pickle(depends_on["data"])
        df = clean_data(data_info, data)[datasets.index(time)]
        df.to_pickle(produces)
