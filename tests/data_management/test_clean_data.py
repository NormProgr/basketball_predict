import pandas as pd
import pytest
import yaml
from bask.config import TEST_DIR
from bask.data_management.clean_data import (
    _produce_model_data,
    _transform_date,
    _win_col,
    clean_columns,
    clean_data,
)

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


def test_clean_columns(data_info, data):
    """Test the unnecessary columns are dropped.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises an Error if the dropped column still exists.

    """
    data_clean = clean_columns(data_info, data)
    assert not set(data_info["columns_to_drop"]).intersection(
        set(data_clean.columns),
    ), "Error: Some columns not dropped."


def test_win_col_ex(data_info, data):
    """Test if the column exists.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises an Error if a necessary column to work with is not created.

    """
    data_win_col = _win_col(clean_columns(data_info, data))
    assert "home_wins" in data_win_col.columns, "Error: Column not created."


def test_win_col_val(data_info, data):
    """Test a function whether it produces invalid outcomes.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises an Error if the function produces outcomes in the column home_wins that do not make sense before a certain date.

    """
    df = _win_col(clean_columns(data_info, data))
    assert all(
        elem in [0, 1] for elem in df[~df["home_wins"].isna()]["home_wins"]
    ) & all(
        df[df["pts_home"].isna()]["home_wins"].isna(),
    ), "Error: Invalid value in home_wins col for past games."


def test_transform_date(data_info, data):
    """Test if all entries in date column have datetime format.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises error if there is an entry that cannot be converted to datetime format.

    Maybe do nicer assert in the end!

    """
    df = _transform_date(clean_columns(data_info, data))
    assert (
        pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce").notnull().all()
    ), "Error: Wrong date format"


def test_produce_model_data(data_info, data):
    """Test if all point entries before 16th feb are not NA and all afterwards are NA.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises an error if there is a NA entry before the cutoff date for model data.
            If the first test passes, raises an error if there is a non-NA entry after that date.

    """

    processed_data = _transform_date(_win_col(clean_columns(data_info, data)))
    processed_data = _produce_model_data(processed_data)
    assert (
        processed_data.loc[
            processed_data["date"] < "2023-02-16",
            ["pts_home", "pts_visitor", "home_wins"],
        ]
        .isna()
        .sum()
        .sum()
        == 0
    ), "Error: There is a NA in the dataset that should not be there."
    assert (
        processed_data.loc[
            processed_data["date"] >= "2023-02-16",
            ["pts_home", "pts_visitor", "home_wins"],
        ]
        .isna()
        .all()
        .all()
    ), "Error: There is a non-NA entry in the dataset that should not be there."


def test_data_split(data):
    """Test if columns for past and future games match.

    Args:
        data (pandas DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises an error if the column labels of the two output data frames don't match.
            If they match, raises an error if the sum of lengths of the output data frames is not
            equal to the number of rows in data.

    """
    data_past = data[data["pts1"].notna()]
    data_future = data[data["pts2"].isna()]
    assert all(
        data_past.columns == data_future.columns,
    ), "Error: Labels of data frame columns are not equal."
    assert len(data_past) + len(data_future) == len(
        data,
    ), "Error: Not all original data entries included in new sets."


def test_clean_data(data_info, data):
    """Check that output is list of 4 entries and that dimensions fit.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas DataFrame): Data for testing from fixture.

    Raises:
        Assert: Asserts an error if the function does not produce a list with 4 entries necessary to produce the analysis.

    """
    assert (
        len(clean_data(data_info, data)) == 4
    ), "Error: The list df does not have 4 entries."
