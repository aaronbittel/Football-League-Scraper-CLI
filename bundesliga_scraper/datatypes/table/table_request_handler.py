"""Handles request of Football table."""

from __future__ import annotations

import argparse

from rich import console

from bundesliga_scraper.api import api
from bundesliga_scraper.datatypes import utils
from bundesliga_scraper.datatypes.table import (
    table_calculator,
    table_creation,
    table_parser,
)


def table_request_handler(args: argparse.Namespace) -> None:
    """Handles the table request.

    Args:
        args (Namespace): user arguments
    """
    league = utils.get_league(args.league)

    all_matchdays = api.retrieve_all_matchdays(league)
    current_matchday = api.retrieve_current_matchday(league)

    active_matchday = utils.get_active_matchday(all_matchdays[current_matchday - 1])

    for title, matchday_selector in table_parser.parse(args, active_matchday):
        standings = table_calculator.calculate(
            all_matchdays=all_matchdays, matchday_selector=matchday_selector
        )

        request_job = table_creation.TableCreationJob(title, standings, args.highlights)
        table = table_creation.create_table(request_job)

        con = console.Console()
        con.print(table, justify="center")
