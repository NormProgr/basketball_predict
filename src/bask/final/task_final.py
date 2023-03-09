"""Tasks running the results formatting (tables, figures)."""

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

tables = ["table", "table_playoffs"]  # ,"inf_table"

for i in tables:

    @pytask.mark.depends_on(
        {
            "plot": ["plot.py"],
            "result_pred": BLD / "python" / "predictions" / "team_result_pred.csv",
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "tables" / f"basketball_results_{i}.tex")
    def task_create_results_table_python(depends_on, produces, i=i):
        """Store a table in LaTeX format with the estimation results (Python
        version).
        """
        res_pred = pd.read_csv(depends_on["result_pred"])
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
        "inferencemodel": BLD / "python" / "predictions" / "inferencemodel.pkl",
    },
)
@pytask.mark.task
@pytask.mark.produces(BLD / "python" / "tables" / "inferencemodel.tex")
def task_produce_inf(depends_on, produces):
    inferencemodel = load_pickle(depends_on["inferencemodel"])
    model = naive_inf_table(inferencemodel)
    with open(produces, "w") as fh:
        fh.write(model.as_latex())


pics = ["heatmap", "roc_curve", "reg_plot"]

for pic in pics:

    @pytask.mark.depends_on(
        {
            "plot": ["plot.py"],
            "concat_pred": BLD / "python" / "predictions" / "concatenated_pred.csv",
            "data_benchmark": BLD / "python" / "data" / "data_benchmark.pkl",
            "scores": BLD / "python" / "predictions" / "prediction_scores.pkl",
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "tables" / f"basketball_pics_{pic}.pdf")
    def task_create_results_table_python(depends_on, produces, pic=pic):
        data_benchmark = pd.read_pickle(depends_on["data_benchmark"])
        concat_pred = pd.read_csv(depends_on["concat_pred"])
        score = pd.read_pickle(depends_on["scores"])
        score = score.iloc[0, 1]
        if pic == "heatmap":
            graph = create_heatmap(concat_pred, data_benchmark, score)
        elif pic == "roc_curve":
            graph = plot_roc_curve(data_benchmark, concat_pred)
        elif pic == "reg_plot":
            graph = reg_plot(concat_pred)
        with open(produces, "w"):
            graph.write_image(produces)
