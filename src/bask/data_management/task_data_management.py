"""Tasks for managing the data."""
import pytask
import yaml

from bask.config import BLD, SRC
from bask.data_management import clean_data

# @pytask.mark.depends_on(
#    },


for time in ["benchmark", "benchmark_pred", "model", "model_pred"]:

    @pytask.mark.depends_on(
        {
            "scripts": ["clean_data.py"],
            "data_info": SRC / "data_management" / "data_info.yaml",
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "data" / f"data_{time}.csv")
    def task_clean_split_data_python(depends_on, produces, time=time):
        data_info = yaml.safe_load(open(depends_on["data_info"]))
        if time == "benchmark":
            df = clean_data(data_info)[0]
        elif time == "benchmark_pred":
            df = clean_data(data_info)[1]
        elif time == "model":
            df = clean_data(data_info)[2]
        else:
            df = clean_data(data_info)[3]
        df.to_csv(produces)
