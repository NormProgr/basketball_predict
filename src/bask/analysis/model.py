"""Functions for fitting the regression model."""
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


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


def _model_fit(data):
    """Fit the logistic regression on training data.

    Args:
        data (pandas DataFrame): Input dataset that contains the split in training and test.

    Return:
        fit (LogisticRegression): Fitted logit regression model to predict new data.

    """
    X_train, y_train, _, _ = split(data)
    logisticRegr = LogisticRegression()
    fit = logisticRegr.fit(X_train, y_train)
    return fit


def _model_test(data):
    """Test the logistic regression model on test data.

    Args:
        data (pandas DataFrame): Input dataset that contains the split in training and test.

    Returns:
        score (float): The accuracy score of the trained logistic regression model.

    """
    _, _, X_test, y_test = split(data)
    fit = _model_fit(data)
    score = fit.score(X_test, y_test)
    return score


def model(data):
    """Test the logistic regression model on test data.

    Args:
        data (pandas DataFrame): Input dataset that contains the split in training and test.

    Returns:
        Tuple:
            _model_fit(data) (function): Returns a fitted logit regression model to predict new data.
            _model_test(data) (function): Returns accuracy score of the trained logistic regression model.

    """
    return _model_fit(data), _model_test(data)
