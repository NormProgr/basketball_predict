"""Tasks for managing the data."""
import pytask
import yaml

from bask.config import BLD, SRC
from bask.data_management import clean_data

datasets = ["benchmark", "benchmark_pred", "model", "model_pred"]
for time in datasets:

    @pytask.mark.depends_on(
        {
            "scripts": ["clean_data.py"],
            "data_info": SRC / "data_management" / "data_info.yaml",
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "data" / f"data_{time}.pkl")
    def task_clean_split_data_python(depends_on, produces, time=time):
        data_info = yaml.safe_load(open(depends_on["data_info"]))
        df = clean_data(data_info)[datasets.index(time)]
        df.to_pickle(produces)
