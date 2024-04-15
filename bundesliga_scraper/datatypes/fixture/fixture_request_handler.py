"""Handles requests for Football fixtures."""

from __future__ import annotations

from argparse import Namespace

from rich import console as con

from bundesliga_scraper.api import api
from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES
from bundesliga_scraper.datatypes.fixture import fixture_creation, fixture_parser
from bundesliga_scraper.datatypes.utils import get_league

TITLE_TEMPLATE = "{} Fixture {}"


def handle_fixture_request(args: Namespace) -> None:
    """Handles the fixture request.

    Args:
        args (Namespace): user arguments
    """
    league = get_league(args.league)

    current_matchday = api.retrieve_current_matchday(league)

    selected_matchday = fixture_parser.parse(args, current_matchday)

    selected_fixtures = api.retrieve_matchday_fixtures(league, selected_matchday)

    title = TITLE_TEMPLATE.format(LEAGUE_NAMES[league], selected_matchday)
    highlights = [] if args.highlights is None else args.highlights

    console = con.Console(highlight=None)
    console.print(title)
    for panel in fixture_creation.create_fixture_panels(
        fixtures=selected_fixtures, highlights=highlights
    ):
        console.print(panel)
