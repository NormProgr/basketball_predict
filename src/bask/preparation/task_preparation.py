"""Tasks for running the scraper."""
from datetime import date

import pytask

from bask.config import BLD
from bask.preparation.parser import parser
from bask.preparation.scraper import _check_internet, scrapedate, scraper

months = ["october", "november", "december", "january", "february", "march", "april"]
url_source = "https://www.basketball-reference.com/leagues/NBA_2023_games-{}.html"
date = date.today() if _check_internet() else scrapedate()


@pytask.mark.depends_on(
    {
        "scripts": ["scraper.py"],
    },
)
@pytask.mark.task
@pytask.mark.produces(
    {
        "scrapes": BLD / "python" / "scrapes",
        "oct": BLD / "python" / "scrapes" / f"october_{date}.html",
        "nov": BLD / "python" / "scrapes" / f"november_{date}.html",
        "dec": BLD / "python" / "scrapes" / f"december_{date}.html",
        "jan": BLD / "python" / "scrapes" / f"january_{date}.html",
        "feb": BLD / "python" / "scrapes" / f"february_{date}.html",
        "mar": BLD / "python" / "scrapes" / f"march_{date}.html",
        "apr": BLD / "python" / "scrapes" / f"april_{date}.html",
    },
)
def task_produce_scrape(produces):
    """Produce multiple basketball data .html scrapes and save them."""
    url_start = "https://www.basketball-reference.com/leagues/NBA_2023_games-{}.html"
    scraper(produces["scrapes"], months, url_start)


@pytask.mark.depends_on(
    {
        "scripts": ["parser.py"],
        "scrapes": BLD / "python" / "scrapes",
        "oct": BLD / "python" / "scrapes" / f"october_{date}.html",
        "nov": BLD / "python" / "scrapes" / f"november_{date}.html",
        "dec": BLD / "python" / "scrapes" / f"december_{date}.html",
        "jan": BLD / "python" / "scrapes" / f"january_{date}.html",
        "feb": BLD / "python" / "scrapes" / f"february_{date}.html",
        "mar": BLD / "python" / "scrapes" / f"march_{date}.html",
        "apr": BLD / "python" / "scrapes" / f"april_{date}.html",
    },
)
@pytask.mark.task
@pytask.mark.produces(BLD / "python" / "parsed" / f"data_{date}.pkl")
def task_produce_data(depends_on, produces):
    """Convert the .html scrapes to one data file."""
    df = parser(months, date, depends_on["scrapes"])
    df.to_pickle(produces)
