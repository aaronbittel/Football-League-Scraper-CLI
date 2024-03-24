"""Handles request of Football table."""

from __future__ import annotations

from argparse import Namespace
from dataclasses import dataclass

from bundesliga_scraper.api import api
from bundesliga_scraper.data_printer import table_printer
from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES, League
from bundesliga_scraper.datatypes.matchday import Matchday
from bundesliga_scraper.datatypes.table import Table


@dataclass(frozen=True)
class MatchdaySelector:
    to: int
    from_: int = 1
    include_postponed_matches: bool = True
    home: bool = True
    away: bool = True


@dataclass(frozen=True)
class TableRequestJob:
    title: str
    matchday_selctor: MatchdaySelector


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
    season_matchdays = api.retrieve_all_matchdays(league)

    current_matchday = api.retrieve_current_matchday(league)
    active_matchday = get_active_matchday(season_matchdays[current_matchday - 1])

    table_request_job_queue = create_job_queue(args, active_matchday)

    empty_table: Table = api.initialize_league_table(league=league)
    for job in table_request_job_queue:
        handle_job(
            league=league,
            empty_table=empty_table,
            season_matchdays=season_matchdays,
            job=job,
            highlights=args.highlights,
        )


def handle_job(
    empty_table: Table,
    league: League,
    season_matchdays: list[Matchday],
    job: TableRequestJob,
    highlights: list[str],
):
    title, selector = job.title, job.matchday_selctor
    table = empty_table.copy()

    title = f"{LEAGUE_NAMES[league]} {title}"

    selected_matchdays = season_matchdays[selector.from_ - 1 : selector.to]
    table.calculate_table(
        matchdays=selected_matchdays, home=selector.home, away=selector.away
    )
    highlights = [] if highlights is None else highlights
    table_printer.print_table_entries(title, table.standings, highlights)


def create_job_queue(args: Namespace, active_matchday: int) -> list[TableRequestJob]:
    table_request_job_queue: list[TableRequestJob] = []

    if args.first_round:
        table_request_job_queue.append(create_first_round_job(active_matchday))

    if args.second_round:
        table_request_job_queue.append(create_second_round_job(active_matchday))

    if args.last:
        table_request_job_queue.append(create_last_job(args.last, active_matchday))

    if args.since:
        table_request_job_queue.append(create_since_job(args.since, active_matchday))

    if args.home:
        table_request_job_queue.append(create_home_job(active_matchday))

    if args.away:
        table_request_job_queue.append(create_away_job(active_matchday))

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
        table_request_job_queue.append(create_matchday_job(matchday, active_matchday))
    return table_request_job_queue


def get_active_matchday(current_matchday: Matchday) -> int:
    for fixture in current_matchday.fixtures:
        if fixture.match_is_finished or fixture.match_is_live:
            return current_matchday.matchday
    return current_matchday.matchday - 1


def create_matchday_job(matchday: int, active_matchday: int) -> TableRequestJob:
    selector = get_matchday_selector(matchday, active_matchday)
    title = f"Table Matchday {selector.to}"
    return TableRequestJob(title, selector)


def create_away_job(active_matchday: int) -> TableRequestJob:
    away_selector = get_away_selector(active_matchday)
    title = "Away Table"
    return TableRequestJob(title, away_selector)


def create_home_job(active_matchday: int) -> TableRequestJob:
    home_selector = get_home_selector(active_matchday)
    title = "Home Table"
    return TableRequestJob(title, home_selector)


def create_since_job(since: int, active_matchday: int) -> TableRequestJob:
    since_selector = get_since_selector(since, active_matchday)
    title = f"Table Since Matchday {since}"
    return TableRequestJob(title, since_selector)


def create_last_job(last: int, active_matchday: int) -> TableRequestJob:
    last_selector = get_last_selector(last, active_matchday)
    number_of_matchdays = last if last <= active_matchday else active_matchday
    title = f"Table Last {number_of_matchdays} Matches"
    return TableRequestJob(title, last_selector)


def create_second_round_job(active_matchday: int) -> TableRequestJob:
    second_round_selector = get_second_round_selector(active_matchday)
    title = "Second Round Table"
    return TableRequestJob(title, second_round_selector)


def create_first_round_job(active_matchday: int) -> TableRequestJob:
    first_round_selector = get_first_round_selector(active_matchday)
    title = "First Round Table"
    return TableRequestJob(title, first_round_selector)


def get_home_selector(active_matchday: int) -> MatchdaySelector:
    return MatchdaySelector(to=active_matchday, away=False)


def get_away_selector(active_matchday: int) -> MatchdaySelector:
    return MatchdaySelector(to=active_matchday, home=False)


def get_matchday_selector(matchday: int, active_matchday: int) -> MatchdaySelector:
    matchday = min(active_matchday, max(1, matchday))
    return MatchdaySelector(to=matchday, include_postponed_matches=False)


def get_last_selector(n: int, active_matchday: int) -> MatchdaySelector:
    matchday = active_matchday - n + 1
    if matchday < 1:
        matchday = 1
    return MatchdaySelector(from_=matchday, to=active_matchday)


def get_since_selector(since: int, active_matchday: int) -> MatchdaySelector:
    if since > active_matchday:
        since = active_matchday

    return MatchdaySelector(from_=since, to=active_matchday)


def get_first_round_selector(active_matchday: int) -> MatchdaySelector:
    matchday = min(FIRST_ROUND_MATCHDAY, active_matchday)
    return MatchdaySelector(to=matchday)


def get_second_round_selector(active_matchday: int) -> MatchdaySelector:
    if active_matchday <= FIRST_ROUND_MATCHDAY:
        # TODO Implement a 0-Table
        raise ValueError(
            f"No second half table available. Its only matchday {active_matchday}"
        )
    return MatchdaySelector(from_=FIRST_ROUND_MATCHDAY + 1, to=active_matchday)
