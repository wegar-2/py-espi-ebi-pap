import logging
from typing import Any, Optional, TypeAlias

import bs4
import pandas as pd
import requests

from pyespiebipap.common import BSTag, NodeSource, BSSoup
from pyespiebipap.common import extract_node_source

Response: TypeAlias = requests.models.Response


__all__ = ["parse_node_soup"]

logger = logging.getLogger(__name__)


def _extract_table_of_contents(
        response: Response,
        node_num: int
) -> pd.DataFrame:
    logger.info(f"Extracting Table of Contents from node {node_num}")
    soup = bs4.BeautifulSoup(response.text, "lxml")
    toc: BSTag = soup.find("div", class_="table-of-contents")
    toc_points: list[BSTag] = toc.find_all("a")

    rows: list[pd.DataFrame] = []

    for point in toc_points:
        rows.append(
            pd.DataFrame(data={
                "name": [point.text],
                "section": [point.get("href").lstrip("#")]
            })
        )
    return pd.concat(rows, axis=0).reset_index(drop=True)


def _extract_current_report(
        response: Response,
        toc: pd.DataFrame
) -> Any:

    logger.info("Extracting current report (raport bieżący)")

    soup = bs4.BeautifulSoup(response.text, "lxml")

    container = soup.find("div", class_="arkusz")
    table = container.find("table")

    rows = table.find_all("tr")

    data = {}
    last_label = None

    for row in rows:
        cells = row.find_all("td")
        texts = [
            cell.get_text(separator=" ", strip=True)
            for cell in cells
            if cell.get_text(strip=True)
        ]

        if not texts:
            continue

        if len(texts) == 1:
            if last_label:
                data[last_label] += "\n" + texts[0]
        elif len(texts) >= 2:
            key = texts[0]
            value = " ".join(texts[1:])

            data[key] = value
            last_label = key

    data
    return response


def _extract_entity_info():
    pass


def _extract_signatures():
    pass


def _extract_attachments():
    pass


def parse_node_soup(
        node_soup: BSSoup,
        node_source: Optional[NodeSource] = None
) -> Any:

    node_url: str = _make_node_id(node_num=node_num)

    logging.info(f"Getting node content from {node_url=}")
    response: Response = requests.get(node_url)
    response.raise_for_status()

    toc: pd.DataFrame = _extract_table_of_contents(
        response=response, node_num=node_num)

    current_report = _extract_current_report(response=response, toc=toc)

    logger.info("Processing entity info (informacje o podmiocie)")
    logger.info("Processing signatures of representatives (PODPISY OSÓB REPREZENTUJĄCYCH SPÓŁKĘ)")



if __name__ == "__main__":
    # parse_node_soup()
    pass
