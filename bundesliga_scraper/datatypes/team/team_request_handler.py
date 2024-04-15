import argparse
from re import A
from turtle import st

from rich import console as con, columns as cols

from bundesliga_scraper.api import api
from bundesliga_scraper.datatypes.fixture import fixture_entry
from bundesliga_scraper.datatypes import utils
from bundesliga_scraper.datatypes.team import team_parser
from bundesliga_scraper.datatypes.table import (
    table_parser,
    table_calculator,
    table_creation,
)
from bundesliga_scraper.datatypes.team.team_creation import create_team_components

TITLE_TEMPLATE = "{} Fixtures & Results"


def handle_team_request(args: argparse.Namespace) -> None:
    team_name: str = args.team_name[0]

    league = utils.get_league(args.league)

    team_fixture_entries = api.retrieve_team_match_data(
        league=league, team=team_name.capitalize()
    )
    last_played_matchday_index = get_last_played_matchday_index(team_fixture_entries)
    title = TITLE_TEMPLATE.format(team_name)

    season_fixtures = api.retrieve_all_matchdays(league)
    current_matchday = api.retrieve_current_matchday(league)
    matchday_selector = table_parser.MatchdaySelector(to=current_matchday)
    standings = table_calculator.calculate(season_fixtures, matchday_selector)

    focus = 0
    for pl, team in enumerate(standings, start=1):
        if team_name in team.team_name:
            focus = pl
            break

    table_creation_job = table_creation.TableCreationJob(
        title, standings, highlights=[], focus=focus
    )
    rich_table = table_creation.create_table(table_creation_job)

    from_, to = team_parser.parse(args, last_played_matchday_index)

    result_fixtures: list[fixture_entry.FixtureEntry] = team_fixture_entries[
        from_ : last_played_matchday_index + 1
    ]
    future_fixtures: list[fixture_entry.FixtureEntry] = team_fixture_entries[
        last_played_matchday_index + 1 : to
    ]

    result_panel, fixture_panel = create_team_components(
        team_name, result_fixtures, future_fixtures
    )

    columns = cols.Columns([result_panel, fixture_panel])
    console = con.Console()
    console.print(rich_table, justify="center")
    console.print(columns)


def get_last_played_matchday_index(
    team_fixture_entries: list[fixture_entry.FixtureEntry],
) -> int:
    for i, fixture in enumerate(team_fixture_entries):
        if not fixture.match_is_finished:
            return i
    return 0
