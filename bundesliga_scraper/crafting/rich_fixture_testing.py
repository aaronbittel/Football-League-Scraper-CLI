from collections import defaultdict
from datetime import datetime

from rich.console import Console
from rich.panel import Panel

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry

from pathlib import Path

fixture_entries: list[FixtureEntry] = []
with open(
    Path() / "bundesliga_scraper" / "crafting" / "fixture.txt", "r", encoding="utf-8"
) as f:
    for line in f.readlines():
        line = line.replace("\n", "")
        home, away, h_goals, a_goals, matchday, is_finished, date = line.split("$")
        fixture_entries.append(
            FixtureEntry(
                home_team=home,
                away_team=away,
                home_goals=int(h_goals),
                away_goals=int(a_goals),
                matchday=int(matchday),
                match_is_finished=bool(is_finished),
                match_is_live=False,
                date=datetime.strptime(date, r"%Y-%m-%d %H:%M:%S"),
            )
        )


def get_fixture_string(fixture):
    if fixture.match_is_finished:
        return f"{fixture.home_team:>30}{fixture.home_goals:>3}:{fixture.away_goals:<3}{fixture.away_team}\n"
    else:
        return f"{fixture.home_team:>30} - : - {fixture.away_team}\n"


max_width = 67
matchday_split = defaultdict(list)

for fixture in fixture_entries:
    matchday_split[fixture.date.strftime(r"%d.%m.%Y, %A")].append(fixture)

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
            width=max_width,
            padding=1,
        )
    )
