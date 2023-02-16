"""Function(s) for cleaning the data set(s)."""
import numpy as np
import pandas as pd
import yaml


def clean_columns():
    """Remember that the name has to be flexible."""
    with open("./src/bask/data_management/data_info.yaml") as file:
        data_info = yaml.safe_load(file)
    df = pd.read_pickle("./src/bask/data/data_2023-02-16.pkl")
    df.drop(columns=data_info["columns_to_drop"], inplace=True)
    df.rename(columns=data_info["column_rename"], inplace=True)
    return df


def win_col(df):
    df["home_wins"] = np.where(
        df[["pts_home", "pts_visitor"]].isna().any(axis=1),
        np.nan,
        np.where(df["pts_home"] > df["pts_visitor"], 1, 0),
    )
    return df


def transform_date(df):
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def clean_data():
    df = transform_date(clean_columns())
    df = win_col(df)
    return df


df = clean_data()
