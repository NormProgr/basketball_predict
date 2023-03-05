"""Tasks for running the scraper."""
import os
from datetime import date

import pytask

from bask.config import SRC
from bask.preparation.parser import parser
from bask.preparation.scraper import months, scraper_by_month, url_start

pytask.mark.try_first()
for month in months:
    task_name = f"task_produce_scrape_{month}"

    @pytask.mark.depends_on({"scrape": ["scraper.py"]})
    @pytask.mark.task
    @pytask.mark.produces(SRC / "preparation" / "data" / f"{month}_{date.today()}.html")
    def task_produce_scrape():
        (lambda produces: scraper_by_month([month], url_start, date.today()))


file_path = f"../folder_name/example_{month}_{date.today()}.txt"
if os.path.isfile(file_path):

    @pytask.mark.try_last
    @pytask.mark.depends_on(
        {
            "scripts": ["parser.py"],
        },
    )
    @pytask.mark.task
    @pytask.mark.produces(SRC / "data" / f"data_{date.today()()}.pkl")
    def task_produce_data(produces, months=months):
        df = parser(months, date.today())
        df.to_pickle(produces)
