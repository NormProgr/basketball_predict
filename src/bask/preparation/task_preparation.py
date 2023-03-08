"""Tasks for running the scraper."""
import os

import pytask

from bask.config import SRC
from bask.preparation.parser import parser, scrapedate
from bask.preparation.scraper import months, scraper_by_month


@pytask.mark.try_first
@pytask.mark.depends_on({"scrape": ["scraper.py"]})
@pytask.mark.task
# keep this you stupid commit hook @pytask.mark.produces(SRC / "preparation" / "data" / f"{month}_{scrapedate()}.html")
def task_produce_scrape():
    scraper_by_month()


# keep   scraper_by_month(months=months, url_start=url_start, today=scrapedate())


folder_path = "src/bask/preparation/data"
if os.path.exists(folder_path):

    @pytask.mark.try_last
    @pytask.mark.depends_on(
        {
            "scripts": ["parser.py"],
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(SRC / "data" / f"data_{scrapedate()}.pkl")
    def task_produce_data(produces, months=months):
        df = parser(months, scrapedate())
        df.to_pickle(produces)
