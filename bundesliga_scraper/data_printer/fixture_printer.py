"""Creating colorful strings of matchday fixture information."""

from collections import defaultdict
from datetime import datetime

from rich.console import Console
from rich.panel import Panel

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry

MAX_WIDTH = 67


def get_fixture_string(fixture: FixtureEntry):
    # TODO Check if game is live and display its live score
    if fixture.match_is_finished:
        return f"{fixture.home_team:>30}{fixture.home_goals:>3}:{fixture.away_goals:<3}{fixture.away_team}\n"
    else:
        return f"{fixture.home_team:>30} - : - {fixture.away_team}\n"


def print_fixture_entries(fixture_entries: list[FixtureEntry]) -> None:
    matchday_split = split_matchday_into_weekdays(fixture_entries)

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
