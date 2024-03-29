from dataclasses import dataclass, field

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry


@dataclass
class TeamSeasonMatches:
    team_name: str
    results: list[FixtureEntry] = field(default_factory=list)
    fixtures: list[FixtureEntry] = field(default_factory=list)

    def team_won_match(self, fixture: FixtureEntry) -> bool:
        self.check_valid_fixture(fixture)

        if self.team_name in fixture.home_team and fixture.home_team_won():
            return True
        if self.team_name in fixture.away_team and fixture.away_team_won():
            return True
        return False

    def team_lost_match(self, fixture: FixtureEntry) -> bool:
        self.check_valid_fixture(fixture)
        if self.team_name in fixture.home_team and fixture.away_team_won():
            return True
        if self.team_name in fixture.away_team and fixture.home_team_won():
            return True
        return False

    def check_valid_fixture(self, fixture):
        if (
            self.team_name not in fixture.home_team
            and self.team_name not in fixture.away_team
        ):
            raise ValueError(f"{self.team_name} not in fixture {fixture}")
