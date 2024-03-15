"""Handles request of Football table."""

from __future__ import annotations

from argparse import Namespace

from bundesliga_scraper.api import api
from bundesliga_scraper.data_printer import table_printer
from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES, League
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.table_entry import TableEntry

from dataclasses import dataclass


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
    current_matchday = api.retrieve_current_matchday(league=league)
    active_matchday = get_active_matchday(all_fixtures, current_matchday)

    matchday = current_matchday if args.matchday is None else args.matchday

    table_list_job_queue = []

    if args.first_round:
        table_list_job_queue.append(create_first_round_job(league, current_matchday))

    if args.second_round:
        table_list_job_queue.append(create_second_round_job(league, current_matchday))

    if args.last:
        table_list_job_queue.append(create_last_job(args.last, league, active_matchday))

    if args.since:
        table_list_job_queue.append(
            create_since_job(args.since, league, active_matchday)
        )

    if args.home:
        table_list_job_queue.append(create_home_job(league, active_matchday))

    if args.away:
        table_list_job_queue.append(create_away_job(league, active_matchday))

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
        table_list_job_queue.append(
            create_matchday_job(league, matchday, active_matchday)
        )

    for job in table_list_job_queue:
        title, selector, calculate = job["title"], job["selector"], job["func"]
        selected_fixtures = select_fixtures(all_fixtures, selector)
        table_list = calculate(selected_fixtures)
        highlights = [] if args.highlights is None else args.highlights
        table_printer.print_table_entries(title, table_list, highlights)


def create_matchday_job(league: League, matchday: int, active_matchday: int) -> dict:
    selector = get_matchday_selector(matchday, active_matchday)
    title = f"{LEAGUE_NAMES[league]} Table Matchday {active_matchday}"
    return {"title": title, "selector": selector, "func": calculate_table}


def create_away_job(league: League, active_matchday: int) -> dict:
    away_selector = get_away_selector(active_matchday)
    title = f"{LEAGUE_NAMES[league]} Away Table"
    return {"title": title, "selector": away_selector, "func": calculate_away_table}


def create_home_job(league: League, active_matchday: int) -> dict:
    home_selector = get_home_selector(active_matchday)
    title = f"{LEAGUE_NAMES[league]} Home Table"
    return {"title": title, "selector": home_selector, "func": calculate_home_table}


def create_since_job(since: int, league: League, active_matchday: int) -> dict:
    since_selector = get_since_selector(since, active_matchday)
    title = f"{LEAGUE_NAMES[league]} Table Since Matchday {since}"
    return {"title": title, "selector": since_selector, "func": calculate_table}


def create_last_job(last: int, league: League, active_matchday: int) -> dict:
    last_selector = get_last_selector(last, active_matchday)
    number_of_matchdays = last if last <= active_matchday else active_matchday
    title = f"{LEAGUE_NAMES[league]} Table Last {number_of_matchdays} Matches"
    return {"title": title, "selector": last_selector, "func": calculate_table}


def create_second_round_job(league: League, current_matchday: int) -> dict:
    second_round_selector = get_second_round_selector(current_matchday)
    title = f"{LEAGUE_NAMES[league]} Second Round Table"
    return {"title": title, "selector": second_round_selector, "func": calculate_table}


def create_first_round_job(league: League, current_matchday: int) -> dict:
    first_round_selector = get_first_round_selector(current_matchday)
    title = f"{LEAGUE_NAMES[league]} First Round Table"
    return {"title": title, "selector": first_round_selector, "func": calculate_table}


def standard_title(league: League, matchday: int) -> str:
    return f"{LEAGUE_NAMES[league]} Matchday {matchday}"


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


def initialize_empty_table_entries_dict(
    fixtures: list[FixtureEntry],
) -> dict[str, TableEntry]:
    table_entries = {}
    for fixture in fixtures[0:9]:
        table_entries[fixture.home_team] = TableEntry(team_name=fixture.home_team)
        table_entries[fixture.away_team] = TableEntry(team_name=fixture.away_team)
    return table_entries


def select_fixtures(
    all_fixtures: list[FixtureEntry], selector: FixtureSelector
) -> list[FixtureEntry]:
    selected_fixtures = []
    for fixture in all_fixtures:
        if fixture.matchday < selector.from_:
            continue
        if fixture.matchday > selector.to:
            if selector.include_postponed_matches and len(selected_fixtures) != 9 * (
                selector.to - selector.from_ + 1
            ):
                continue
            break
        selected_fixtures.append(fixture)
    return selected_fixtures


def get_first_round_selector(current_matchday: int) -> FixtureSelector:
    matchday = min(FIRST_ROUND_MATCHDAY, current_matchday)
    return FixtureSelector(to=matchday)


def get_second_round_selector(current_matchday: int) -> FixtureSelector:
    if current_matchday <= FIRST_ROUND_MATCHDAY:
        # TODO Implement a 0-Table
        raise ValueError(
            f"No second half table available. Its only matchday {current_matchday}"
        )
    return FixtureSelector(from_=FIRST_ROUND_MATCHDAY, to=current_matchday)


def calculate_table(fixtures: list[FixtureEntry]) -> list[TableEntry]:
    # TODO Somehow use Defaultdict
    table_entries = initialize_empty_table_entries_dict(fixtures)

    for fixture in fixtures:
        table_entries[fixture.home_team].update(fixture)
        table_entries[fixture.away_team].update(fixture)

    table_list = list(table_entries.values())
    return sorted(table_list, reverse=True)


def calculate_home_table(fixtures: list[FixtureEntry]) -> list[TableEntry]:
    # TODO Somehow use Defaultdict
    table_entries = initialize_empty_table_entries_dict(fixtures)

    for fixture in fixtures:
        table_entries[fixture.home_team].update(fixture)

    table_list = list(table_entries.values())
    return sorted(table_list, reverse=True)


def calculate_away_table(fixtures: list[FixtureEntry]) -> list[TableEntry]:
    # TODO Somehow use Defaultdict
    table_entries = initialize_empty_table_entries_dict(fixtures)

    for fixture in fixtures:
        table_entries[fixture.away_team].update(fixture)

    table_list = list(table_entries.values())
    return sorted(table_list, reverse=True)


def index_of(entry: TableEntry, table_list: list[TableEntry]) -> int:
    for i, table_entry in enumerate(table_list):
        if table_entry.team_name == entry.team_name:
            return i


def get_active_matchday(all_fixtures: list[FixtureEntry], current_matchday: int) -> int:
    for fixture in all_fixtures:
        if fixture.matchday != current_matchday:
            continue
        if fixture.match_is_finished or fixture.match_is_live:
            return current_matchday
        else:
            return current_matchday - 1
