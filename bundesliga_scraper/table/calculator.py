from bundesliga_scraper.datatypes import matchday as m, table_entry
from bundesliga_scraper.table import parser


def calculate(
    matchdays: list[m.Matchday], matchday_selector: parser.MatchdaySelector
) -> list[table_entry.TableEntry]:
    table: dict[str, table_entry.TableEntry] = {}

    for fixture in matchdays[0].fixtures:
        table[fixture.home_team] = table_entry.TableEntry(fixture.home_team)
        table[fixture.away_team] = table_entry.TableEntry(fixture.away_team)

    standings: list[table_entry.TableEntry] = []

    for matchday in matchdays:
        for fixture in matchday.fixtures:
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
