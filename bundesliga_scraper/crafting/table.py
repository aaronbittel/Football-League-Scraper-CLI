from itertools import batched

from bundesliga_scraper.api import api
from bundesliga_scraper.crafting.graph_testings import print_points
from bundesliga_scraper.datatypes.constants import League
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry, Matchday
from bundesliga_scraper.datatypes.table_entry import Table, TableEntry

table: Table = api.initialize_league_table(League.Bundesliga)
all_fixtures: list[FixtureEntry] = api.retrieve_all_matchdays(League.Bundesliga)
all_matchdays: list[Matchday] = [
    Matchday(matchday=matchday, fixtures=fixtures)
    for matchday, fixtures in enumerate(batched(all_fixtures, 9), start=1)
]


table.calculate_table(all_matchdays[:25])


teams: list[TableEntry] = table._sort()
# for pl, team in enumerate(teams, start=1):
#     print(
#         f"{pl:<3}{team.get_standings_direction():<5}{team.team_name:<30}{team.matches:>3}{team.goal_diff:>5}{team.points:>3}"
#     )

print_points(
    [
        table.teams["Bayer Leverkusen"].history.points,
        table.teams["FC Bayern München"].history.points,
        table.teams["Borussia Dortmund"].history.points,
        table.teams["1. FC Union Berlin"].history.points,
    ]
)
