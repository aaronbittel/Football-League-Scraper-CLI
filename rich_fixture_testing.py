from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from datetime import datetime
from rich.panel import Panel
from rich.console import Console

fixture_entries: list[FixtureEntry] = []
with open("fixture.txt", "r", encoding="utf-8") as f:
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
                date=datetime.strptime(date, r"%Y-%m-%d %H:%M:%S"),
            )
        )

output = ""
current_date = datetime.today()


def get_fixture_string(fixture):
    if fixture.match_is_finished:
        return f"{fixture.home_team:>30}{fixture.home_goals:>3}:{fixture.away_goals:<3}{fixture.away_team}\n"
    else:
        return f"{fixture.home_team:>30} - : - {fixture.away_team}\n"


for fixture in fixture_entries:
    date = fixture.date
    if date != current_date:
        current_date = date
        output += "\n" + date.strftime(r"%Y-%m-%d %H:%M:%S") + "\n"
    get_fixture_string(fixture)
else:
    output = output[1:-1]
Console().print(Panel(renderable=output, title="Fixture Matchday 24", expand=False))


def get_max_width(entries):
    # Example logic, replace with your actual calculation
    max_width = 0
    for entry in entries:
        current_width = len(get_fixture_string(entry))
        max_width = max(max_width, current_width)
    return max_width + 20


max_width = get_max_width(fixture_entries)
print(max_width)

output = f"{fixture_entries[0].date.hour}:{fixture_entries[0].date.minute}\n"
output += get_fixture_string(fixture_entries[0])
output = output[:-1]
Console().print(
    Panel(
        renderable=output,
        # expand=False,
        title=fixture_entries[0].date.strftime("%d.%m.%Y, %A"),
        width=max_width,
    )
)

output = f"{fixture_entries[1].date.hour}:{fixture_entries[1].date.minute}\n"
output += "".join(get_fixture_string(fixture) for fixture in fixture_entries[1:5])
output += f"\n{fixture_entries[5].date.hour}:{fixture_entries[5].date.minute}\n"
output += "".join(get_fixture_string(fixture) for fixture in fixture_entries[5:6])
output = output[:-1]
Console().print(
    Panel(
        renderable=output,
        # expand=False,
        title=fixture_entries[1].date.strftime("%d.%m.%Y, %A"),
        width=max_width,
    )
)
