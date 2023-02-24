"""Functions for fitting the regression model."""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, KFold, train_test_split

data_model = pd.read_pickle("bld/python/data/data_model.pkl")


def split(data=data_model):
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
    # das hier behalten train_data = pd.concat([X_train, y_train], axis=1)
    # das auch test_data = pd.concat([X_test, y_test], axis=1)
    return X_train, y_train, X_test, y_test  # train_data, test_data


blub = split()


def naive_model(data=split(data_model)):
    X_train = data[0]
    y_train = data[1]
    X_test = data[2]
    y_test = data[3]
    logisticRegr = LogisticRegression()
    logisticRegr.fit(X_train, y_train)
    logisticRegr.predict(X_test)
    score = logisticRegr.score(X_test, y_test)
    return print(score)  #  print(y_pred),


naive_model()


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
