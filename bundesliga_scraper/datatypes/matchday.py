from collections import defaultdict
from dataclasses import dataclass, field

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry


@dataclass
class Matchday:
    matchday: int
    fixtures: list[FixtureEntry] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Matchday {self.matchday}\n" + "\n".join(
            repr(fixture) for fixture in self.fixtures
        )

    def split_fixture_into_weekdays(self) -> dict:
        # outer dict: Matchday split into weekdays e.g. Friday, Saturday, Sunday
        # inner dict: Weekday split into kickoff times e.g. (Saturday) 15:30, 18:30
        # inner list: list of fixture entries for each match at the weekday at the kickoff time
        matchday_split = defaultdict(lambda: defaultdict(list))

        for fixture in self.fixtures:
            matchday_split[fixture.date.date()][fixture.date.strftime(r"%H:%M")].append(
                fixture
            )

        return matchday_split
