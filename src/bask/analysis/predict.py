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


def team_df(data_model_pred, data_model, conferences):
    data_model_pred = pred_naive(data_model_pred, data_model)
    df = conferences
    df["past_wins"] = 0
    for name in df["team_name"]:
        for game in range(len(data_model)):
            if (
                data_model.loc[game, f"home_{name}"] == 1
            ):  # & data_model.loc[game, "homewin"] == 1:
                df.loc[name, "past_wins"] = df.loc[name, "past_wins"] + 1
    return df


# def conferences():
