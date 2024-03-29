"""Evaluate the regression model."""
import pandas as pd
import statsmodels.api as sm

from bask.analysis.model import model
from bask.analysis.predict import prediction


def concatenate_dfs(data_model, data_model_pred, data_benchmark, data_benchmark_pred):
    """Concatenate the given DataFrames into a single DataFrame.

    Args:
        data_model (pandas DataFrame): Input dataset that contains the split in
            training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not
            contain any data for points and wins of basketball games.
        data_benchmark (pandas.DataFrame): Current scrape DataFrame that contains more
            data than the data DataFrame.
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
        data_model (pandas DataFrame): Input dataset that contains the split in
            training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not
            contain any data for points and wins of basketball games.
        data_benchmark (pandas.DataFrame): Current scrape DataFrame that contains more
            data than the data DataFrame.

    Returns:
        hpercent (float): Is an evaluation score between 0/1 to show the prediction
            accuracy.

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
        data_model (pandas.DataFrame): Input dataset that contains the split in
            training and test.
        data_model_pred (pandas.DataFrame): DataFrame for prediction  that does not
            contain any data for points and wins of basketball games.
        data_benchmark (pandas.DataFrame): Current scrape DataFrame that contains more
            data than the data DataFrame.

    Returns:
        df (pandas.DataFrame): A DataFrame containing two columns with accuracy measure
            results.

    """
    names = ["fit_score", "pred_accuracy_benchmark"]
    scores = [
        model(data_model)[1],
        pred_accuracy(data_model, data_model_pred, data_benchmark),
    ]
    data = {"score_type": names, "score": scores}
    df = pd.DataFrame(data)
    return df


def naive_inference(data_benchmark):
    """Perform logistic regression on the scores of each team.

    Args:
        data_benchmark (pandas.DataFrame): Current scrape DataFrame that contains more
            data than the data DataFrame.

    Returns:
        statsmodels.iolib.summary.Summary: A summary of the logistic regression model.

    """
    team_names = {
        col.split("_")[1]
        for col in data_benchmark.columns
        if "visitor_" in col or "home_" in col
    }
    team_scores = {team_name: 0 for team_name in team_names}
    for team_name in team_names:
        team_scores[team_name] = (
            data_benchmark[f"home_{team_name}"] + data_benchmark[f"visitor_{team_name}"]
        )
    X = pd.DataFrame.from_dict(team_scores)
    y = data_benchmark["homewin"]
    result = sm.Logit(y, X).fit()
    return result
