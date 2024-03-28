from datetime import datetime
from rich.console import Console
from rich.panel import Panel

from bundesliga_scraper.data_printer.fixture_printer import (
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
)
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.team import TeamSeasonMatches
from rich.layout import Layout


def print_team_entries(title: str, selected_team_matches: TeamSeasonMatches) -> None:
    console = Console()
    layout = create_layout()

    print(selected_team_matches)

    print_title(console, title)

    result_panel_content = get_results_string(selected_team_matches)
    layout["Results"].update(
        Panel(renderable=result_panel_content, title="Results", padding=1)
    )

    console.print(layout)


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
