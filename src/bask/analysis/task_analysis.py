"""Tasks running the core analyses."""
import pandas as pd
import pytask

# from bask.analysis.model import naive_model only called in pred_naive
from bask.analysis.evaluation import concatenate_dfs, score_df
from bask.config import BLD


@pytask.mark.depends_on(
    {
        "fit": ["model.py"],
        "pred": ["predict.py"],
        "data_model": BLD / "python" / "data" / "data_model.pkl",
        "data_model_pred": BLD / "python" / "data" / "data_model_pred.pkl",
        "data_benchmark": BLD / "python" / "data" / "data_benchmark.pkl",
        "data_benchmark_pred": BLD / "python" / "data" / "data_benchmark_pred.pkl",
    },
)
@pytask.mark.task
@pytask.mark.produces(BLD / "python" / "data" / "concatenated_pred.csv")
def task_produce_data(depends_on, produces):
    data_model = pd.read_pickle(depends_on["data_model"])
    data_model_pred = pd.read_pickle(depends_on["data_model_pred"])
    data_benchmark = pd.read_pickle(depends_on["data_benchmark"])
    data_benchmark_pred = pd.read_pickle(depends_on["data_benchmark_pred"])
    predicted_df = concatenate_dfs(
        data_model,
        data_model_pred,
        data_benchmark,
        data_benchmark_pred,
    )
    predicted_df.to_csv(produces)


@pytask.mark.depends_on(
    {
        "fit": ["model.py"],
        "pred": ["predict.py"],
        "data_model": BLD / "python" / "data" / "data_model.pkl",
        "data_model_pred": BLD / "python" / "data" / "data_model_pred.pkl",
        "data_benchmark": BLD / "python" / "data" / "data_benchmark.pkl",
    },
)
@pytask.mark.task
@pytask.mark.produces(BLD / "python" / "data" / "scores_pred.csv")
def task_produce_data(depends_on, produces):
    data_model = pd.read_pickle(depends_on["data_model"])
    data_model_pred = pd.read_pickle(depends_on["data_model_pred"])
    data_benchmark = pd.read_pickle(depends_on["data_benchmark"])
    scores = score_df(data_model, data_model_pred, data_benchmark)
    scores.to_csv(produces)
