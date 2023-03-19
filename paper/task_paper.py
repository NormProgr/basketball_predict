"""Tasks for compiling the paper and presentation(s)."""
import shutil

import pytask
from bask.config import BLD, PAPER_DIR
from pytask_latex import compilation_steps as cs


@pytask.mark.latex(
    script=PAPER_DIR / "bask.tex",
    document=BLD / "latex" / "bask.pdf",
    compilation_steps=cs.latexmk(
        options=("--pdf", "--interaction=nonstopmode", "--synctex=1", "--cd"),
    ),
)
@pytask.mark.task()
def task_compile_document():
    """Compile the document specified in the latex decorator."""


@pytask.mark.depends_on(BLD / "latex" / "bask.pdf")
@pytask.mark.task
@pytask.mark.produces(BLD.parent.resolve() / "bask.pdf")
def task_copy_to_root(depends_on, produces):
    """Copy a document to the root directory for easier retrieval."""
    shutil.copy(depends_on, produces)
