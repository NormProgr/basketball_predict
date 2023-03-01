"""Tests for the prediction model."""

import pandas as pd
import pytest
from bask.analysis.predict import (
    _pred_cols,
    _team_win_prob_home,
    _team_win_prob_vis,
    df_pred_results,
    playoff_pred,
    prediction,
    team_win_pred,
    team_win_prob,
)
from bask.config import TEST_DIR


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture.csv")


@pytest.fixture()
def data_pred():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture_pred.csv")


@pytest.fixture()
def data_model():
    return pd.read_pickle("bld/python/data/data_model.pkl")


@pytest.fixture()
def data_model_pred():
    return pd.read_pickle("bld/python/data/data_model_pred.pkl")


@pytest.fixture()
def conferences():
    return pd.read_csv("src/bask/data/conferences.csv")


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


def test_prediction(data, data_pred):
    """Test if the produced columns have the correct data types.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.


    Raises:
        Assert: Raises an error if homewin_pred and homewin_pred_prob have the wrong datatype.

    """
    df = prediction(data, data_pred)
    assert all(
        df["homewin_pred"].isin([0, 1]),
    ), "Error: homewin_pred column contains values other than 0 or 1"
    assert all(
        (df["homewin_pred_prob"] >= 0) & (df["homewin_pred_prob"] <= 1),
    ), "Error: homewin_pred_prob column contains values outside the range [0, 1]"


def test_team_win_prob_home(data, data_pred):
    """Test that homewin_pred column has no NAs and that the probabilities are valid.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.

    Raises:
        Assert: Raises an error if there are NAs in the homewin_pred column.
        Assert: Raises an error if not all teams are considered.
        Assert: Raises an error if there are invalid probability numbers.

    """
    data_pred = prediction(data, data_pred)
    prob = _team_win_prob_home(data_pred)
    assert (
        not data_pred["homewin_pred"].isna().any()
    ), "Error: There are NAs in the homewin_pred column."
    assert len(prob) == len(
        data_pred["home"].unique(),
    ), "Error: Not all teams considered."
    assert (prob >= 0).all() and (
        prob <= 1
    ).all(), "Error: Invalid probability numbers."


def test_team_win_prob_vis(data, data_pred):
    """Test that homewin_pred column has no NAs and that the probabilities are valid.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.

    Raises:
        Assert: Raises an error if there are NAs in the homewin_pred column.
        Assert: Raises an error if not all teams are considered.
        Assert: Raises an error if there are invalid probability numbers.

    """
    data_pred = prediction(data, data_pred)
    prob = _team_win_prob_vis(data_pred)
    assert not data_pred["homewin_pred"].isna().any(), "Error"
    assert len(prob) == len(
        data_pred["visitor"].unique(),
    ), "Error: Not all teams considered."
    assert (prob >= 0).all() and (
        prob <= 1
    ).all(), "Error: Invalid probability numbers."


def test_team_win_prob(data, data_pred):
    """Test if all teams are considered and the probability numbers are valid.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.

    Raises:
        Assert: Raises an error when not all teams are considered.
        Assert: Raises an error if there are invalid probability numbers.

    """
    win_prob = team_win_prob(data, data_pred)
    assert len(win_prob) == len(
        pd.unique(data_pred[["home", "visitor"]].values.ravel()),
    ), "Error: Not all teams considered."
    assert (win_prob >= 0).all() and (
        win_prob <= 1
    ).all(), "Error: Invalid probability numbers."


def test_team_win_pred(data, data_pred):
    """Test if win entries have right format and if all teams are considered.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.
        data_pred (pandas DataFrame): Small test DataFrame that does not contain any data for points and wins of basketball games.

    Raises:
        Assert: Raises an error if some win entries are not reasonable integers.
        Assert: Raises an error if there are too many or too few teams in predicted win overview.

    """
    wins = team_win_pred(data, data_pred)
    teams = set(data["home"]).union(set(data_pred["home"]))
    # keep this assert wins.values.isdigit() and 0 <= int(x) <= 90, "Error: Invalid win entries."
    assert len(wins) == len(teams), "Error: Not right amount of teams considered."


def test_playoff_pred(data_model, data_model_pred, conferences):
    """Test if win entries have right format and if all teams are considered.

    Args:
        data_model (pandas.DataFrame): Input dataset that contains the split in training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction that does not contain any data for points and wins of basketball games.
        conferences (pandas.DataFrame): DataFrame that contains information to team and conference membership.

    Raises:
        Assert: Raises an error if the wrong number of teams participating the playoffs.

    ------------------
    Note: This must be tested with the real data because it is key to have the correct number of playoff teams.

    """
    pred = playoff_pred(data_model, data_model_pred, conferences)
    assert len(pred) == 16, "Error: Wrong team number in playoffs."


def test_df_pred_results(data_model, data_model_pred, conferences):
    """Test if all model results are concetanated.

    Args:
        data_model (pandas.DataFrame): Input dataset that contains the split in training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction that does not contain any data for points and wins of basketball games.
        conferences (pandas.DataFrame): DataFrame that contains information to team and conference membership.


    Raises:
        Assert: Raises an error if the function produces not the right playoff teams.

    ------------------
    Note: This is tested with the real data to see if the concetanation of results works.

    """
    df = playoff_pred(data_model, data_model_pred, conferences)
    pred = df_pred_results(data_model, data_model_pred, conferences)
    pred = pred.loc[pred["pred_in_playoffs"].__eq__(True)]
    df_str = df["team_name"]
    pred = pred["team_name"]
    pred = sorted(pred, key=str.lower)
    df_str = sorted(df_str, key=str.lower)
    true = pred == df_str
    assert true is True, "Error: Incorrect top 8 teams are produced by the function."
