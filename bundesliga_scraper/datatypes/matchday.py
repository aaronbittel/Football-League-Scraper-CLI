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
