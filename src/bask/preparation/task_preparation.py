"""Tasks for running the scraper."""
import os
from datetime import date

import pytask

from bask.config import BLD
from bask.preparation.parser import parser
from bask.preparation.scraper import scraper

months = ["october", "november", "december", "january", "february", "march", "april"]
url_source = "https://www.basketball-reference.com/leagues/NBA_2023_games-{}.html"
date = date.today()


@pytask.mark.try_first
@pytask.mark.depends_on(
    {
        "scripts": ["scraper.py"],
    },
)
@pytask.mark.task
@pytask.mark.produces(BLD / "python" / "scrapes")
def task_produce_scrape(produces):
    url_start = "https://www.basketball-reference.com/leagues/NBA_2023_games-{}.html"
    scraper(produces, months, url_start)


folder_path = "bld/python/scrapes"
dir = os.listdir(folder_path)
if len(dir) != 0:
    # @pytask.mark.try_second
    @pytask.mark.depends_on(
        {
            "scripts": ["parser.py"],
            "scrapes": BLD / "python" / "scrapes",
        },
    )
    @pytask.mark.task
    # later try this @pytask.mark.produces(BLD / "python" / "parsed" / f"data_{scrapedate()}.pkl")
    @pytask.mark.produces(BLD / "python" / "parsed" / f"data_{date.today()}.pkl")
    def task_produce_data(depends_on, produces):
        df = parser(months, date.today(), depends_on["scrapes"])
        df.to_pickle(produces)
