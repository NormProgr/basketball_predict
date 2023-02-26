"""Functions for predicting outcomes based on the estimated model."""
import pandas as pd

from bask.analysis.model import naive_model


def _pred_cols(data_model_pred):
    home_col = [col for col in data_model_pred if col.startswith("home_")]
    visitor_col = [col for col in data_model_pred if col.startswith("visitor_")]
    predictors = home_col + visitor_col
    return predictors


def pred_naive(data_model_pred, data_model):
    df = data_model_pred[_pred_cols(data_model_pred)]
    """Predict new data from 16th february basketball games outcomes."""
    fit = naive_model(data_model)[0]
    pred_16_02 = fit.predict(df)
    pred_proba_16_02 = fit.predict_proba(df)
    data_model_pred["homewin_pred"] = pred_16_02
    data_model_pred["homewin_pred_prob"] = pred_proba_16_02[:, 1]
    return data_model_pred


# possible stuff:
# Prob that team wins
# Prob that home wins for two fixed teams
# Dann pred fur playoffs


# Erstmal data frame umstellen nach teams
conferences = pd.read_csv("src/bask/data/conferences.csv")
data_model = pd.read_pickle("bld/python/data/data_model.pkl")
data_model_pred = pd.read_pickle("bld/python/data/data_model_pred.pkl")


def team_win_pred(data_pred=data_model_pred, data=data_model):
    """Predict total number of wins per team."""
    data_pred = pred_naive(data_pred, data)
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


# def conferences():


def _team_win_prob_home(data_pred, data):
    """Predict win probability for home games.

    data_pred is already predicted data! Good to have test if column homewin_pred is
    empty

    """
    win_prob_home = data_pred.groupby("home")["homewin_pred_prob"].mean()
    return win_prob_home


def _team_win_prob_vis(data_pred, data):
    """Predict win probability for visitor games.

    data_pred is already predicted data!

    """
    win_prob_vis = 1 - data_pred.groupby("visitor")["homewin_pred_prob"].mean()
    return win_prob_vis


def team_win_prob(data_pred=data_model_pred, data=data_model):
    """Predict winning probability for each team."""
    data_pred = pred_naive(data_pred, data)
    win_prob_home = _team_win_prob_home(data_pred, data)
    win_prob_vis = _team_win_prob_vis(data_pred, data)
    win_prob = (
        win_prob_home * data_pred.groupby("home").size()
        + win_prob_vis * data_pred.groupby("visitor").size()
    )
    win_prob = win_prob / (
        data_pred.groupby("home").size() + data_pred.groupby("visitor").size()
    )
    return win_prob
