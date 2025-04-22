"""Handles requests for Football fixtures."""

from __future__ import annotations

from argparse import Namespace

from bundesliga_scraper.api import api
from bundesliga_scraper.data_printer import fixture_printer
from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES
from bundesliga_scraper.datatypes.matchday import Matchday
from bundesliga_scraper.request_handler.utils import MAX_MATCHDAY, get_league
from dataclasses import dataclass


TITLE_TEMPLATE = "{} Fixture {}"


@dataclass(frozen=True)
class MatchdaySelectionParams:
    nxt: int
    prev: int
    user_matchday: int
    current_matchday: int


def handle_fixture_request(args: Namespace) -> None:
    """Handles the fixture request.

    Args:
        args (Namespace): user arguments
    """
    league = get_league(args.league)

    season_matchdays = api.retrieve_all_matchdays(league=league)
    current_matchday = api.retrieve_current_matchday(league)

    matchday_selection_params = MatchdaySelectionParams(
        nxt=args.next,
        prev=args.prev,
        user_matchday=args.matchday,
        current_matchday=current_matchday,
    )
    selected_matchday = get_selected_matchday_games(
        matchday_selection_params, season_matchdays
    )

    title = TITLE_TEMPLATE.format(LEAGUE_NAMES[league], selected_matchday.matchday)
    highlights = [] if args.highlights is None else args.highlights

    fixture_printer.print_fixture_entries(
        title=title, matchday=selected_matchday, highlights=highlights
    )


def get_selected_matchday_games(
    params: MatchdaySelectionParams, season_matchdays: list[Matchday]
) -> Matchday:
    matchday = get_matchday(params)
    return season_matchdays[matchday - 1]


def get_matchday(params: MatchdaySelectionParams) -> int:
    # user did not provide a matchday -> get current
    matchday = 0
    if not params.user_matchday:
        effective_count = params.nxt - params.prev
        matchday = params.current_matchday + effective_count
    return min(MAX_MATCHDAY, max(1, matchday))
