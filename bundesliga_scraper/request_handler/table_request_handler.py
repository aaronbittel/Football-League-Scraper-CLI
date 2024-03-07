"""Handles request of Football table."""

from __future__ import annotations

from bundesliga_scraper.data_printer import table_printer
from bundesliga_scraper.api import api


def handle_table_request(user_args: dict[str, str | int]) -> None:
    """Handles the table request.

    Args:
        user_args (dict[str, str  |  int]): user arguments
    """
    league = (
        api.League.Bundesliga
        if user_args["league"] == "bundesliga"
        else api.League.Bundesliga_2
    )

    print("Fetching data from web ...\n")

    table_entries = api.retrieve_table(league=league, season=2023)
    table_printer.print_table_entries(table_entries)
