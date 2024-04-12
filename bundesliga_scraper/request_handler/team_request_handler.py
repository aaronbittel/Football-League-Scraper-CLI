from argparse import Namespace
from dataclasses import dataclass

from bundesliga_scraper.api import api
from bundesliga_scraper.data_printer.team_printer import print_team_entries
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.team import TeamSeasonMatches
from bundesliga_scraper.request_handler.utils import MAX_MATCHDAY, get_league

TITLE_TEMPLATE = "{} Fixtures & Results"
FUTURE_GAMES_COUNT = 3
PREVOUS_GAMES_COUNT = 2


@dataclass(frozen=True)
class TeamRequestParams:
    next_: int
    prev: int
    all_: bool
    last_played_matchday_index: int


def handle_team_request(args: Namespace) -> None:
    team: str = args.team_name[0].capitalize()

    league = get_league(args.league)

    team_fixture_entries = api.retrieve_team_match_data(league=league, team=team)

    last_played_matchday_index = get_last_played_matchday_index(team_fixture_entries)

    team_request_params = TeamRequestParams(
        next_=args.next,
        prev=args.prev,
        all_=args.all,
        last_played_matchday_index=last_played_matchday_index,
    )

    from_, to = get_matchday_range(team_request_params)

    selected_team_matches = TeamSeasonMatches(
        team_name=team,
        results=team_fixture_entries[from_:last_played_matchday_index],
        fixtures=team_fixture_entries[last_played_matchday_index:to],
    )
    title = TITLE_TEMPLATE.format(team)
    print_team_entries(league, title, selected_team_matches)


def get_matchday_range(params: TeamRequestParams):
    previous_games = PREVOUS_GAMES_COUNT if params.prev is None else params.prev
    future_games = FUTURE_GAMES_COUNT if params.next_ is None else params.next_

    if params.all_:
        from_ = 0
        to = MAX_MATCHDAY
    else:
        from_ = params.last_played_matchday_index - previous_games
        to = params.last_played_matchday_index + future_games
    return from_, to


def get_last_played_matchday_index(team_fixture_entries: list[FixtureEntry]):
    for i, fixture in enumerate(team_fixture_entries):
        if not fixture.match_is_finished:
            return i
    return 0
