"""Tests for the regression model."""
import numpy as np
import pandas as pd
import pytest
from bask.analysis.model import _naive_model_fit, _naive_model_test, naive_model, split
from bask.config import TEST_DIR


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture.csv")


def test_split(data):
    assert (
        len(split(data)) == 4
    ), "Error: There is not the right amount of test and training data sets."


# RecursionError: maximum recursion depth exceeded while calling a Python object
def test_naive_model_fit(data):
    used_fit = _naive_model_fit(data)
    assert np.count_nonzero(used_fit.coef_) > 0, "The fit object has zero coefficients"


def test_naive_model_test(data):
    # RecursionError: maximum recursion depth exceeded while calling a Python object

    score = _naive_model_test(data)
    assert 0 <= score <= 1, "Error: Score takes a not possible value."


# RecursionError: maximum recursion depth exceeded while calling a Python object
def test_naive_model(data):
    assert isinstance(naive_model(data), tuple), "Error: variable is not a tuple"


# def test__naive_model_test(:)
