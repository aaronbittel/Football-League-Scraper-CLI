<<<<<<< HEAD
from rich.layout import Layout
from rich.panel import Panel

from rich.console import Console

from bundesliga_scraper.api.api import retrieve_team_match_data
from bundesliga_scraper.datatypes.constants import League

console = Console()

layout = Layout()
layout.split_column(
    Layout(name="0"),
    Layout(name="1"),
    Layout(name="2"),
    Layout(name="3"),
    Layout(name="4"),
)


fixtures = retrieve_team_match_data(League.Bundesliga, team="Augsburg")

max_home_length = max(len(fixture.home_team) for fixture in fixtures[-12:-7])
max_away_length = max(len(fixture.away_team) for fixture in fixtures[-12:-7])

for idx, fixture in enumerate(fixtures[-12:-7]):
    home_team = fixture.home_team
    away_team = fixture.away_team

    layout[str(idx)].split_row(
        Layout(name="home_team", size=max_home_length + 4),
        Layout(name="home_goals", size=5),
        Layout(name="seperator", size=5),
        Layout(name="away_goals", size=5),
        Layout(name="away_team", size=max_away_length + 4),
    )

    layout[str(idx)]["home_team"].update(
        Panel.fit(home_team.ljust(max_home_length), height=3)
    )
    layout[str(idx)]["home_goals"].update(Panel.fit(str(fixture.home_goals), height=3))
    layout[str(idx)]["seperator"].update(Panel.fit(":", height=3))
    layout[str(idx)]["away_goals"].update(Panel.fit(str(fixture.away_goals), height=3))
    layout[str(idx)]["away_team"].update(
        Panel.fit(away_team.ljust(max_away_length), height=3)
    )
console.print(Panel(layout, width=65), height=17)
=======
from datetime import datetime
from rich.layout import Layout
from rich.panel import Panel

# from rich import print
from rich.console import Console

from bundesliga_scraper.data_printer.fixture_printer import get_fixture_string
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry

console = Console()
layout = Layout()


layout.split_column(Layout(name="Table"), Layout(name="lower"))

layout["lower"].split_row(
    Layout(name="Results"),
    Layout(name="Fixtures"),
)

fixture_entry = FixtureEntry(
    home_team="FC Augsburg",
    home_goals=3,
    away_team="1. FC Heidenheim 1848",
    away_goals=1,
    matchday=27,
    match_is_finished=True,
    match_is_live=False,
    date=datetime(year=2024, month=1, day=1, hour=18, minute=30),
)

layout["Results"].update(
    Panel(
        renderable=f"{get_fixture_string(fixture_entry, highlights=[])}({fixture_entry.matchday})",
        title="Results",
        padding=1,
    )
)
console.print(layout)
>>>>>>> aecddceae48e985d3fc1d997cfeea7f823517ded
