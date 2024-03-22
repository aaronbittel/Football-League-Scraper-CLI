from argparse import Namespace

from bundesliga_scraper.api import api
from bundesliga_scraper.datatypes.constants import League
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.matchday import Matchday
from bundesliga_scraper.data_printer.fixture_printer import print_fixture_entries


def handle_team_request(args: Namespace) -> None:
    team: str = args.team_name[0]

    future_games = 2 if args.next is None else args.next
    previous_games = 3 if args.prev is None else args.prev

    league: League = (
        League.Bundesliga
        if args.league.lower() == "bundesliga"
        else League.Bundesliga_2
    )
    team_fixture_entries: list[FixtureEntry] = api.retrieve_match_data_team(
        league=league, team=team
    )

    last_played_matchday_index = get_last_played_matchday_index(team_fixture_entries)
    print(last_played_matchday_index)

    from_ = last_played_matchday_index - previous_games
    to = last_played_matchday_index + future_games

    title = f"{team} Fixtures & Results"
    matches = Matchday(
        matchday=0,
        fixtures=team_fixture_entries[from_:to],
    )
    print_fixture_entries(title=title, matchday=matches, highlights=[])


def get_last_played_matchday_index(team_fixture_entries):
    for i, fixture in enumerate(team_fixture_entries):
        if not fixture.match_is_finished:
            return i
    return 0
