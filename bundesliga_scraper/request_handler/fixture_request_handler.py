"""Handles requests for Football fixtures."""

from __future__ import annotations

from bundesliga_scraper import data_fetcher
from bundesliga_scraper.config import LEAGUE_FIXTURES_BASE_URLS
from bundesliga_scraper.data_extractors import bundesliga_fixture_extractor
from bundesliga_scraper.data_printer import fixture_printer


def handle_fixture_request(args: dict[str, str | int]) -> None:
    """Handles the fixture request.

    Args:
        args (dict[str, str  |  int]): user arguments
    """
    league = args["league"]
    matchday = args["fixture"]

    print("Fetching data from the web ...\n")
    soup = data_fetcher.fetch_html(
        f"{LEAGUE_FIXTURES_BASE_URLS[league.lower()]}{matchday}"
    )

    fixture = bundesliga_fixture_extractor.extract_bundesliga_fixture_information(soup)
    print(fixture_printer.styled_bundesliga_fixure(fixture))
