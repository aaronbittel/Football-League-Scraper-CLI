"""Creating colorful strings of matchday fixture information."""

from typing import Generator
from rich import panel
from bundesliga_scraper.datatypes.fixture import fixture_utils

from bundesliga_scraper.datatypes.fixture import fixture_entry

WINNING_STYLE = "[bold pale_green3]"
WINNING_STYLE_END = f"[/{WINNING_STYLE[1:]}"
LOSING_STYLE = "[bold red]"
LOSING_STYLE_END = f"[/{LOSING_STYLE[1:]}"
NEUTRAL_STYLE = "[bold pale_turquoise4]"
NEUTRAL_STYLE_END = f"[/{NEUTRAL_STYLE[1:]}"
HIGHLIGHT_STYLE = "[on orange3]"
HIGHLIGHT_STYLE_END = f"[/{HIGHLIGHT_STYLE[1:]}"

WIDTH = 62
MATCH_SEPERATOR = " : "
FUTURE_MATCH_SEPERATOR = " - : - "
NAME_SPACE = (WIDTH - len(MATCH_SEPERATOR)) // 2
FUTURE_GAME_SPACE = (WIDTH - len(FUTURE_MATCH_SEPERATOR)) // 2


def get_fixture_string(
    fixture: fixture_entry.FixtureEntry, highlights: list[str]
) -> str:
    if fixture.match_is_finished or fixture.match_is_live:
        home_string = get_home_team_styled_string(fixture)
        away_string = get_away_team_styled_string(fixture)
        match_string = f"{home_string}{MATCH_SEPERATOR}{away_string}"
    else:
        match_string = f"{fixture.home_team.rjust(FUTURE_GAME_SPACE)}{FUTURE_MATCH_SEPERATOR}{fixture.away_team.ljust(FUTURE_GAME_SPACE)}"

    if any(
        highlight.lower() in fixture.home_team.lower()
        or highlight.lower() in fixture.away_team.lower()
        for highlight in highlights
    ):
        return f"{HIGHLIGHT_STYLE}{match_string}{HIGHLIGHT_STYLE_END}"

    return match_string


def create_fixture_panels(
    fixtures: list[fixture_entry.FixtureEntry], highlights: list[str]
) -> Generator[panel.Panel, None, None]:
    matchday_weekdays_split = fixture_utils.split_fixture_into_weekdays(fixtures)

    for weekday_date, kickoff_times in matchday_weekdays_split.items():
        panel_content = get_panel_content(highlights, kickoff_times)

        yield panel.Panel(
            renderable=panel_content,
            title=weekday_date.strftime(r"%d.%m.%Y, %A"),
            width=WIDTH,
            padding=1,
        )


def get_panel_content(
    highlights: list[str], kickoff_times: dict[str, list[fixture_entry.FixtureEntry]]
) -> str:
    panel_content = ""
    for kickoff_time, fixtures in kickoff_times.items():
        panel_content += f"{kickoff_time}\n"
        is_live = any(fixture.match_is_live for fixture in fixtures)
        if is_live:
            panel_content = panel_content[:-1] + 45 * " " + "🔴 LIVE\n"
        panel_content += "\n".join(
            get_fixture_string(fixture, highlights) for fixture in fixtures
        )

    return panel_content


def get_home_string(fixture: fixture_entry.FixtureEntry) -> str:
    return f"{fixture.home_team} {fixture.home_goals}"


def get_away_string(fixture: fixture_entry.FixtureEntry) -> str:
    return f"{fixture.away_goals} {fixture.away_team}"


def get_home_team_styled_string(fixture: fixture_entry.FixtureEntry) -> str:
    home_string = f"{get_home_string(fixture).rjust(NAME_SPACE)}"
    if fixture.home_team_won():
        return f"{WINNING_STYLE}{home_string}{WINNING_STYLE_END}"
    else:
        return home_string


def get_away_team_styled_string(fixture: fixture_entry.FixtureEntry) -> str:
    away_string = f"{get_away_string(fixture).ljust(NAME_SPACE)}"
    if fixture.away_team_won():
        return f"{WINNING_STYLE}{away_string}{WINNING_STYLE_END}"
    else:
        return away_string
