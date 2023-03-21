import os
from datetime import datetime

import requests as req
from bask.config import BLD
from bask.preparation.parser import parser
from bask.preparation.scraper import _check_internet, _remove_old_scrapes, scrapedate


def test_scraper():
    """Test whether the correct amount of files is generated.

    Raises:
        Assert: Raises an error if the 7 months long basketball season is not
            represented by 7 html files. If not, the function scraper_by_month or
            _remove_old_scrapes does not work as intended.

    """
    prefixed = [
        filename
        for filename in os.listdir("bld/python/scrapes")
        if filename.endswith(".html")
    ]
    assert len(prefixed) == 7, "Error: Not the right number of .html files."


def test_parser():
    """Test if the right amount of months is parsed.

    Raises:
        Assert: Raises an error if not the 7 months are represented in the data.

    """
    path = BLD / "python" / "scrapes"
    months = [
        "october",
        "november",
        "december",
        "january",
        "february",
        "march",
        "april",
    ]
    df = parser(months, scrapedate(), path)
    parts = []
    for date_str in df["Date"]:
        mon = date_str.split(" ")[1]
        parts.append(mon)
    parts = set(parts)
    assert len(parts) == len(
        months,
    ), f"Error: Wrong number of months in data frame. Data frame includes {parts}."


def test_scrapedate():
    """Check whether scrapedate function returns the right format.

    Raises:
        Assert: Raises an error if the expected format of date and the used format are
            different.

    """
    expected_format = "%Y-%m-%d"
    scrape = scrapedate()
    assert datetime.strptime(
        scrape,
        expected_format,
    ), f"Error: scrapedate {scrape} is not a valid date."


def test_check_internet(url="https://github.com/", timeout=5):
    """Check whether there is an internet connection.

    Args:
        url (string): The URL to be used for the connectivity test. Default value is
            "https://github.com/".
        timeout (integer): The maximum time, in seconds, allowed for the request to
            complete. Default value is 5 seconds.


    Raises:
        Assert: Raises an error if there is an internet connection to the one url but
            not to the other.

    """
    check = _check_internet()
    try:
        _ = req.head(url, timeout=timeout)
        snd_check = True
    except OSError:
        snd_check = False
    assert check == snd_check, "Internet connection is not available."


def test_remove_old_scrapes(tmpdir):
    """Test if html files are removed by function.

    Args:
        tmpdir (py.path.local): Pytest fixture providing a temporary directory unique
            to each test function.

    Raises:
        Assert (1st to 4th assert): Raises an assert if the html files still exist.
        Assert (5th assert): Raises an assert if the py file does not exist anymore.

    """
    sample_files = [
        "file1.html",
        "file2.html",
        "file3.html",
        "file4.html",
        "someotherfile.py",
    ]
    for f in sample_files:
        open(os.path.join(tmpdir, f), "w").close()
    _remove_old_scrapes(tmpdir)
    remaining_files = os.listdir(tmpdir)
    assert "file1.html" not in remaining_files, "Error: Not all html files deleted."
    assert "file2.html" not in remaining_files, "Error: Not all html files deleted."
    assert "file4.html" not in remaining_files, "Error: Not all html files deleted."
    assert "file5.html" not in remaining_files, "Error: Not all html files deleted."
    assert "someotherfile.py" in remaining_files, "Error: Non-html file deleted."
