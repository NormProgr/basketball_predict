"""Tests for the prediction model."""

import pandas as pd
import pytest
from bask.analysis.predict import (
    _pred_cols,
    _team_win_prob_home,
    _team_win_prob_vis,
    pred_naive,
    team_win_prob,
)
from bask.config import TEST_DIR


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture.csv")


@pytest.fixture()
def data_pred():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture_pred.csv")


def test_pred_cols(data):
    """Test the correct type of predictors.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.


    Raises:
        Assert: Raises an error if any of the columns in the predictors DataFrame contains values other than 0 or 1.

    """
    predictors = _pred_cols(data)
    cols_to_remove = ["date", "pts1", "pts2"]
    predictors = [col for col in predictors if col not in cols_to_remove]
    for col in predictors:
        assert all(
            val in [0, 1] for val in data[col]
        ), f"Error: {col} column contains values other than 0 or 1"


def test_pred_naive(data_pred, data):
    """Test if the produced columns have the correct data types.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.


    Raises:
        Assert: Raises an error if homewin_pred and homewin_pred_prob have the wrong datatype.

    """
    df = pred_naive(data_pred, data)
    assert all(
        df["homewin_pred"].isin([0, 1]),
    ), "Error: homewin_pred column contains values other than 0 or 1"
    assert all(
        (df["homewin_pred_prob"] >= 0) & (df["homewin_pred_prob"] <= 1),
    ), "Error: homewin_pred_prob column contains values outside the range [0, 1]"


def test_team_win_prob_home(data_pred, data):
    """Test that homewin_pred column has no NAs and that the probabilities are valid."""
    data_pred = pred_naive(data_pred, data)
    prob = _team_win_prob_home(data_pred)
    assert not data_pred["homewin_pred"].isna().any(), "Error"
    assert len(prob) == len(
        data_pred["home"].unique(),
    ), "Error: Not all teams considered."
    assert (prob >= 0).all() and (
        prob <= 1
    ).all(), "Error: Invalid probability numbers."


def test_team_win_prob_vis(data_pred, data):
    """Test that homewin_pred column has no NAs and that the probabilities are valid."""
    data_pred = pred_naive(data_pred, data)
    prob = _team_win_prob_vis(data_pred)
    assert not data_pred["homewin_pred"].isna().any(), "Error"
    assert len(prob) == len(
        data_pred["visitor"].unique(),
    ), "Error: Not all teams considered."
    assert (prob >= 0).all() and (
        prob <= 1
    ).all(), "Error: Invalid probability numbers."


def test_team_win_prob(data_pred, data):
    win_prob = team_win_prob(data_pred, data)
    assert len(win_prob) == len(
        pd.unique(data_pred[["home", "visitor"]].values.ravel()),
    ), "Error: Not all teams considered."
    assert (win_prob >= 0).all() and (
        win_prob <= 1
    ).all(), "Error: Invalid probability numbers."
