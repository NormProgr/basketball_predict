"""Tasks for running the scraper."""
import os
from datetime import date

import pytask

from bask.config import BLD
from bask.preparation.parser import parser, scrapedate
from bask.preparation.scraper import scraper_by_month

months = ["october", "november", "december", "january", "february", "march", "april"]


@pytask.mark.try_first
@pytask.mark.depends_on(
    {
        "scripts": ["scraper.py"],
    },
)
@pytask.mark.task
# keep this you stupid commit hook @pytask.mark.produces(SRC / "preparation" / "data" / f"{month}_{scrapedate()}.html")
def task_produce_scrape(depends_on):
    url_start = "https://www.basketball-reference.com/leagues/NBA_2023_games-{}.html"
    scraper_by_month(months, url_start, date.today())


# keep   scraper_by_month(months=months, url_start=url_start, today=scrapedate())


folder_path = "bld/python/scrapes"
dir = os.listdir(folder_path)
if len(dir) != 0:
    # @pytask.mark.try_last
    @pytask.mark.depends_on(
        {
            "scripts": ["parser.py"],
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(BLD / "python" / "scrapes" / f"data_{scrapedate()}.pkl")
    def task_produce_data(depends_on, produces):
        df = parser(months, scrapedate())
        df.to_pickle(produces)
