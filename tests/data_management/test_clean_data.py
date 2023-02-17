import pandas as pd
import pytest
import yaml
from bask.config import TEST_DIR
from bask.data_management.clean_data import *

# What to test:

# clean columns:
# whether dropped columns still exist
# Whether old names still exist (maybe also if new ones exist)


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "data_management" / "data_fixture.csv")


@pytest.fixture()
def data_info():
    return yaml.safe_load(open(TEST_DIR / "data_management" / "data_info_fixture.yaml"))


# write the test and make the assert function proper
# it is taking from the original code


def test_clean_columns(data_info, data):
    data_clean = clean_columns(data_info, data)
    assert not set(data_info["columns_to_drop"]).intersection(set(data_clean.columns))


# _win_col:
# whether wins column exists and if it only includes 0 and 1 and NA for future games

# _transform_date: check whether format is datetime

# _produce_model_data
# check that data neq df from before
# and that there are no nans before date and only nans after

# _data_split: Check that dimensions of dfs align (sum of rows equal to total rows)

# clean_data: check that output is list of 4 entries and that dimensions fit
