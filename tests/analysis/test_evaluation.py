"""Tests for the model evaluations."""

import pandas as pd
import pytest
import statsmodels.api as sm
from bask.analysis.evaluation import (
    concatenate_dfs,
    naive_inference,
    pred_accuracy,
    score_df,
)
from bask.analysis.predict import prediction
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
        Assert: Raises an error if the original results do not match the ones after concetenating.

    """
    data_pred = prediction(data_model=data, data_model_pred=data_pred)
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


def test_pred_accuracy(data, data_pred, data_benchmark):
    """Test if concatenated data frame has correct dimensions.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.
        data_benchmark (pandas DataFrame): Current scrape DataFrame that contains more data than the data DataFrame.

    Raises:
        Assert: Raises an error if the score is outside the 0/1 boundaries.

    """
    score_acc = pred_accuracy(data, data_pred, data_benchmark)
    assert 1 >= score_acc >= 0, "Error: Score not between 0 and 1."


def test_score_df(data, data_pred, data_benchmark):
    """Test if the correct length of columns is returned.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.
        data_benchmark (pandas DataFrame): Current scrape DataFrame that contains more data than the data DataFrame.

    Raises:
        Assert: Raises an error if the wrong amount of columns is returned.

    """
    df = score_df(data, data_pred, data_benchmark)
    assert df.shape[1] == 2, f"Error: Returns {len(df.shape[1])}, but expects: {2}."


def test_naive_inference(data_benchmark):
    """Test if the inference function produces correct results and is the correct type.

    Args:
        data_benchmark (pandas DataFrame): Current scrape DataFrame that contains more data than the data DataFrame.

    Raises:
        Assert: Raises an error if the p-values are out of the possible values.
        Assert: Raises an error if summary of the fit is not the correct type.

    """
    result = naive_inference(data_benchmark)
    for pvalue in result.pvalues:
        assert (
            pvalue >= 0 and pvalue <= 1
        ), "Error: p-values are out of the possible space."
    assert isinstance(
        result.summary(),
        sm.iolib.summary.Summary,
    ), "Error: It is not statsmodel  type."
