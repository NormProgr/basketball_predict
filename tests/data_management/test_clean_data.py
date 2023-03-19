import pandas as pd
import pytest
import yaml
from bask.config import TEST_DIR
from bask.data_management.clean_data import (
    _dummy_teams,
    _produce_model_data,
    _transform_date,
    _win_col,
    clean_columns,
    clean_data,
)


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
        data (pandas.DataFrame): Data for testing from fixture.

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
        data (pandas.DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises an Error if a necessary column to work with is not created.

    """
    data_win_col = _win_col(clean_columns(data_info, data))
    assert "homewin" in data_win_col.columns, "Error: Column not created."


def test_win_col_val(data_info, data):
    """Test a function whether it produces invalid outcomes.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas.DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises an error if "home_wins" has values that are not 0 or 1 when
            there are points and if there are non-NA entries when there are no points
            yet.

    """
    df = _win_col(clean_columns(data_info, data))
    assert all(elem in [0, 1] for elem in df[~df["homewin"].isna()]["homewin"]) & all(
        df[df["pts_home"].isna()]["homewin"].isna(),
    ), "Error: Invalid value in homewin col for past games."


def test_transform_date(data_info, data):
    """Test if all entries in date column have datetime format.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas.DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises error if there is an entry that cannot be converted to datetime
            format.

    """
    df = _transform_date(clean_columns(data_info, data))
    assert (
        pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce").notnull().all()
    ), "Error: Wrong date format, cannot be converted to datetime."


def test_produce_model_data(data_info, data):
    """Test if all point entries before 16th feb are not NA and all afterwards are NA.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas.DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises an error if there is a NA entry before the cutoff date for model
            data. If the first test passes, raises an error if there is a non-NA entry
            after that date.

    """
    processed_data = _transform_date(_win_col(clean_columns(data_info, data)))
    processed_data = _produce_model_data(processed_data)
    assert (
        processed_data.loc[
            processed_data["date"] < "2023-02-16",
            ["pts_home", "pts_visitor", "homewin"],
        ]
        .isna()
        .sum()
        .sum()
        == 0
    ), "Error: There is a NA in the dataset that should not be there."
    assert (
        processed_data.loc[
            processed_data["date"] >= "2023-02-16",
            ["pts_home", "pts_visitor", "homewin"],
        ]
        .isna()
        .all()
        .all()
    ), "Error: There is a non-NA entry in the dataset that should not be there."


def test_data_split(data):
    """Test if columns for past and future games match.

    Args:
        data (pandas.DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises error if the column labels of the two output data frames don't
        match. If they match, raises an error if the sum of lengths of the output data
        frames is not equal to the number of rows in data.

    """
    data_past = data[data["pts1"].notna()]
    data_future = data[data["pts2"].isna()]
    assert all(
        data_past.columns == data_future.columns,
    ), "Error: Labels of data frame columns are not equal."
    assert len(data_past) + len(data_future) == len(
        data,
    ), "Error: Not all original data entries included in new sets."


def test_dummy_teams(data_info, data):
    """Test if created dummy columns have valid values.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas.DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises error if other values than 0 and 1 are included in dummy
        columns. If it passes, raises an error if too many or too few dummies are
        created.

    """
    data = clean_columns(data_info, data)
    df = _dummy_teams(data_info, data)
    home_col = [col for col in df if col.startswith("home_")]
    visitor_col = [col for col in df if col.startswith("visitor_")]
    assert (
        df[home_col + visitor_col].isin([0, 1]).all().all()
    ), "Error: Not allowed number in dummy column."
    assert (
        len(data["home"].unique()) == len(data["visitor"].unique()) == len(home_col)
    ), "Error: Too many or too few dummy variables."


def test_clean_data(data_info, data):
    """Check that output is list of 4 entries and that dimensions fit.

    Args:
        data_info (yaml): Configuration of column names from fixture.
        data (pandas.DataFrame): Data for testing from fixture.

    Raises:
        Assert: Raises error if the function does not produce a list with 4 entries
            necessary to produce the analysis.

    """
    assert (
        len(clean_data(data_info, data)) == 4
    ), "Error: The list of data frames does not have 4 entries."
