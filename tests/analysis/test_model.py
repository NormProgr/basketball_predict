"""Tests for the regression model."""
import numpy as np
import pandas as pd
import pytest
from bask.analysis.model import _model_fit, _model_test, model, split
from bask.config import TEST_DIR


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture.csv")


def test_split(data):
    """Test the correct amount of function outputs.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.

    Raises:
        Assert: Raises an error if the return of the test function is unequal 4 elements.
    """
    assert (
        len(split(data)) == 4
    ), "Error: There is not the right amount of test and training data sets."


def test_model_fit(data):
    """Test if the fitted model produce coefficients.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.

    Raises:
        Assert: Raises an error if there is not even one coefficient in the fitted model.
    """
    used_fit = _model_fit(data)
    assert (
        np.count_nonzero(used_fit.coef_) > 0
    ), "Error: The fit object has zero coefficients"


def test_model_test(data):
    """Test if the score has a meaningful value.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.

    Raises:
        Assert: Raises an error if the score is not between 0 and 1.
    """
    score = _model_test(data)
    assert 0 <= score <= 1, "Error: Score takes on a value not between 0 and 1."


def test_model(data):
    """Test if the function returns two outputs.

    Args:
        data (pandas DataFrame): Small test DataFrame that works essentially like the main DataFrame.

    Raises:
        Assert: Raises an error if the function does not returns two outputs. If there are not two returns, the pytask function fails.
    """
    assert isinstance(model(data), tuple), "Error: Variable is not a tuple."
