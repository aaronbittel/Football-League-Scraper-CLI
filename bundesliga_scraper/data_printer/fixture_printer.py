"""Creating colorful strings of matchday fixture information."""

from collections import defaultdict
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry

WINNING_STYLE = "[bold pale_green3]"
WINNING_STYLE_END = f"[/{WINNING_STYLE[1:]}"
HIGHLIGHT_STYLE = "[on orange3]"
HIGHLIGHT_STYLE_END = f"[/{HIGHLIGHT_STYLE[1:]}"

WIDTH = 62
MATCH_SEPERATOR = " : "
FUTURE_MATCH_SEPERATOR = " - : - "
NAME_SPACE = (WIDTH - len(MATCH_SEPERATOR)) // 2
NAME_SPACE_2 = (WIDTH - len(FUTURE_MATCH_SEPERATOR)) // 2


def get_fixture_text(fixture: FixtureEntry, highlights: list[str]) -> str:
    if fixture.match_is_finished or fixture.match_is_live:
        home_string = get_home_team_styled_string(fixture)
        away_string = get_away_team_styled_string(fixture)
        match_string = f"{home_string}{MATCH_SEPERATOR}{away_string}"
    else:
        match_string = f"{fixture.home_team.rjust(NAME_SPACE_2)}{FUTURE_MATCH_SEPERATOR}{fixture.away_team.ljust(NAME_SPACE_2)}"

    if fixture.home_team in highlights or fixture.away_team in highlights:
        return f"{HIGHLIGHT_STYLE}{match_string}{HIGHLIGHT_STYLE_END}"

    return match_string


def print_fixture_entries(
    title: str, matchday_fixtures: list[FixtureEntry], highlights: list[str]
) -> None:
    console = Console()
    fixture_weekdays_split = split_fixture_into_weekdays(matchday_fixtures)

    print_title(console, title)

    for weekday_date, kickoff_times in fixture_weekdays_split.items():
        panel_content = ""
        for kickoff_time, fixtures in kickoff_times.items():
            panel_content += f"{kickoff_time}\n"
            is_live = any(fixture.match_is_live for fixture in fixtures)
            if is_live:
                panel_content = panel_content[:-1] + 45 * " " + "🔴 LIVE\n"
            panel_content += "\n".join(
                get_fixture_text(fixture, highlights) for fixture in fixtures
            )

        console.print(
            Panel(
                renderable=panel_content,
                title=weekday_date.strftime(r"%d.%m.%Y, %A"),
                width=WIDTH,
                padding=1,
            )
        )


def print_title(console: Console, title: str) -> None:
    leftspace = (WIDTH - len(title)) // 2
    console.print(Text(leftspace * " ") + Text(f"{title}\n", style="bold italic"))


def split_fixture_into_weekdays(
    fixture_entries: list[FixtureEntry],
) -> defaultdict[datetime, list[FixtureEntry]]:
    matchday_split = defaultdict(lambda: defaultdict(list))

    for fixture in fixture_entries:
        matchday_split[fixture.date.date()][fixture.date.strftime(r"%H:%M")].append(
            fixture
        )

    return matchday_split


def get_home_string(fixture: FixtureEntry) -> str:
    return f"{fixture.home_team} {fixture.home_goals}"


def get_away_string(fixture: FixtureEntry) -> str:
    return f"{fixture.away_goals} {fixture.away_team}"


def get_home_team_styled_string(fixture: FixtureEntry) -> str:
    home_string = f"{get_home_string(fixture).rjust(NAME_SPACE)}"
    if fixture.home_team_won():
        return f"{WINNING_STYLE}{home_string}{WINNING_STYLE_END}"
    else:
        return home_string


def get_away_team_styled_string(fixture: FixtureEntry) -> str:
    away_string = f"{get_away_string(fixture).ljust(NAME_SPACE)}"
    if fixture.away_team_won():
        return f"{WINNING_STYLE}{away_string}{WINNING_STYLE_END}"
    else:
        return away_string
