"""Functions for predicting outcomes based on the estimated model."""
import pandas as pd

from bask.analysis.model import model


def _pred_cols(data_model_pred):
    """Append all predictors into one DataFrame.

    Args:
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not contain any data for points and wins of basketball games.

    Returns:
        predictors (pandas.DataFrame): Appended DataFrame containing all predictors.

    """
    home_col = [col for col in data_model_pred if col.startswith("home_")]
    visitor_col = [col for col in data_model_pred if col.startswith("visitor_")]
    predictors = home_col + visitor_col
    return predictors


def prediction(data_model, data_model_pred):
    """Predict new data from 16th february basketball games outcomes.

    Args:
        data_model (pandas.DataFrame): Input dataset that contains the split in training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not contain any data for points and wins of basketball games.

    Returns:
        data_model_pred (pandas.DataFrame): DataFrame that contains predictors and predicted data.

    """
    df = data_model_pred[_pred_cols(data_model_pred)]
    fit = model(data_model)[0]
    pred_16_02 = fit.predict(df)
    pred_proba_16_02 = fit.predict_proba(df)
    data_model_pred["homewin_pred"] = pred_16_02
    data_model_pred["homewin_pred_prob"] = pred_proba_16_02[:, 1]
    return data_model_pred


def team_win_pred(data, data_pred):
    """Predict total number of wins per team.

    Args:
        data_model (pandas.DataFrame): Input dataset that contains the split in training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction that does not contain any data for points and wins of basketball games.

    Returns:
        wins (pandas.DataFrame): DataFrame that contains the predicted wins per team.

    """
    data_pred = prediction(data, data_pred)
    past_wins = (
        data.groupby("home")["homewin"].sum()
        + data.groupby("visitor").size()
        - data.groupby("visitor")["homewin"].sum()
    )
    pred_wins = (
        data_pred.groupby("home")["homewin_pred"].sum()
        + data_pred.groupby("visitor").size()
        - data_pred.groupby("visitor")["homewin_pred"].sum()
    )
    wins = past_wins + pred_wins
    return wins


def _team_win_prob_home(data_pred):
    """Predict win probability for home games.

    Args:
        data_pred (pandas.DataFrame): DataFrame that includes predicted data.


    Returns:
        win_prob_home (pandas.DataFrame): DataFrame with winning probabilities for the home team.

    """
    if "homewin_pred" not in data_pred.columns:
        raise ValueError("Input for future games should be already predicted data.")
    win_prob_home = data_pred.groupby("home")["homewin_pred_prob"].mean()
    return win_prob_home


def _team_win_prob_vis(data_pred):
    """Predict win probability for visitor games.

    Args:
        data_pred (pandas.DataFrame): DataFrame that includes predicted data.


    Returns:
        win_prob_vis (pandas.DataFrame): DataFrame with winning probabilities for the visiting team.

    """
    if "homewin_pred" not in data_pred.columns:
        raise ValueError("Input for future games should be already predicted data.")
    win_prob_vis = 1 - data_pred.groupby("visitor")["homewin_pred_prob"].mean()
    return win_prob_vis


def team_win_prob(data, data_pred):
    """Predict winning probability for each team playing in home and visiting stadium.

    Args:
        data (pandas.DataFrame): Input dataset that contains the split in training and test.
        data_pred (pandas.DataFrame): DataFrame that includes predicted data.


    Returns:
        win_prob (pandas.DataFrame): DataFrame with winning probabilities for the visiting and home team.

    """
    data_pred = prediction(data, data_pred)
    win_prob_home = _team_win_prob_home(data_pred)
    win_prob_vis = _team_win_prob_vis(data_pred)

    home_scaled = win_prob_home * data_pred.groupby("home").size()
    vis_scaled = win_prob_vis * data_pred.groupby("visitor").size()
    win_prob = (home_scaled).add(vis_scaled, fill_value=0)
    win_prob = win_prob / (
        data_pred.groupby("home")
        .size()
        .add(data_pred.groupby("visitor").size(), fill_value=0)
    )
    return win_prob


def playoff_pred(data, data_pred, conferences):
    """Predict which teams are participating the playoffs.

    Args:
        data_model (pandas.DataFrame): Input dataset that contains the split in training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not contain any data for points and wins of basketball games.
        conferences (pandas.DataFrame): DataFrame that contains information to team and conference membership.


    Returns:
        playoff_teams (pandas.DataFrame): DataFrame with winning probabilities for each team in each conference.

    """
    east_teams = conferences[conferences["conference"] == "East"].copy()
    east_teams["wins"] = (
        team_win_pred(data, data_pred).loc[east_teams["team_name"]].values
    )
    east_teams = east_teams.sort_values("wins", ascending=False)
    west_teams = conferences[conferences["conference"] == "West"].copy()
    west_teams["wins"] = team_win_pred(data, data_pred)[west_teams["team_name"]].values
    west_teams.sort_values("wins", ascending=False, inplace=True)
    playoff_teams = pd.concat([east_teams[0:8], west_teams[0:8].reset_index(drop=True)])
    return playoff_teams


def df_pred_results(data, data_pred, conferences):
    """Concatenate the prediction results.

    Args:
        data_model (pandas.DataFrame): Input dataset that contains the split in training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not contain any data for points and wins of basketball games.
        conferences (pandas.DataFrame): DataFrame that contains information to team and conference membership.


    Returns:
        df (pandas.DataFrame): DataFrame of concatenated winning prediction and the playoff prediction data.

    """
    names = playoff_pred(data, data_pred, conferences)["team_name"]
    df = conferences
    df["pred_total_wins"] = (
        team_win_pred(data, data_pred).loc[conferences["team_name"]].values
    )
    df["pred_win_prob"] = (
        team_win_prob(data, data_pred).loc[conferences["team_name"]].values
    )
    df["pred_in_playoffs"] = df["team_name"].isin(names)
    return df
