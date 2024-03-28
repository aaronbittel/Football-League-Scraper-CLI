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
