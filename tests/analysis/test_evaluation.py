"""Tests for the model evaluations."""

import pandas as pd
import pytest
from bask.config import TEST_DIR


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture.csv")


@pytest.fixture()
def data_pred():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture_pred.csv")


@pytest.fixture()
def data_pred():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture_benchmark.csv")


@pytest.fixture()
def data_pred():
    return pd.read_csv(TEST_DIR / "analysis" / "data_fixture_benchmark_pred.csv")
