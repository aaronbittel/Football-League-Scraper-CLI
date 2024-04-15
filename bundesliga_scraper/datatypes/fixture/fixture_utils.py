from collections import defaultdict

from bundesliga_scraper.datatypes.fixture import fixture_entry


def split_fixture_into_weekdays(fixtures: list[fixture_entry.FixtureEntry]) -> dict:
    # outer dict: Matchday split into weekdays e.g. Friday, Saturday, Sunday
    # inner dict: Weekday split into kickoff times e.g. (Saturday) 15:30, 18:30
    # inner list: list of fixture entries for each match at the weekday at the kickoff time
    matchday_split = defaultdict(lambda: defaultdict(list))

    for fixture in fixtures:
        matchday_split[fixture.date.date()][fixture.date.strftime(r"%H:%M")].append(
            fixture
        )

    return matchday_split
