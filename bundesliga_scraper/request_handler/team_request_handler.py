from argparse import Namespace

from bundesliga_scraper.api import api
from bundesliga_scraper.data_printer.team_printer import print_team_entries
from bundesliga_scraper.datatypes.constants import League
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.matchday import Matchday


def handle_team_request(args: Namespace) -> None:
    team: str = args.team_name[0]

    league = (
        League.Bundesliga
        if args.league.lower() == "bundesliga"
        else League.Bundesliga_2
    )

    future_games = 3 if args.next is None else args.next
    previous_games = 2 if args.prev is None else args.prev

    team_fixture_entries = api.retrieve_team_match_data(league=league, team=team)

    last_played_matchday_index = get_last_played_matchday_index(team_fixture_entries)

    if args.all:
        from_ = 0
        to = 34
    else:
        from_ = last_played_matchday_index - previous_games
        to = last_played_matchday_index + future_games

    title = f"{team} Fixtures & Results"
    matches = Matchday(
        matchday=0,
        fixtures=team_fixture_entries[from_:to],
    )
    print_team_entries(title, matches)


def get_last_played_matchday_index(team_fixture_entries: list[FixtureEntry]):
    for i, fixture in enumerate(team_fixture_entries):
        if not fixture.match_is_finished:
            return i
    return 0
