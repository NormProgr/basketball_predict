"""Tasks for managing the data."""

from clean_data import *

# combine steps from cleaning


def data_management():
    df = transform_date(clean_data())
    return df


df = data_management()
