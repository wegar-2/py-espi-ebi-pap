from datetime import date
import logging
from typing import Any

import bs4
import pandas as pd
import requests

from pyespiebipap.constants import DEFAULT_DATE_FORMAT

logger = logging.getLogger(__name__)


def _make_single_date_url(d: date) -> str:
    return (f"https://espiebi.pap.pl/wyszukiwarka?"
            f"created={d.strftime(DEFAULT_DATE_FORMAT)}&"
            f"enddate={d.strftime(DEFAULT_DATE_FORMAT)}+23%3A59")


def scrape_date_entries(d: date) -> Any:
    url: str = _make_single_date_url(d=d)

    response = requests.get(url=url)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.text, "lxml")

    results_section = soup.find_all("li")

    scraped_data = []

    # for li in results_section:
    #     # time = li.find_previous_sibling(text=True)
    #     link = li.find("a")
    #
    #     children = list(li.children)
    #     li.find_all("div", class_="hour")
    #
    #     time_child = list(li.children)[3]
    #     # time_child.getText()
    #
    #     if link and time:
    #         scraped_data.append({
    #             "time": time.strip(),
    #             "title": link.get_text(strip=True),
    #             "href": link.get("href")
    #         })
    # # scraped_data[10]
    # for item in scraped_data:
    #     print(item)


__all__ = ["scrape_date_entries"]
