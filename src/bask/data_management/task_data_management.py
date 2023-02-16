"""Tasks for managing the data."""
import pytask
import yaml

from bask.config import BLD, SRC
from bask.data_management import clean_data


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data_info": SRC / "data_management" / "data_info.yaml",
    },
)

# Add loop here! for 4 dataframes (current and benchmark past and future)
@pytask.mark.produces(BLD / "python" / "data" / "data_clean_past.pkl")
def task_clean_split_data_python(depends_on, produces):
    data_info = yaml.safe_load(open(depends_on["data_info"]))
    df = clean_data(data_info)[0]
    df.to_pickle(produces)
