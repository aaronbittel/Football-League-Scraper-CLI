from bundesliga_scraper.datatypes.constants import League
from bundesliga_scraper.datatypes.fixture import fixture_entry


MAX_MATCHDAY = 34
FIRST_ROUND_MATCHDAY = MAX_MATCHDAY // 2


def get_league(league: str) -> League:
    return League.Bundesliga if league.lower() == "bundesliga" else League.Bundesliga_2


def get_active_matchday(current_matchday: list[fixture_entry.FixtureEntry]) -> int:
    if all(fixture.match_is_in_future for fixture in current_matchday):
        return current_matchday[0].matchday
    return current_matchday[0].matchday - 1
