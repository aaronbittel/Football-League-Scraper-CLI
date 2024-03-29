<<<<<<< HEAD
import requests
=======
from datetime import datetime
>>>>>>> aecddceae48e985d3fc1d997cfeea7f823517ded
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns

from bundesliga_scraper.data_printer.fixture_printer import (
<<<<<<< HEAD
    LOSING_STYLE,
    LOSING_STYLE_END,
    MATCH_SEPERATOR,
    NEUTRAL_STYLE,
    NEUTRAL_STYLE_END,
    WINNING_STYLE,
    WINNING_STYLE_END,
=======
    FUTURE_GAME_SPACE,
    FUTURE_MATCH_SEPERATOR,
    LOSING_STYLE,
    LOSING_STYLE_END,
    MATCH_SEPERATOR,
    WIDTH,
    WINNING_STYLE,
    WINNING_STYLE_END,
    get_fixture_string,
    get_home_team_styled_string,
    print_title,
>>>>>>> aecddceae48e985d3fc1d997cfeea7f823517ded
)
from bundesliga_scraper.data_printer.table_printer import add_rows, create_table
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
<<<<<<< HEAD
from bundesliga_scraper.datatypes.table_entry import TableEntry
from bundesliga_scraper.datatypes.team import TeamSeasonMatches
=======
from bundesliga_scraper.datatypes.team import TeamSeasonMatches
from rich.layout import Layout
>>>>>>> aecddceae48e985d3fc1d997cfeea7f823517ded


def print_team_entries(title: str, selected_team_matches: TeamSeasonMatches) -> None:
    console = Console()
    layout = create_layout()

    print(selected_team_matches)

    results_panel_content = get_results_string(selected_team_matches)

<<<<<<< HEAD
    # print(max(len(content) for content in results_panel_content.split("\n\n")))
=======
    result_panel_content = get_results_string(selected_team_matches)
    layout["Results"].update(
        Panel(renderable=result_panel_content, title="Results", padding=1)
    )

    console.print(layout)
>>>>>>> aecddceae48e985d3fc1d997cfeea7f823517ded

    result_panel = Panel(renderable=results_panel_content, title="Results", padding=1)

<<<<<<< HEAD
    fixtures_panel_content = get_fixtures_string(selected_team_matches)
    fixture_panel = Panel(
        renderable=fixtures_panel_content, title="Fixtures", padding=1
    )

    table = do_table(selected_team_matches.team_name)

    height_diff = results_panel_content.count("\n") - fixtures_panel_content.count("\n")
    if height_diff > 0:
        fixture_panel.renderable += "\n" * height_diff
    else:
        result_panel.renderable += "\n" * abs(height_diff)

    columns = Columns([result_panel, fixture_panel])

    console.print(title, justify="center")
    console.print(table, justify="center")
    console.print(columns, justify="center")


def do_table(team_name: str):
    table_data = requests.get(
        "https://api.openligadb.de/getbltable/bl1/2023", timeout=3
    ).json()
    table_entries = [TableEntry.from_dict(entry) for entry in table_data]
    table_entries.sort(reverse=True)

    placement = 0
    for idx, entry in enumerate(table_entries, start=1):
        if team_name in entry.team_name:
            placement = idx

    table = create_table(title="", last_5=False)
    add_rows(table, table_entries, highlights=[team_name], place=placement)
    return table


def get_results_string(selected_team_matches: TeamSeasonMatches) -> str:
    max_home_length = max(
        len(result.home_team) for result in selected_team_matches.results
    )

    max_away_length = max(
        len(result.away_team) for result in selected_team_matches.results
    )

    return "\n\n".join(
        get_result_string(
            selected_team_matches, result, max_home_length, max_away_length
        )
        for result in selected_team_matches.results
    )


def get_style(
    selected_team_matches: TeamSeasonMatches, result: FixtureEntry
) -> tuple[str, str]:
    if selected_team_matches.team_won_match(result):
        return WINNING_STYLE, WINNING_STYLE_END
    elif selected_team_matches.team_lost_match(result):
        return LOSING_STYLE, LOSING_STYLE_END
    return NEUTRAL_STYLE, NEUTRAL_STYLE_END


def get_result_string(
    selected_team_matches: TeamSeasonMatches,
    result: FixtureEntry,
    max_length: int,
    max_away_length: int,
) -> str:
    style_open, style_closing = get_style(selected_team_matches, result)

    home_goal_string = f"[o u]| {result.home_goals} |[/]"
    away_goal_string = f"[o u]| {result.away_goals} |[/]"

    if selected_team_matches.team_name in result.home_team:
        return f"{style_open}{result.home_team.rjust(max_length)} {home_goal_string}{style_closing}{MATCH_SEPERATOR}{away_goal_string} {result.away_team.ljust(max_away_length)} ({result.matchday})"
    return f"{result.home_team.rjust(max_length)} {home_goal_string}{MATCH_SEPERATOR}{style_open}{away_goal_string} {result.away_team.ljust(max_away_length)}{style_closing} ({result.matchday})"


def get_fixtures_string(selected_team_matches: TeamSeasonMatches) -> str:
    max_home_length = max(
        len(fixture.home_team) for fixture in selected_team_matches.fixtures
    )

    max_away_length = max(
        len(fixture.away_team) for fixture in selected_team_matches.fixtures
    )
    return "\n\n".join(
        get_fixture_string(
            selected_team_matches.team_name, fixture, max_home_length, max_away_length
        )
        for fixture in selected_team_matches.fixtures
    )


def get_fixture_string(
    team_name: str, fixture: FixtureEntry, max_length: int, max_away_length: int
) -> str:
    match_seperator = " [u o]| - |[/] : [u o]| - |[/] "

    if team_name in fixture.home_team:
        return f"{NEUTRAL_STYLE}{fixture.home_team.rjust(max_length)}{NEUTRAL_STYLE_END}{match_seperator}{fixture.away_team.ljust(max_away_length)} ({fixture.matchday})"
    return f"{fixture.home_team.rjust(max_length)}{match_seperator}{NEUTRAL_STYLE}{fixture.away_team.ljust(max_away_length)}{NEUTRAL_STYLE_END} ({fixture.matchday})"
=======
# def get_fixture_string() -> str:
#     if fixture.is_in_future:
#         return f"{fixture.home_team.rjust(FUTURE_GAME_SPACE)}{FUTURE_MATCH_SEPERATOR}{fixture.away_team.ljust(FUTURE_GAME_SPACE)}"

#     style = get_style(team_name, fixture)


# def get_style(team_name: str, fixture: FixtureEntry) -> str:
#     if

# def get_team_styled_string(fixure: FixtureEntry) -> str:
#     pass


def get_results_string(selected_team_matches: TeamSeasonMatches) -> str:
    return "\n".join(
        get_result_string(selected_team_matches, result)
        for result in selected_team_matches.results
    )


def get_style(
    selected_team_matches: TeamSeasonMatches, result: FixtureEntry
) -> tuple[str, str]:
    if selected_team_matches.team_won_match(result):
        return WINNING_STYLE, WINNING_STYLE_END
    elif selected_team_matches.team_lost_match(result):
        return LOSING_STYLE, LOSING_STYLE_END
    return "", ""


def get_result_string(
    selected_team_matches: TeamSeasonMatches, result: FixtureEntry
) -> str:
    style_open, style_closing = get_style(selected_team_matches, result)

    if selected_team_matches.team_name == result.home_team:
        match_string = f"{style_open}{result.home_team} {result.home_goals}{style_closing}{MATCH_SEPERATOR}{result.away_goals} {result.away_team}"
    else:
        match_string = f"{result.home_team} {result.home_goals}{MATCH_SEPERATOR}{style_open}{result.away_goals} {result.away_team}{style_closing}"
    return match_string


def create_layout() -> Layout:
    layout = Layout()

    layout.split_column(Layout(name="Table"), Layout(name="lower"))

    layout["lower"].split_row(
        Layout(name="Results"),
        Layout(name="Fixtures"),
    )

    return layout
>>>>>>> aecddceae48e985d3fc1d997cfeea7f823517ded
