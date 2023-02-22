"""Tasks for running the scraper."""
import pytask

from bask.config import SRC
from bask.preparation.parser import parser
from bask.preparation.scraper import months, scrapedate


@pytask.mark.depends_on(
    {
        "scripts": ["parser.py"],
    },
)
@pytask.mark.task
@pytask.mark.produces(SRC / "data" / f"data_{scrapedate}.pkl")
def task_produce_data(produces, months=months, scrapedate=scrapedate):
    df = parser(months, scrapedate)
    df.to_pickle(produces)
