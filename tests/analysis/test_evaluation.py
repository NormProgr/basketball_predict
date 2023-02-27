"""Tests for the model evaluations."""

import pandas as pd
import pytest
from bask.analysis.evaluation import concatenate_dfs
from bask.analysis.predict import pred_naive
from bask.config import TEST_DIR


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture.csv")


@pytest.fixture()
def data_pred():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture_pred.csv")


@pytest.fixture()
def data_benchmark():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture_benchmark.csv")


@pytest.fixture()
def data_benchmark_pred():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture_benchmark_pred.csv")


def test_concatenate_dfs(data, data_pred, data_benchmark, data_benchmark_pred):
    """Test if concatenated data frame has correct dimensions.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.
        data_benchmark (pandas DataFrame): Current scrape DataFrame that contains more data than the data DataFrame.
        data_benchmark_pred(pandas DataFrame): Remaining basketball games DataFrame.

    Raises:
        Assert: Raises an error if the shape of the concatenated DataFrames does not match the expected shape.

    """
    data_pred = pred_naive(data_model=data, data_model_pred=data_pred)
    data_shape = pd.concat([data, data_pred]).shape
    df = concatenate_dfs(
        data_model=data,
        data_model_pred=data_pred,
        data_benchmark=data_benchmark,
        data_benchmark_pred=data_benchmark_pred,
    )
    assert (
        data_shape == df.shape
    ), f"Error: Expected shape {data_shape} but got {df.shape}"
    assert (
        data["homewin"][0 : len(data)] == df["homewin"][0 : len(data)]
    ).all(), "Error: Past results changed by concatenating."

    # ValueError: Can only compare identically-labeled Series objects

    # def test_pred_score(data,data_pred,data_benchmark):
    """Test if concatenated data frame has correct dimensions.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.
        data_benchmark (pandas DataFrame): Current scrape DataFrame that contains more data than the data DataFrame.
        data_benchmark_pred(pandas DataFrame): Remaining basketball games DataFrame.

    Raises:
        Assert: Raises an error if the shape of the concatenated DataFrames does not match the expected shape.

    """
    # assert score_percent > 0


# ValueError: Can only compare identically-labeled Series objects


# def test_score_df(data,data_pred,data_benchmark):
