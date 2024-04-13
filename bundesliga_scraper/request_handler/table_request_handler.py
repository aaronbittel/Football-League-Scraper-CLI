"""Handles request of Football table."""

from __future__ import annotations

from argparse import Namespace
from dataclasses import dataclass

from bundesliga_scraper.datatypes.table_entry import TableEntry
import bundesliga_scraper.request_handler.handler as h
from bundesliga_scraper.api import api
from bundesliga_scraper.data_printer import table_printer
from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES, League
from bundesliga_scraper.datatypes.matchday import Matchday
from bundesliga_scraper.datatypes.table import Table
from bundesliga_scraper.table.calculator import calculate
from bundesliga_scraper.table.parser import MatchdaySelector


def table_request_handler(matchday_selector: MatchdaySelector) -> None:
    """Handles the table request.

    Args:
        args (Namespace): user arguments
    """
    league = matchday_selector.league
    all_matchdays = h.cache[league]["all_matchdays"]
    standings = calculate(
        matchdays=all_matchdays[matchday_selector.from_ - 1 : matchday_selector.to],
        matchday_selector=matchday_selector,
    )


def handle_job(
    empty_table: Table,
    league: League,
    season_matchdays: list[Matchday],
    job: TableRequestJob,
    highlights: list[str],
) -> None:
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
