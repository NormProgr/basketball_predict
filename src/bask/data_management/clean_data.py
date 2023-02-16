"""Function(s) for cleaning the data set(s)."""
import numpy as np
import pandas as pd
import yaml


def clean_data():
    """Remember that the name has to be flexible."""
    with open("./src/bask/data_management/data_info.yaml") as file:
        data_info = yaml.safe_load(file)
    df = pd.read_pickle("./src/bask/data/data_2023-02-16.pkl")
    df.drop(columns=data_info["columns_to_drop"], inplace=True)
    df.rename(columns=data_info["column_rename"], inplace=True)
    df["home_wins"] = np.where(df["pts_home"] > df["pts_visitor"], 1, 0)

    return df


clean_data()

# change dateformat
# add winner
