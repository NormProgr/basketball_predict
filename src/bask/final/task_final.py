"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import pytask
from statsmodels.iolib.smpickle import load_pickle

from bask.config import BLD
from bask.final.plot import (
    generate_prediction_table,
    naive_inf_table,
)

tables = ["table", "table_playoffs"]  # ,"inf_table"

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


pics = ["heatmap"]
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
    @pytask.mark.produces(BLD / "python" / "tables" / f"basketball_pics_{pic}.pdf")
    def task_create_results_pic_python(depends_on, produces, pic=pic):
        """Produce multiple descriptive graphs in pdf format based on the basketball
        data analysis.
        """
        data_benchmark = pd.read_pickle(depends_on["data_benchmark"])
        concat_pred = pd.read_csv(depends_on["concat_pred"])
        score = pd.read_pickle(depends_on["scores"])
        # old code, keep in case loc problems arise score = score.iloc[0, 1]
        score = score.loc[score["score_type"] == "fit_score", "score"]
        if pic == "heatmap":
            graph = create_heatmap(concat_pred, data_benchmark, score)
        with open(produces, "w"):
            graph.savefig(produces)


#########

"""
pics = ["heatmap", "roc_curve", "reg_plot"] #, "reg_plot"

for pic in pics:
    @pytask.mark.skip
    @pytask.mark.depends_on(
        {
            "plot": ["plot.py"],
            "concat_pred": BLD / "python" / "predictions" / "concatenated_pred.pkl",
            "data_benchmark": BLD / "python" / "data" / "data_benchmark.pkl",
            "scores": BLD / "python" / "predictions" / "prediction_scores.pkl",
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "tables" / f"basketball_pics_{pic}.pdf")
    def task_create_results_pics_python(depends_on, produces, pic=pic):
        data_benchmark = pd.read_pickle(depends_on["data_benchmark"])
        concat_pred = pd.read_csv(depends_on["concat_pred"])
        score = pd.read_pickle(depends_on["scores"])
        # old code, keep in case loc problems arise score = score.iloc[0, 1]
        score = score.loc[score["score_type"] == "fit_score", "score"]
        if pic == "heatmap":
            graph = create_heatmap(concat_pred, data_benchmark, score)
        elif pic == "roc_curve":
            graph = plot_roc_curve(data_benchmark, concat_pred)
        elif pic == "reg_plot":
            graph = reg_plot(concat_pred)
        with open(produces, "w"):
            graph.write_image(produces)
"""
# """Produce multiple descriptive graphs in pdf format based on the basketball data analysis."""
