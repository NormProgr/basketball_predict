"""Function(s) for cleaning the data set(s)."""

import numpy as np
import pandas as pd


def clean_columns(data_info, df):
    """Drop and rename columns.

    Args:
        data_info (yaml): Contains a configuration of column names.
        df (pandas.DataFrame): Raw data given from the parser.

    Returns:
        df (pandas.DataFrame): DataFrame has dropped unnecessary data and renamed.

    """
    df = df.drop(columns=data_info["columns_to_drop"])
    df = df.rename(columns=data_info["column_rename"])
    return df


def _win_col(df):
    """Produce new column.

    Args:
        df (pandas.DataFrame): Data manipulated by previous functions.

    Returns:
        df (pandas.DataFrame): DataFrame has now a dummy variable column indicating
            wins and losses.

    """
    df["homewin"] = np.where(
        df[["pts_home", "pts_visitor"]].isna().any(axis=1),
        np.nan,
        np.where(df["pts_home"] > df["pts_visitor"], 1, 0),
    )
    return df


def _transform_date(df):
    """Change to more readable datetime.

    Args:
        df (pandas.DataFrame): Data manipulated by previous functions.

    Returns:
        df (pandas.DataFrame): DataFrame has now changed datetime display.

    """
    df["date"] = pd.to_datetime(df["date"])
    return df


def _produce_model_data(data):
    """Change to analysis dataset with cutoff date 2023-02-15.

    Args:
        data (pandas.DataFrame): Data manipulated by previous functions.

    Returns:
        data (pandas.DataFrame): DataFrame has now NaN values from cutoff point.

    """
    data.loc[data["date"] >= "2023-02-16", "pts_home"] = np.nan
    data.loc[data["date"] >= "2023-02-16", "pts_visitor"] = np.nan
    data.loc[data["date"] >= "2023-02-16", "homewin"] = np.nan
    return data


def _data_split(df):
    """Split the DataFrame into two parts.

    Args:
        df (pandas.DataFrame): Data manipulated by previous functions.

    Returns:
        list:
            df_past (pandas.DataFrame): DataFrame that includes all data including the
                scraping data.
            df_future(pandas.DataFrame): DataFrame that includes all data after the
                scraping data.

    """
    df_past = df[df["pts_home"].notna()]
    df_future = df[df["pts_home"].isna()]
    return df_past, df_future


def _dummy_teams(data_info, df):
    """Create dummy variables for team names.

    Args:
        data_info (yaml): Contains a configuration of column names.
        df (pandas.DataFrame): Data frame with team name columns.


    Return:
        new_df (pandas.DataFrame): df with 2 dummy variables per team (home/visitor).
            We do NOT remove the first dummy, so we have perfect multicollinearity.

    """
    new_df = pd.get_dummies(df, columns=data_info["dummy_columns"], drop_first=False)
    new_df["home"] = df["home"]
    new_df["visitor"] = df["visitor"]

    return new_df


def clean_data(data_info, data):
    """Produce 4 DataFrames for analysis.

    Args:
        data_info (yaml): Contains a configuration of column names.
        data (pandas.DataFrame): Raw data given from the parser.

    Returns:
        list:
            _data_split(df) (list): List that contains two DataFrames with data before
                and after the scraping date.
            _data_split(_produce_model_data(df)) (list): List that contains two
                DataFrames with data before and after the cutoff date.

    """
    df = _transform_date(clean_columns(data_info, data))
    df = _dummy_teams(data_info, _win_col(df))
    return _data_split(df) + _data_split(_produce_model_data(df))
