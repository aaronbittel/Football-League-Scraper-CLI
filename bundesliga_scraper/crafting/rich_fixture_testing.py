from collections import defaultdict
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.rule import Rule
from rich.table import Table

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry

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


console = Console()


# max_length = max((len(repr(fixture)) for fixture in fixture_entries))

# content = "\n".join(
#     (fixture.get_rich_string()).ljust(max_length) for fixture in fixture_entries
# )

max_home_length = max(len(fixture.home_team) for fixture in fixture_entries)
max_away_length = max(len(fixture.away_team) for fixture in fixture_entries)


table = Table.grid()
table.add_column("Home Team", justify="right")
table.add_column("Home Goals", justify="center")
table.add_column(":", justify="center")
table.add_column("Away Goals", justify="center")
table.add_column("Away Team", justify="left")
for fixture in fixture_entries:
    table.add_row(
        fixture.home_team.rjust(max_home_length),
        str(fixture.home_goals) + "  ",
        ":" + " ",
        str(fixture.away_goals) + " ",
        fixture.away_team.ljust(max_away_length),
    )

table.show_header = False

# content[-1] = content[-1] + "\t"

# print(list(entry.index(":") for entry in content))

# content = Text("")
# content += Text("alösjdfaölsfj : aösldkfj.-" + "\n")
# content += Text("     öasdjfas : asldfjdfaö")
# content.highlight_words(["sl"], style="red on green", case_sensitive=True)

# print(list(e.index(":") for e in content.split("\n")))
# console.print(
#     Panel(
#         renderable="\n".join(content),
#         width=max_home_length + max_away_length + 40,
#     ),
#     justify="center",
# )

console.print(Panel(table, title="10.03.2024, Sunday", padding=1), justify="center")

console.print(Rule(title="This is a Rule"))
