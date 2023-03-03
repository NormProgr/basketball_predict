"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import pytask

from bask.config import BLD
from bask.final.plot import generate_prediction_table

names = ["table", "table_playoffs"]

for i in names:

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
        else:
            model = generate_prediction_table(res_pred=res_pred, playoff=True)
        table = model.style.hide(axis="index").to_latex()
        with open(produces, "w") as f:
            f.write(table)
