"""Tasks running the results formatting (tables, figures)."""

import matplotlib.pyplot as plt
import pandas as pd
import pytask
from statsmodels.iolib.smpickle import load_pickle

from bask.config import BLD
from bask.final.plot import (
    create_heatmap,
    generate_prediction_table,
    naive_inf_table,
    plot_roc_curve,
    reg_plot,
)

tables = ["table", "table_playoffs"]

for i in tables:

    @pytask.mark.depends_on(
        {
            "plot": ["plot.py"],
            "result_pred": BLD / "python" / "predictions" / "team_result_pred.pkl",
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "tables" / f"basketball_results_{i}.tex")
    def task_create_results_table_python(depends_on, produces, i=i):
        """Store a table in LaTeX format with the estimation results (Python
        version).
        """
        res_pred = pd.read_pickle(depends_on["result_pred"])
        if i == "table":
            model = generate_prediction_table(res_pred=res_pred, playoff=False)
        elif i == "table_playoffs":
            model = generate_prediction_table(res_pred=res_pred, playoff=True)
        table = model.style.hide(axis="index").to_latex()
        with open(produces, "w") as f:
            f.write(table)


@pytask.mark.depends_on(
    {
        "plot": ["plot.py"],
        "inference_model": BLD / "python" / "predictions" / "inference_model.pkl",
    },
)
@pytask.mark.task
@pytask.mark.produces(BLD / "python" / "tables" / "inference_model.tex")
def task_produce_inf(depends_on, produces):
    """Produce an inference table of the basketball data in LaTeX format."""
    inference_model = load_pickle(depends_on["inference_model"])
    model = naive_inf_table(inference_model)
    with open(produces, "w") as fh:
        fh.write(model.as_latex())


pics = ["roc_curve", "heatmap", "reg_plot"]

for pic in pics:

    @pytask.mark.depends_on(
        {
            "plot": ["plot.py"],
            "concat_pred": BLD / "python" / "predictions" / "concatenated_pred.pkl",
            "data_benchmark": BLD / "python" / "data" / "data_benchmark.pkl",
            "scores": BLD / "python" / "predictions" / "prediction_scores.pkl",
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "figures" / f"basketball_pics_{pic}.pdf")
    def task_create_results_pics_python(depends_on, produces, pic=pic):
        """Produce multiple descriptive graphs in pdf format based on the basketball
        data analysis.
        """
        data_benchmark = pd.read_pickle(depends_on["data_benchmark"])
        concat_pred = pd.read_pickle(depends_on["concat_pred"])
        score = pd.read_pickle(depends_on["scores"])
        score = score.loc[score["score_type"] == "fit_score", "score"]
        if pic == "roc_curve":
            plot_roc_curve(data_benchmark, concat_pred)
        elif pic == "heatmap":
            create_heatmap(concat_pred, data_benchmark, score)
        elif pic == "reg_plot":
            reg_plot(concat_pred)
        plt.savefig(produces)
        plt.close()
