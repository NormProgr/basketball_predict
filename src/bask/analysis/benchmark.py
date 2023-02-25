"""Functions for fitting the regression model."""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

data_model = pd.read_pickle("bld/python/data/data_model.pkl")


def split(data):
    """Split data into test and train data.

    Args:
        data (pandas DataFrame): Dataset that should be split.

    Returns:
        train_data (list):
            X_train (pandas DataFrame): Predictors for the train data.
            y_train (pandas DataFrame): Outcome variable for train data.
        test_data (list):
            X_test (pandas DataFrame): Predictors for the test data.
            y_test (pandas DataFrame): Outcome variable for test data.

    """
    home_col = [col for col in data if col.startswith("home_")]
    visitor_col = [col for col in data if col.startswith("visitor_")]
    cols = home_col + visitor_col
    X = data[cols]
    y = data["homewin"]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        random_state=42,
        test_size=0.3,
        shuffle=True,
    )
    return X_train, y_train, X_test, y_test


def _naive_model_fit(data):
    X_train, y_train, _, _ = split(data)
    logisticRegr = LogisticRegression()
    fit = logisticRegr.fit(X_train, y_train)
    return fit


def _naive_model_test(data):
    _, _, X_test, y_test = split(data)
    fit = _naive_model_fit(data)
    score = fit.score(X_test, y_test)
    return fit, score


def naive_model(data):
    return _naive_model_fit(data), _naive_model_test(data)


# 1 predict the test set


####predict


pred_model = pd.read_pickle("bld/python/data/data_model_pred.pkl")


def _pred_cols(pred_model=pred_model):
    home_col = [col for col in pred_model if col.startswith("home_")]
    visitor_col = [col for col in pred_model if col.startswith("visitor_")]
    predictors = home_col + visitor_col
    return predictors


# data_model_pred.pkl this part has to be predicted then benchmarked with benchmark.pkl


def pred_naive(data_pred=pred_model, data=data_model):
    df = data_pred[_pred_cols(data_pred)]
    """Predict new data from 16th february basketball games outcomes."""
    fit = naive_model(data)[0]
    pred_16_02 = fit.predict(df)
    pred_proba_16_02 = fit.predict_proba(df)
    data_pred["homewin_pred"] = pred_16_02
    data_pred["homewin_pred_prob"] = pred_proba_16_02[:, 1]
    return data_pred


#####benchmark
data_benchmark = pd.read_pickle("bld/python/data/data_benchmark.pkl")


def benchmark_to_16_02(data_benchmark, pred_model, data_model):
    data_pred = pred_naive(pred_model, data_model)
    latest_date_bm = data_benchmark["date"].max()
    pred_subset = data_pred.loc[data_pred["date"] <= latest_date_bm]

    homewin_pred_subset = pred_subset["homewin_pred"]
    homewin_real_subset = data_benchmark.loc[data_benchmark["date"] <= latest_date_bm]
    homewin_real_subset = homewin_real_subset.loc[
        homewin_real_subset["date"] > "2023-02-15",
        "homewin",
    ]

    hpercent = (homewin_real_subset == homewin_pred_subset).mean()
    return hpercent

    # compare from including 16.02 to current date the prediction with benchmark
    # übereinstimmung zwischen den spalten
    # find in column oldest date


def cross_val():
    """Choose the cross-validation subsets.

    Return:
        k_fold ():

    """
    k_fold = KFold(n_splits=10, shuffle=True, random_state=42)
    return k_fold


def model_fit(k_fold, data=split(data_model)):
    param_grid = {"C": [0.1, 1, 10, 100], "penalty": ["l2"]}
    model = LogisticRegression(random_state=42)
    grid = GridSearchCV(model, param_grid, cv=k_fold)
    model_fit = grid.fit(data[0], data[1])
    return model_fit


# Create a logistic regression classifier

# Train the classifier on the training set


# Predict the classes of the test set

# Evaluate the accuracy of the classifier

# see example of other branch
