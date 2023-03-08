"""Functions plotting results."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import metrics


def confusion_matrix(concat_pred, data_benchmark):
    latest_date_bm = data_benchmark["date"].max()
    concat_pred["date"] = pd.to_datetime(concat_pred["date"])
    cond = (concat_pred["date"] > "2023-02-15") & (
        concat_pred["date"] <= latest_date_bm
    )
    subset = concat_pred.loc[cond]
    pred_subset = subset["homewin_pred"]
    true_val = subset["homewin"]
    cm = metrics.confusion_matrix(pred_subset, true_val)
    return cm


def create_heatmap(concat_pred, data_benchmark, score):
    cm = confusion_matrix(concat_pred, data_benchmark)
    plt.figure(figsize=(9, 9))
    sns.heatmap(cm, annot=True, fmt=".3f", linewidths=0.5, square=True, cmap="Blues_r")
    plt.ylabel("Actual label")
    plt.xlabel("Predicted label")
    all_sample_title = f"Benchmark Accuracy Score: {score}"
    plt.title(all_sample_title, size=15)
    plt.show()


def plot_roc_curve(data_benchmark, concat_pred):
    latest_date_bm = data_benchmark["date"].max()
    concat_pred["date"] = pd.to_datetime(concat_pred["date"])
    cond = (concat_pred["date"] > "2023-02-15") & (
        concat_pred["date"] <= latest_date_bm
    )
    subset = concat_pred.loc[cond]
    subset["homewin_pred"]
    true_val = subset["homewin"]
    y_pred_proba = subset["homewin_pred_prob"]
    fp_r, tp_r, _ = metrics.roc_curve(true_val, y_pred_proba)
    plt.plot(fp_r, tp_r)
    plt.ylabel("True Positive Rate")
    plt.xlabel("False Positive Rate")
    plt.show()


def generate_prediction_table(res_pred, playoff=False):
    res_pred.sort_values(
        ["conference", "pred_win_prob"],
        ascending=[True, False],
        inplace=True,
    )

    eastern = res_pred[res_pred["conference"] == "East"].reset_index(drop=True)
    western = res_pred[res_pred["conference"] == "West"].reset_index(drop=True)
    if playoff:
        eastern = eastern[eastern["pred_in_playoffs"]]  # == True]
        western = western[western["pred_in_playoffs"]]  # == True]

    final_df = pd.concat(
        [
            eastern[
                ["team_name", "pred_win_prob", "pred_total_wins", "pred_in_playoffs"]
            ].reset_index(drop=True),
            western[
                ["team_name", "pred_win_prob", "pred_total_wins", "pred_in_playoffs"]
            ].reset_index(drop=True),
        ],
        axis=1,
        keys=["Eastern Conference", "Western Conference"],
    )
    return final_df


# summary table


def reg_plot(concat_pred):
    data = concat_pred
    x = data["pts_visitor"]
    y = data["homewin_pred"]
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    ax = sns.regplot(x=x, y=y, data=data, logistic=True, ci=None)
    ax.set_xlabel("Points Visitor", fontsize=14)
    ax.set_ylabel("Home Team Winning", fontsize=14)
    plt.title("Home Team Winning Probability vs. Points Visitor", fontsize=16)
    ax.tick_params(labelsize=12)
