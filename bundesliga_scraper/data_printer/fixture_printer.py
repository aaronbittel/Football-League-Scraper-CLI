"""Creating colorful strings of matchday fixture information."""

from datetime import datetime

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry


def print_fixture_entry(fixture_entry: FixtureEntry) -> None:
    if fixture_entry.match_is_finished:
        print(
            f"{fixture_entry.home_team:>30}{fixture_entry.home_goals:>3}:{fixture_entry.away_goals:<3}{fixture_entry.away_team}"
        )
    else:
        print(f"{fixture_entry.home_team:>30} - : - {fixture_entry.away_team}")


def print_fixture_entries(fixture_entries: list[FixtureEntry]) -> None:
    with open("fixture.txt", "w", encoding="utf-8") as f:
        for fixture in fixture_entries:
            f.write(fixture.__str__() + "\n")
    current_date = datetime.today()
    for fixture in fixture_entries:
        date = fixture.date
        if date != current_date:
            current_date = date
            print(date)
        print_fixture_entry(fixture)
