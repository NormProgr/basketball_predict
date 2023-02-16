"""Function(s) for cleaning the data set(s)."""
import numpy as np
import pandas as pd


def clean_columns(data_info):
    """Remember that the name has to be flexible.

    If we decide not to have flexible names, add data to management file instead of here

    """
    df = pd.read_pickle("./src/bask/data/data_2023-02-16.pkl")
    df.drop(columns=data_info["columns_to_drop"], inplace=True)
    df.rename(columns=data_info["column_rename"], inplace=True)
    return df


def _win_col(df):
    df["home_wins"] = np.where(
        df[["pts_home", "pts_visitor"]].isna().any(axis=1),
        np.nan,
        np.where(df["pts_home"] > df["pts_visitor"], 1, 0),
    )
    return df


def _transform_date(df):
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def _data_split(df):
    df_past = df[df["pts_home"].notna()]
    df_future = df[df["pts_home"].isna()]
    return df_past, df_future


def clean_data(data_info):
    df = _transform_date(clean_columns(data_info))
    df = _win_col(df)
    return _data_split(df)
