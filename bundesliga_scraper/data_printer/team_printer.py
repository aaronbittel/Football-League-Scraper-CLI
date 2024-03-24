from rich.console import Console
from rich.panel import Panel

from bundesliga_scraper.data_printer.fixture_printer import (
    FUTURE_GAME_SPACE,
    FUTURE_MATCH_SEPERATOR,
    MATCH_SEPERATOR,
    WIDTH,
    get_away_team_styled_string,
    get_home_team_styled_string,
    print_title,
)
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.matchday import Matchday


def print_team_entries(title: str, matches: Matchday) -> None:
    console = Console()

    print_title(console, title)

    for fixture in matches.fixtures:
        console.print(
            Panel(
                renderable=get_fixture_string(fixture),
                title=fixture.date.strftime(r"%d.%m.%Y, %A, %H:%M"),
                width=WIDTH,
                padding=1,
            )
        )


def get_fixture_string(fixture: FixtureEntry) -> str:
    if fixture.match_is_finished or fixture.match_is_live:
        home_string = get_home_team_styled_string(fixture)
        away_string = get_away_team_styled_string(fixture)
        match_string = f"{home_string}{MATCH_SEPERATOR}{away_string}"
    else:
        match_string = f"{fixture.home_team.rjust(FUTURE_GAME_SPACE)}{FUTURE_MATCH_SEPERATOR}{fixture.away_team.ljust(FUTURE_GAME_SPACE)}"

    return match_string
