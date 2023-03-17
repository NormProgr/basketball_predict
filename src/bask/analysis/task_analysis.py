"""Tasks running the core analyses."""
import pandas as pd
import pytask

from bask.analysis.evaluation import concatenate_dfs, naive_inference, score_df
from bask.analysis.predict import df_pred_results
from bask.config import BLD, SRC

names = ["concatenated_pred", "prediction_scores", "team_result_pred"]


@pytask.mark.depends_on(
    {
        "eval": ["evaluation.py"],
        "data_benchmark": BLD / "python" / "data" / "data_benchmark.pkl",
    },
)
@pytask.mark.task
@pytask.mark.produces(BLD / "python" / "predictions" / "inference_model.pkl")
def task_produce_inf(depends_on, produces):
    """Produce the inference table."""
    data_benchmark = pd.read_pickle(depends_on["data_benchmark"])
    result = naive_inference(data_benchmark)
    result.save(produces)


for name in names:

    @pytask.mark.depends_on(
        {
            "eval": ["evaluation.py"],
            "pred": ["predict.py"],
            "data_model": BLD / "python" / "data" / "data_model.pkl",
            "data_model_pred": BLD / "python" / "data" / "data_model_pred.pkl",
            "data_benchmark": BLD / "python" / "data" / "data_benchmark.pkl",
            "data_benchmark_pred": BLD / "python" / "data" / "data_benchmark_pred.pkl",
            "conferences": SRC / "data" / "conferences.csv",
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "predictions" / f"{name}.pkl")
    def task_produce_results(depends_on, produces, name=name):
        """Produce logit model prediction data sets and scores."""
        data_model = pd.read_pickle(depends_on["data_model"])
        data_model_pred = pd.read_pickle(depends_on["data_model_pred"])
        data_benchmark = pd.read_pickle(depends_on["data_benchmark"])
        data_benchmark_pred = pd.read_pickle(depends_on["data_benchmark_pred"])
        conferences = pd.read_csv(depends_on["conferences"])
        if name == "concatenated_pred":
            result = concatenate_dfs(
                data_model,
                data_model_pred,
                data_benchmark,
                data_benchmark_pred,
            )
        elif name == "prediction_scores":
            result = score_df(data_model, data_model_pred, data_benchmark)
        elif name == "team_result_pred":
            result = df_pred_results(data_model, data_model_pred, conferences)
        result.to_pickle(produces)
