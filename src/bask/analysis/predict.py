"""Functions for predicting outcomes based on the estimated model."""
import pandas as pd

from bask.analysis.model import naive_model

pred_model = pd.read_pickle("bld/python/data/data_model_pred.pkl")
# data_model_pred.pkl this part has to be predicted then benchmarked with benchmark.pkl
# data_model.pkl has real data
# data_benchmark.pkl has real data
# data_benchmark_pred.pkl


def _pred_cols(data_model_pred):
    home_col = [col for col in data_model_pred if col.startswith("home_")]
    visitor_col = [col for col in data_model_pred if col.startswith("visitor_")]
    predictors = home_col + visitor_col
    return predictors


# data_model_pred.pkl this part has to be predicted then benchmarked with benchmark.pkl


def pred_naive(data_model_pred, data_model):
    df = data_model_pred[_pred_cols(data_model_pred)]
    """Predict new data from 16th february basketball games outcomes."""
    fit = naive_model(data_model)[0]
    pred_16_02 = fit.predict(df)
    pred_proba_16_02 = fit.predict_proba(df)
    data_model_pred["homewin_pred"] = pred_16_02
    data_model_pred["homewin_pred_prob"] = pred_proba_16_02[:, 1]
    return data_model_pred


# 2 predict the teams that participate in the playoffs by winning possibility (it is just an order)
# But we need to pay attention to conferences!

# - graphic
