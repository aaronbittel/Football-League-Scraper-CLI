"""Handles request of Football table."""

from __future__ import annotations

from argparse import Namespace
from dataclasses import dataclass

from bundesliga_scraper.api import api
from bundesliga_scraper.data_printer import table_printer
from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.matchday import Matchday
from bundesliga_scraper.datatypes.table import Table


@dataclass(frozen=True)
class FixtureSelector:
    to: int
    from_: int = 1
    include_postponed_matches: bool = True


FIRST_ROUND_MATCHDAY = 17
MAX_MATCHDAY = 34


def handle_table_request(args: Namespace) -> None:
    """Handles the table request.

    Args:
        args (Namespace): user arguments
    """

    league = (
        api.League.Bundesliga
        if args.league == "bundesliga"
        else api.League.Bundesliga_2
    )
    all_fixtures = api.retrieve_all_fixtures(league)

    all_matchdays: list[Matchday] = extract_all_matchdays(all_fixtures)

    active_matchday = get_active_matchday(
        all_fixtures, current_matchday=api.retrieve_current_matchday(league=league)
    )

    table_list_job_queue = []

    if args.first_round:
        table_list_job_queue.append(create_first_round_job(active_matchday))

    if args.second_round:
        table_list_job_queue.append(create_second_round_job(active_matchday))

    if args.last:
        table_list_job_queue.append(create_last_job(args.last, active_matchday))

    if args.since:
        table_list_job_queue.append(create_since_job(args.since, active_matchday))

    if args.home:
        table_list_job_queue.append(create_home_job(active_matchday))

    if args.away:
        table_list_job_queue.append(create_away_job(active_matchday))

    if args.matchday or not any(
        (
            args.first_round,
            args.second_round,
            args.last,
            args.since,
            args.home,
            args.away,
        )
    ):
        matchday = active_matchday if args.matchday is None else args.matchday
        table_list_job_queue.append(create_matchday_job(matchday, active_matchday))

    for job in table_list_job_queue:
        table: Table = api.initialize_league_table(league=league)
        title, selector, home, away = job

        title = f"{LEAGUE_NAMES[league]} {title}"

        selected_matchdays = all_matchdays[selector.from_ - 1 : selector.to]
        table.calculate_table(matchdays=selected_matchdays, home=home, away=away)
        highlights = [] if args.highlights is None else args.highlights
        table_printer.print_table_entries(title, table.standings, highlights)


def extract_all_matchdays(all_fixtures: list[FixtureEntry]) -> list[Matchday]:
    all_matchdays: list[Matchday] = []
    for i in range(1, 35):
        all_matchdays.append(Matchday(matchday=i, fixtures=[]))
    for fixture in all_fixtures:
        matchday = fixture.matchday
        all_matchdays[matchday - 1].fixtures.append(fixture)

    return all_matchdays


def get_active_matchday(all_fixtures: list[FixtureEntry], current_matchday: int) -> int:
    for fixture in all_fixtures:
        if fixture.matchday != current_matchday:
            continue
        if fixture.match_is_finished or fixture.match_is_live:
            return current_matchday
        else:
            return current_matchday - 1


def create_matchday_job(matchday: int, active_matchday: int) -> dict:
    selector = get_matchday_selector(matchday, active_matchday)
    title = f"Table Matchday {selector.to}"
    return title, selector, True, True


def create_away_job(active_matchday: int) -> dict:
    away_selector = get_away_selector(active_matchday)
    title = "Away Table"
    return title, away_selector, False, True


def create_home_job(active_matchday: int) -> dict:
    home_selector = get_home_selector(active_matchday)
    title = "Home Table"
    return title, home_selector, True, False


def create_since_job(since: int, active_matchday: int) -> dict:
    since_selector = get_since_selector(since, active_matchday)
    title = f"Table Since Matchday {since}"
    return title, since_selector, True, True


def create_last_job(last: int, active_matchday: int) -> dict:
    last_selector = get_last_selector(last, active_matchday)
    number_of_matchdays = last if last <= active_matchday else active_matchday
    title = f"Table Last {number_of_matchdays} Matches"
    return title, last_selector, True, True


def create_second_round_job(active_matchday: int) -> dict:
    second_round_selector = get_second_round_selector(active_matchday)
    title = "Second Round Table"
    return title, second_round_selector, True, True


def create_first_round_job(active_matchday: int) -> dict:
    first_round_selector = get_first_round_selector(active_matchday)
    title = "First Round Table"
    return title, first_round_selector, True, True


def get_home_selector(active_matchday: int) -> FixtureSelector:
    return FixtureSelector(to=active_matchday)


def get_away_selector(active_matchday: int) -> FixtureSelector:
    return FixtureSelector(to=active_matchday)


def get_matchday_selector(matchday: int, active_matchday: int) -> FixtureSelector:
    matchday = min(active_matchday, max(1, matchday))
    return FixtureSelector(to=matchday, include_postponed_matches=False)


def get_last_selector(n: int, active_matchday: int) -> FixtureSelector:
    matchday = active_matchday - n + 1
    if matchday < 1:
        matchday = 1
    return FixtureSelector(from_=matchday, to=active_matchday)


def get_since_selector(since: int, active_matchday: int) -> FixtureSelector:
    if since > active_matchday:
        since = active_matchday

    return FixtureSelector(from_=since, to=active_matchday)


def get_first_round_selector(active_matchday: int) -> FixtureSelector:
    matchday = min(FIRST_ROUND_MATCHDAY, active_matchday)
    return FixtureSelector(to=matchday)


def get_second_round_selector(active_matchday: int) -> FixtureSelector:
    if active_matchday <= FIRST_ROUND_MATCHDAY:
        # TODO Implement a 0-Table
        raise ValueError(
            f"No second half table available. Its only matchday {active_matchday}"
        )
    return FixtureSelector(from_=FIRST_ROUND_MATCHDAY + 1, to=active_matchday)
