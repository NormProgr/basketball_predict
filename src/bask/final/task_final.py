"""Tasks running the results formatting (tables, figures)."""


import pandas as pd
import pytask

from bask.config import BLD
from bask.final.plot import generate_prediction_table


# for group in GROUPS:
#
#
#    @pytask.mark.depends_on(
#        },
#    @pytask.mark.task(id=group, kwargs=kwargs)
#    def task_plot_results_by_age_python(depends_on, group, produces):


@pytask.mark.depends_on(
    {
        "plot": ["plot.py"],
        "res_pred": BLD / "python" / "data" / "result_prediction.csv",
    },
)
@pytask.mark.task
@pytask.mark.produces(BLD / "python" / "tables" / "basketball_results_table.tex")
def task_create_results_table_python(depends_on, produces):
    """Store a table in LaTeX format with the estimation results (Python version)."""
    res_pred = pd.read_csv(depends_on["res_pred"])
    model = generate_prediction_table(res_pred=res_pred)
    table = model.style.hide(axis="index").to_latex()
    with open(produces, "w") as f:
        f.write(table)
