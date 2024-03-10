"""Handles request of Football table."""

from __future__ import annotations

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.table_entry import TableEntry
from bundesliga_scraper.data_printer import table_printer
from bundesliga_scraper.api import api
from itertools import chain


def handle_table_request(user_args: dict[str, str | int]) -> None:
    """Handles the table request.

    Args:
        user_args (dict[str, str  |  int]): user arguments
    """
    league = (
        api.League.Bundesliga
        if user_args["league"].lower() == "bundesliga"
        else api.League.Bundesliga_2
    )
    matchday = user_args["table"]

    current_matchday = api.retrieve_current_matchday(league=league)

    # -1 == get current one
    if matchday == -1:
        matchday = current_matchday

    # need to calculate the table for the given matchday by myself
    # get all fixtures -> calculate till matchday

    # TODO: Depending on League max matchday may be greater or less than 34
    if matchday < 1 or matchday > 34:
        raise ValueError(f"matchday must be between 1 and 34. You gave {matchday}.")

    all_fixtures = api.retrieve_all_fixtures(league=league)

    table_list_prior_matchday = calculate_table_entries(
        all_fixtures, matchday=matchday - 1
    )

    table_list = calculate_table_entries(all_fixtures, matchday=matchday)

    for pl, entry in enumerate(table_list):
        old_pl = index_of(entry=entry, table_list=table_list_prior_matchday)
        if pl == old_pl:
            continue
        elif pl > old_pl:
            entry.direction = -1
        else:
            entry.direction = 1

    table_printer.print_table_entries(
        league=league, matchday=matchday, table_list=table_list
    )


def calculate_table_entries(
    fixtures: list[FixtureEntry], matchday: int
) -> list[TableEntry]:
    # TODO Somehow use Defaultdict
    table_entries = {}
    for fixture in fixtures[0:9]:
        table_entries[fixture.home_team] = TableEntry(team_name=fixture.home_team)
        table_entries[fixture.away_team] = TableEntry(team_name=fixture.away_team)

    for fixture in fixtures:
        # Based on Kicker.de, if a match has been postponed and was not played on
        # the match day, then it will not be displayed in the table for the match day
        # This means that if games are canceled, games from the following match day
        # would be included and this will be prevented
        if fixture.matchday > matchday:
            break

        if not fixture.match_is_finished and not fixture.match_is_live:
            break

        table_entries[fixture.home_team].update(fixture)
        table_entries[fixture.away_team].update(fixture)

    table_list = list(table_entries.values())
    table_list.sort(reverse=True)
    return table_list


def index_of(entry: TableEntry, table_list: list[TableEntry]) -> int:
    for i, table_entry in enumerate(table_list):
        if table_entry.team_name == entry.team_name:
            return i
