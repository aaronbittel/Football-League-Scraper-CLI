import copy

from rich import console as con
from rich import layout as lay

from bundesliga_scraper.api import api
from bundesliga_scraper.datatypes import constants
from bundesliga_scraper.datatypes.fixture import fixture_creation, fixture_entry
from bundesliga_scraper.datatypes.table import table_creation, table_entry, table_parser


class League:
    def __init__(self, league: constants.League) -> None:
        self.short_name = league
        self.name = league.name
        self.all_fixtures = api.retrieve_all_matchdays(league)
        self.teams = self._initalize_teams()
        self.current_matchday = api.retrieve_current_matchday(league)
        self.active_matchday = self._calculate_active_matchday()

    def _initalize_teams(self) -> dict[str, table_entry.TableEntry]:
        teams = {}
        for fixture in self.all_fixtures[0]:
            teams[fixture.home_team] = table_entry.TableEntry(
                team_name=fixture.home_team
            )
            teams[fixture.away_team] = table_entry.TableEntry(
                team_name=fixture.away_team
            )
        return teams

    def _calculate_active_matchday(self) -> int:
        if all(
            fixture.match_is_in_future()
            for fixture in self.all_fixtures[self.current_matchday - 1]
        ):
            return self.current_matchday - 1
        return self.current_matchday

    def calculate_table(
        self, matchday_selector: table_parser.MatchdaySelector
    ) -> list[table_entry.TableEntry]:
        table = copy.deepcopy(self.teams)

        matchdays = self.all_fixtures[
            matchday_selector.from_ - 1 : matchday_selector.to
        ]

        standings: list[table_entry.TableEntry] = []

        for matchday_fixtures in matchdays:
            for fixture in matchday_fixtures:
                if fixture.match_is_in_future():
                    continue
                if matchday_selector.home:
                    table[fixture.home_team].update(fixture)
                if matchday_selector.away:
                    table[fixture.away_team].update(fixture)
            standings = sorted(table.values(), reverse=True)
            for pl, team in enumerate(standings, start=1):
                team.history.placements.append(pl)

        return standings

    def get_fixture(self, matchday: int) -> list[fixture_entry.FixtureEntry]:
        return self.all_fixtures[matchday - 1]


if __name__ == "__main__":
    l = League(constants.League.Bundesliga)
    matchday_selector = table_parser.MatchdaySelector(to=30)

    standings = l.calculate_table(matchday_selector)
    table_job = table_creation.TableCreationJob(title="", standings=standings)
    table = table_creation.create_table(table_job)
    console = con.Console()

    fixtures = l.get_fixture(matchday=30)
    fixture_panels = []
    for panel in fixture_creation.create_fixture_panels(fixtures, highlights=[]):
        fixture_panels.append(panel)
    fixture_panel_group = con.Group(*fixture_panels)

    layout = lay.Layout()
    layout.split_row(
        lay.Layout(name="left", size=70),
        lay.Layout(name="right"),
    )

    layout["left"].update(fixture_panel_group)
    layout["right"].update(table)
    console.print("Bundesliga Matchday 30", justify="center")
    console.print(layout)
