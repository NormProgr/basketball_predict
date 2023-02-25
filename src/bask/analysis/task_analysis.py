"""Tasks running the core analyses."""
import pandas as pd
import pytask

# from bask.analysis.model import naive_model only called in pred_naive
from bask.analysis.predict import pred_naive
from bask.config import BLD, SRC
from bask.preparation.parser import scrapedate


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
@pytask.mark.produces(SRC / "data" / f"concatenated_data_{scrapedate()}.csv")
def task_produce_data(depends_on, produces):
    data_model = pd.read_pickle(depends_on["data_model"])
    data_model_pred = pd.read_pickle(depends_on["data_model_pred"])
    pd.read_pickle(depends_on["data_benchmark"])
    pd.read_pickle(depends_on["data_benchmark_pred"])
    predicted_data = pred_naive(data_model_pred=data_model_pred, data_model=data_model)
    predicted_data.to_csv(produces)
