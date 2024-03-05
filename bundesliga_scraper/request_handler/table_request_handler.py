"""Handles request of Football table."""

from __future__ import annotations

from bundesliga_scraper import data_fetcher
from bundesliga_scraper.config import LEAGUE_TABELS_BASE_URLS
from bundesliga_scraper.data_extractors import (
    bundesliga_table_extractor,
)
from bundesliga_scraper.data_printer import table_printer


def handle_table_request(user_args: dict[str, str | int]) -> None:
    """Handles the table request.

    Args:
        user_args (dict[str, str  |  int]): user arguments
    """
    league = user_args["league"]
    matchday = user_args["table"]

    print("Fetching data from web ...\n")
    soup = data_fetcher.fetch_html(
        f"{LEAGUE_TABELS_BASE_URLS[league.lower()]}{matchday}"
    )
    table_entries = bundesliga_table_extractor.extract_bundesliga_table_information(
        soup
    )

    print(table_printer.styled_bundesliga_table_information(table_entries))
