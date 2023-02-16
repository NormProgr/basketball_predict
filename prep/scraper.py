import os
from datetime import date

import requests as req

months = ["october", "november", "december", "january", "february", "march", "april"]
scrapedate = date.today()
# put in dictionary!

if __name__ == "__main__":

    url_start = "https://www.basketball-reference.com/leagues/NBA_2023_games-{}.html"
    # replace october by month string with bracket{}

    def _remove_old_scrapes():
        folder_path = "prep/data"
        if os.path.exists(folder_path):
            folder_contents = os.listdir(folder_path)
            for item in folder_contents:
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path) and item_path.endswith(".html"):
                    os.remove(item_path)

    def scraper_by_month(months=months, url_start=url_start, today=scrapedate):
        """Scrape the data by month and save it.

        Args:
            months (list): List of months to be scraped.
            url_start (url): Source url to scrape data.

        """
        _remove_old_scrapes()
        for month in months:
            url = url_start.format(month)
            data = req.get(url)

            with open(f"prep/data/{month}_{today}.html", "w+") as f:
                f.write(data.text)

    scraper_by_month()
