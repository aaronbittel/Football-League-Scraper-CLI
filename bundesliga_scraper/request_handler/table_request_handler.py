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
    matchday = current_matchday if args.matchday is None else args.matchday

    table_list_job_queue = []

    if args.first_round:
        table_list_job_queue.append(create_first_round_job(league, current_matchday))

    if args.second_round:
        table_list_job_queue.append(create_second_round_job(league, current_matchday))

    if args.last:
        table_list_job_queue.append(
            create_last_job(args.last, league, current_matchday)
        )

    if args.since:
        table_list_job_queue.append(
            create_since_job(args.since, league, current_matchday)
        )

    if args.home:
        table_list_job_queue.append(create_home_job(league, current_matchday))

    if args.away:
        table_list_job_queue.append(create_away_job(league, current_matchday))

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
        # table_list = handle_table(
        #     all_fixtures=all_fixtures,
        #     matchday=matchday,
        #     current_matchday=current_matchday,
        # )
        # table_printer.print_table_entries(
        #     title=f"{LEAGUE_NAMES[league]} Table Matchday {matchday}",
        #     table_list=table_list,
        # )
        table_list_job_queue.append(create_matchday_job(league, matchday))

    for job in table_list_job_queue:
        title, selector, calculate = job["title"], job["selector"], job["func"]
        selected_fixtures = select_fixtures(all_fixtures, selector)
        table_list = calculate(selected_fixtures)
        table_printer.print_table_entries(title, table_list, args.highlights)


def create_matchday_job(league: League, matchday: int) -> dict:
    selector = get_matchday_selector(matchday)
    title = f"{LEAGUE_NAMES[league]} Table Matchday {matchday}"
    return {"title": title, "selector": selector, "func": calculate_table}


def create_away_job(league: League, current_matchday: int) -> dict:
    away_selector = get_away_selector(current_matchday)
    title = f"{LEAGUE_NAMES[league]} Away Table"
    return {"title": title, "selector": away_selector, "func": calculate_away_table}


def create_home_job(league: League, current_matchday: int) -> dict:
    home_selector = get_home_selector(current_matchday)
    title = f"{LEAGUE_NAMES[league]} Home Table"
    return {"title": title, "selector": home_selector, "func": calculate_home_table}


def create_since_job(since: int, league: League, current_matchday: int) -> dict:
    since_selector = get_since_selector(since, current_matchday)
    title = f"{LEAGUE_NAMES[league]} Table Since Matchday {since}"
    return {"title": title, "selector": since_selector, "func": calculate_table}


def create_last_job(last: int, league: League, current_matchday: int) -> dict:
    last_selector = get_last_selector(last, current_matchday)
    title = f"{LEAGUE_NAMES[league]} Table Last {last} Matches"
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


def handle_table(
    all_fixtures: list[FixtureEntry],
    matchday: int,
    current_matchday: int,
) -> None:
    # -1 == get current one
    if matchday is None:
        matchday = current_matchday

    # need to calculate the table for the given matchday by myself
    # get all fixtures -> calculate till matchday

    # TODO: Depending on League max matchday may be greater or less than 34
    if matchday < 1 or matchday > 34:
        raise ValueError(f"matchday must be between 1 and 34. You gave {matchday}.")

    selected_fixtures = select_fixtures(all_fixtures, FixtureSelector(to=matchday - 1))

    table_list_prior_matchday = calculate_table(selected_fixtures)

    selected_fixtures = select_fixtures(all_fixtures, FixtureSelector(to=matchday))
    table_list = calculate_table(selected_fixtures)

    if matchday != 1:
        for pl, entry in enumerate(table_list):
            old_pl = index_of(entry=entry, table_list=table_list_prior_matchday)
            if pl == old_pl:
                continue
            elif pl > old_pl:
                entry.direction = -1
            else:
                entry.direction = 1
    return table_list


def get_home_selector(current_matchday: int) -> FixtureSelector:
    return FixtureSelector(to=current_matchday)


def get_away_selector(current_matchday: int) -> FixtureSelector:
    return FixtureSelector(to=current_matchday)


def get_matchday_selector(matchday: int) -> FixtureSelector:
    matchday = min(MAX_MATCHDAY, max(1, matchday))
    return FixtureSelector(to=matchday, include_postponed_matches=False)


def get_last_selector(n: int, current_matchday: int) -> FixtureSelector:
    matchday = current_matchday - n + 1
    if matchday < 1:
        matchday = 1
    return FixtureSelector(from_=matchday, to=current_matchday)


def get_since_selector(since: int, current_matchday: int) -> FixtureSelector:
    if since > current_matchday:
        since = current_matchday

    return FixtureSelector(from_=since, to=current_matchday)


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
