import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bundesliga_scraper.datatypes.fixture.fixture_entry import FixtureEntry


def create_table():
    table = Table(
        title="Star Wars Movies",
        pad_edge=False,
        caption_justify="center",
        title_justify="center",
    )

    table.add_column("Released", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

    return table


data = requests.get(
    "https://api.openligadb.de/getmatchdata/bl1/2023/26", timeout=3
).json()

fixtures = [FixtureEntry.from_dict(fixture) for fixture in data]

console = Console()
panel1 = Panel.fit(renderable="\n".join(repr(fixture) for fixture in fixtures[:5]))
panel2 = Panel.fit(renderable="\n".join(repr(fixture) for fixture in fixtures[5:]))

table = create_table()


console.print(table, panel1, panel2)
