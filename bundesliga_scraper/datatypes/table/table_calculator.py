from bundesliga_scraper.datatypes.fixture import fixture_entry
from bundesliga_scraper.datatypes.table import table_entry, table_parser


def calculate(
    all_matchdays: list[list[fixture_entry.FixtureEntry]],
    matchday_selector: table_parser.MatchdaySelector,
) -> list[table_entry.TableEntry]:
    table: dict[str, table_entry.TableEntry] = {}

    for fixture in all_matchdays[1]:
        table[fixture.home_team] = table_entry.TableEntry(fixture.home_team)
        table[fixture.away_team] = table_entry.TableEntry(fixture.away_team)

    matchdays = all_matchdays[matchday_selector.from_ - 1 : matchday_selector.to]

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
