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

    current_matchday = api.retrieve_current_matchday(league=league) - 1

    # -1 == get current one
    if matchday == -1 or matchday >= current_matchday:
        table_entries = api.retrieve_table(league=league)
        table_printer.print_table_entries(
            league=league, matchday=current_matchday, table_entries=table_entries
        )
        return

    # need to calculate the table for the given matchday by myself
    # get all fixtures -> calculate till matchday

    # TODO: Depending on League max matchday may be greater or less than 34
    if matchday < 1 or matchday > 34:
        raise ValueError(f"matchday must be between 1 and 34. You gave {matchday}.")

    all_fixtures = api.retrieve_all_fixtures(league=league)
    fixtures_till_matchday = select_fixtures_till_matchday(
        all_fixtures, till_matchday=matchday - 1
    )

    table_entries = calculate_table_entries(fixtures_till_matchday, matchday=matchday)
    table_entries.sort(reverse=True)
    table_printer.print_table_entries(
        league=league, matchday=matchday, table_entries=table_entries
    )


def select_fixtures_till_matchday(
    all_fixtures: list[list[FixtureEntry]], till_matchday: int
) -> list[FixtureEntry]:
    return list(chain.from_iterable(all_fixtures[: till_matchday + 1]))


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
        table_entries[fixture.home_team].update(fixture)
        table_entries[fixture.away_team].update(fixture)

    return list(table_entries.values())
