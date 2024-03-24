"""Handles requests for Football fixtures."""

from __future__ import annotations

from argparse import Namespace

from bundesliga_scraper.api import api
from bundesliga_scraper.data_printer import fixture_printer
from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES

MAX_MATCHDAY = 34


def handle_fixture_request(args: Namespace) -> None:
    """Handles the fixture request.

    Args:
        args (Namespace): user arguments
    """
    league = (
        api.League.Bundesliga
        if args.league == "bundesliga"
        else api.League.Bundesliga_2
    )

    season_matchdays = api.retrieve_all_matchdays(league=league)

    matchday = args.matchday

    # user did not provide a matchday -> get current
    if matchday is None:
        effective_count = args.next - args.prev
        matchday = api.retrieve_current_matchday(league) + effective_count
        matchday = min(MAX_MATCHDAY, max(1, matchday))

    matchday = season_matchdays[matchday - 1]

    title = f"{LEAGUE_NAMES[league]} Fixture {matchday.matchday}"
    highlights = [] if args.highlights is None else args.highlights

    fixture_printer.print_fixture_entries(
        title=title, matchday=matchday, highlights=highlights
    )
