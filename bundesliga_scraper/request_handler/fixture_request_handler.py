"""Handles requests for Football fixtures."""

from __future__ import annotations

from bundesliga_scraper.api import api
from bundesliga_scraper.data_printer import fixture_printer
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry

MAX_MATCHDAY = 34


def handle_fixture_request(args: dict[str, str | int]) -> None:
    """Handles the fixture request.

    Args:
        args (dict[str, str  |  int]): user arguments
    """
    league = (
        api.League.Bundesliga
        if args.league == "bundesliga"
        else api.League.Bundesliga_2
    )

    fixture_entries = api.retrieve_all_fixtures(league=league)

    matchday = args.matchday

    # user did not provide a matchday -> get current
    if matchday == -1:
        effective_count = args.next - args.prev
        matchday = api.retrieve_current_matchday(league) + effective_count
        matchday = min(MAX_MATCHDAY, max(1, matchday))

    total = 0
    matchday_fixtures: list[FixtureEntry] = []
    for fixture in fixture_entries:
        if fixture.matchday == matchday:
            matchday_fixtures.append(fixture)
            total += 1
            if total == 9:
                break

    fixture_printer.print_fixture_entries(
        league=league, matchday_fixtures=matchday_fixtures
    )
