"""Functions plotting results."""
import pandas as pd

data = pd.read_csv("bld/python/predictions/prediction_scores.csv")
data_scores = pd.read_csv("bld/python/predictions/concatenated_pred.csv")
data_pred = pd.read_csv("bld/python/predictions/result_prediction.csv")


# heatmap of how well the model performed

# ROC curve to plot the true positive rate against the false positive rate (sensitivity and specifiticity tradeoff)
