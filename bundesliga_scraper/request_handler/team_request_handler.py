from argparse import Namespace

from bundesliga_scraper.api import api
from bundesliga_scraper.datatypes.constants import League
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.matchday import Matchday
from bundesliga_scraper.data_printer.fixture_printer import print_fixture_entries


def handle_team_request(args: Namespace) -> None:
    team: str = args.team_name[0]

    league: League = (
        League.Bundesliga
        if args.league.lower() == "bundesliga"
        else League.Bundesliga_2
    )
    team_fixture_entries: list[FixtureEntry] = api.retrieve_match_data_team(
        league=league, team=team
    )

    last_played_matchday = 0
    for i, fixture in enumerate(team_fixture_entries):
        if not fixture.match_is_finished:
            last_played_matchday = i
            break
    print(last_played_matchday)

    title = f"{team} Fixtures & Results"
    matches = Matchday(
        matchday=0,
        fixtures=team_fixture_entries[
            last_played_matchday - 3 : last_played_matchday + 2
        ],
    )
    print_fixture_entries(title=title, matchday=matches, highlights=[])
