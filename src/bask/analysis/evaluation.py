"""Evaluate the regression model."""
#####benchmark
import pandas as pd

from bask.analysis.model import model
from bask.analysis.predict import prediction


def concatenate_dfs(data_model, data_model_pred, data_benchmark, data_benchmark_pred):
    """Concatenate the given DataFrames into a single DataFrame.

    Args:
        data_model (pandas DataFrame): Input dataset that contains the split in training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not contain any data for points and wins of basketball games.
        data_benchmark (pandas.DataFrame): Current scrape DataFrame that contains more data than the data DataFrame.
        data_benchmark_pred (pandas.DataFrame): Remaining basketball games DataFrame.

    Returns:
        df_mod (pandas.DataFrame): A concatenated DataFrame containing all input data.

    """
    data_model_pred = prediction(data_model, data_model_pred)
    df_mod = pd.concat([data_model, data_model_pred])
    df_bm = pd.concat([data_benchmark, data_benchmark_pred])
    df_mod[["pts_visitor", "pts_home", "homewin"]] = df_bm[
        ["pts_visitor", "pts_home", "homewin"]
    ].values
    return df_mod


def pred_accuracy(data_model, data_model_pred, data_benchmark):
    """Calculate the score to evaluate prediction precision.

    Args:
        data_model (pandas DataFrame): Input dataset that contains the split in training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not contain any data for points and wins of basketball games.
        data_benchmark (pandas.DataFrame): Current scrape DataFrame that contains more data than the data DataFrame.

    Returns:
        hpercent (float): Is an evaluation score between 0/1 to show the prediction accuracy.

    """
    data_pred = prediction(data_model, data_model_pred)
    latest_date_bm = data_benchmark["date"].max()
    pred_subset = data_pred.loc[data_pred["date"] <= latest_date_bm]
    homewin_pred_subset = pred_subset["homewin_pred"]
    homewin_real_subset = data_benchmark.loc[
        data_benchmark["date"] > "2023-02-15",
        "homewin",
    ]

    hpercent = (
        homewin_real_subset.reset_index(drop=True)
        == homewin_pred_subset.reset_index(drop=True)
    ).mean()
    return hpercent


def score_df(data_model, data_model_pred, data_benchmark):
    """Put the accuracy measures into one DataFrame.

    Args:
        data_model (pandas.DataFrame): Input dataset that contains the split in training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not contain any data for points and wins of basketball games.
        data_benchmark (pandas.DataFrame): Current scrape DataFrame that contains more data than the data DataFrame.

    Returns:
        df (pandas.DataFrame): A DataFrame containing two columns with accuracy measure results.

    """
    names = ["fit_score", "pred_accuracy_benchmark"]
    scores = [
        model(data_model)[1],
        pred_accuracy(data_model, data_model_pred, data_benchmark),
    ]
    data = {"score_type": names, "score": scores}
    df = pd.DataFrame(data)
    return df


import pandas as pd
import statsmodels.api as sm

data = pd.read_csv("bld/python/data/data_benchmark.csv")
team_ids = data[["home", "visitor"]].stack().unique()
common_ids = pd.Series(range(len(team_ids)), index=team_ids)
data["Team1ID"] = data["home"].map(common_ids)
data["Team2ID"] = data["visitor"].map(common_ids)


X = data["Team1ID"]
y = data["homewin"]
result = sm.Logit(y, X).fit()
result.summary()


def inference(data=data):
    X = data["Team2ID"]
    y = data["homewin"]
    result = sm.Logit(y, X).fit()
    return result.summary()
