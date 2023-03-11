"""Functions plotting results."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import metrics


def confusion_matrix(concat_pred, data_benchmark):
    """Compute the confusion matrix for a given set of predictions and benchmark data.

    Args:
        concat_pred (pandas.DataFrame): A DataFrame containing concatenated predictions for basketball games.
        data_benchmark (pandas.DataFrame): A DataFrame containing benchmark data for basketball games.

    Returns:
        cm (array): A 2D array representing the confusion matrix of the predictions.

    """
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
    """Create a heatmap visualization of a confusion matrix.

    Args:
    Args:
        concat_pred (pandas.DataFrame): A DataFrame containing concatenated predictions for basketball games.
        data_benchmark (pandas.DataFrame): A DataFrame containing benchmark data for basketball games.
        score (float): The benchmark accuracy score for the predictions.

    Returns:
        plt (matplotlib.pyplot): A heatmap visualization of the confusion matrix.

    """
    cm = confusion_matrix(concat_pred, data_benchmark)
    plt.figure(figsize=(9, 9))
    sns.heatmap(cm, annot=True, fmt=".3f", linewidths=0.5, square=True, cmap="Blues_r")
    plt.ylabel("Actual values")
    plt.xlabel("Predicted values")
    title = f"Benchmark Accuracy Score: {round(score.iloc[0], 4)}"
    plt.title(title, size=15)
    return plt


def plot_roc_curve(data_benchmark, concat_pred):
    """Create a ROC curve visualization.

    Args:
        concat_pred (pandas.DataFrame): A DataFrame containing concatenated predictions for basketball games.
        data_benchmark (pandas.DataFrame): A DataFrame containing benchmark data for basketball games.

    Returns:
        plt (matplotlib.pyplot): A ROC (receiver operating characteristic) curve visualization

    """
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
    return plt


def generate_prediction_table(res_pred, playoff=False):
    """Generate a summarized prediction table based on the results of a basketball game
    prediction model.

    Args:
        res_pred (pandas.DataFrame): A DataFrame containing the prediction results for each team.
        playoff (bool, optional): A flag indicating whether to include only teams predicted to be in the playoffs. Defaults to False.

    Returns:
        final_df (pandas.DataFrame): A DataFrame containing the predicted win probability, total wins, and playoff status for each team in the Eastern and Western conferences.

    """
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
    """Plot a logistic regression of the home team winning probability against the
    points scored by the visiting team.

    Args:
        concat_pred (pandas.DataFrame): A DataFrame containing predictions for basketball games.

    Returns:
        plt (matplotlib.pyplot): A scatter plot of the home team winning probability against the points scored by the visiting team.

    """
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
    plt.show()
    return plt


def naive_inf_table(inferencemodel):
    """Generate a summary table for the logit model.

    Args:
        inferencemodel (pandas.DataFrame): Fit of the logistic regression.

    Returns:
        summary_table (pandas.DataFrame): A summary table containing key statistics about the model.

    """
    return inferencemodel.summary()
