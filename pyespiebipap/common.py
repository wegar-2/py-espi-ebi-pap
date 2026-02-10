from datetime import date, datetime
import logging
from typing import TypeAlias

import bs4
import pandas as pd
import requests

from pyespiebipap.constants import DEFAULT_DATE_FORMAT
from pyespiebipap.entry import Entry

logger = logging.getLogger(__name__)

BSTag: TypeAlias = bs4.element.Tag

def _make_single_date_url(d: date) -> str:
    return (f"https://espiebi.pap.pl/wyszukiwarka?"
            f"created={d.strftime(DEFAULT_DATE_FORMAT)}&"
            f"enddate={d.strftime(DEFAULT_DATE_FORMAT)}+23%3A59")


def _validate_li(li: BSTag) -> None:

    if (div_hour := li.find("div", class_="hour") is None) or len(div_hour) != 2:
        raise ValueError()

    if li.find("badge") is None:
        raise ValueError("Entry does not contain info on ")

    return


def _full_url_from_node(node: str) -> str:
    return f"https://espiebi.pap.pl/{node}"


def _parse_period(period: str) -> pd.Period:
    pass


def _parse_list_item(li: BSTag, d: date) -> Entry:
    ts_, period_ = li.find_all("div", class_="hour")
    return Entry(
        source=li.find("div", class_="badge").text,
        ts=datetime.combine(
            date=d,
            time=datetime.strptime(ts_.text, "%H:%M").time()
        ),
        period=_parse_period(period=period_.text),
        title=li.find("a").text,
        url=_full_url_from_node(node=li.find("a").get("href"))
    )


def scrape_date_entries(d: date) -> pd.DataFrame:
    url: str = _make_single_date_url(d=d)

    logger.info(f"Getting response from {url}")
    response = requests.get(url=url)
    response.raise_for_status()

    logger.info("Making a bs4 soup")
    soup = bs4.BeautifulSoup(response.text, "lxml")

    logger.info("Extracting ESPI/EBI entries from the soup")
    results_section = soup.find_all("li")
    entries: list[Entry | Exception] = []
    entries_count: int = len(entries)
    for i, li in enumerate(results_section, start=1):
        logger.info(f"Parsing entry {i}/{entries_count}")
        try:
            _validate_li(li)
        except Exception as e:
            entries.append(e)
        else:
            entries.append(_parse_list_item(li=li, d=d))

    return pd.DataFrame()

__all__ = ["scrape_date_entries"]
