"""Evaluate the regression model."""
#####benchmark
import pandas as pd

from bask.analysis.model import naive_model
from bask.analysis.predict import pred_naive


def concatenate_dfs(data_model, data_model_pred, data_benchmark, data_benchmark_pred):
    data_model_pred = pred_naive(data_model_pred, data_model)
    df_mod = pd.concat([data_model, data_model_pred])
    df_bm = pd.concat([data_benchmark, data_benchmark_pred])
    df_mod[["pts_visitor", "pts_home", "homewin"]] = df_bm[
        ["pts_visitor", "pts_home", "homewin"]
    ].values
    return df_mod


def pred_score(data_benchmark, pred_model, data_model):
    data_pred = pred_naive(pred_model, data_model)
    latest_date_bm = data_benchmark["date"].max()
    pred_subset = data_pred.loc[data_pred["date"] <= latest_date_bm]

    homewin_pred_subset = pred_subset["homewin_pred"]
    homewin_real_subset = data_benchmark.loc[
        data_benchmark["date"] > "2023-02-15",
        "homewin",
    ]

    hpercent = (homewin_real_subset == homewin_pred_subset).mean()
    return hpercent


def score_df(data_model, data_model_pred, data_benchmark):
    names = ["fit_score", "benchmark_score"]
    scores = [
        naive_model(data_model)[1],
        pred_score(data_benchmark, data_model_pred, data_model),
    ]
    data = {"score_type": names, "score": scores}
    df = pd.DataFrame(data)
    return df
