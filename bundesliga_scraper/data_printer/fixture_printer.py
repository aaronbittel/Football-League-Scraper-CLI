"""Creating colorful strings of matchday fixture information."""

from collections import defaultdict
from datetime import datetime

from rich.console import Console
from rich.panel import Panel

from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES, League
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry

MAX_WIDTH = 67
WINNING_STYLE = "[bold pale_green3]"
END_WINNING_STYLE = "[/bold pale_green3]"


def get_fixture_string(fixture: FixtureEntry):
    # TODO Check if game is live and display its live score
    if fixture.match_is_finished or fixture.match_is_live:
        home_string = get_home_team_string(fixture)
        away_string = get_away_team_string(fixture)
        return f"{home_string} : {away_string}\n"
    else:
        return f"{fixture.home_team:>30} - : - {fixture.away_team}\n"


def print_fixture_entries(
    league: League, matchday_fixtures: list[FixtureEntry]
) -> None:
    matchday_split = split_matchday_into_weekdays(matchday_fixtures)

    print(f"{LEAGUE_NAMES[league]} Fixture {matchday_fixtures[0].matchday}")

    for date, fixture_list in matchday_split.items():
        output = ""
        current_time = datetime.today()
        for fixture in fixture_list:
            if not (
                current_time.hour == fixture.date.hour
                and current_time.minute == fixture.date.minute
            ):
                output += fixture.date.strftime(r"%H:%M") + "\n"
                current_time = fixture.date
                if fixture.match_is_live:
                    output = output[:-1]
                    # output += " " * 50 + "[blink]🔴 LIVE[/blink]\n"
                    output += " " * 50 + "🔴 LIVE\n"
            output += get_fixture_string(fixture)
        output = output[:-1]
        Console().print(
            Panel(
                renderable=output,
                title=date,
                width=MAX_WIDTH,
                padding=1,
            )
        )


def split_matchday_into_weekdays(
    fixture_entries: list[FixtureEntry],
) -> defaultdict[str, list[FixtureEntry]]:
    matchday_split = defaultdict(list)
    for fixture in fixture_entries:
        matchday_split[fixture.date.strftime(r"%d.%m.%Y, %A")].append(fixture)
    return matchday_split


def home_string(fixture: FixtureEntry) -> str:
    return f"{fixture.home_team:>30}{fixture.home_goals:>3}"


def away_string(fixture: FixtureEntry) -> str:
    return f"{fixture.away_goals:<3}{fixture.away_team}"


def get_home_team_string(fixture: FixtureEntry) -> str:
    return (
        f"{WINNING_STYLE}{home_string(fixture)}{END_WINNING_STYLE}"
        if fixture.home_team_won()
        else home_string(fixture)
    )


def get_away_team_string(fixture: FixtureEntry) -> str:
    return (
        f"{WINNING_STYLE}{away_string(fixture)}{END_WINNING_STYLE}"
        if fixture.away_team_won()
        else away_string(fixture)
    )
