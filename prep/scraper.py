import requests as req

url_start = "https://www.basketball-reference.com/leagues/NBA_2023_games-{}.html"
# replace october by month string with bracket{}

months = ["october", "november", "december", "january", "february", "march", "april"]


def scraper_by_month(months=months, url_start=url_start):
    """Scrape the data by month and save it.

    Args:
        months (list): List of months to be scraped.
        url_start (url): Source url to scrape data.

    """
    for month in months:
        url = url_start.format(month)
        data = req.get(url)

        with open(f"prep/data/{month}.html", "w+") as f:
            f.write(data.text)


scraper_by_month()
