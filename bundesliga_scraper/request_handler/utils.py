from bundesliga_scraper.datatypes.constants import League


MAX_MATCHDAY = 34
FIRST_ROUND_MATCHDAY = MAX_MATCHDAY // 2


def get_league(league: str) -> League:
    return League.Bundesliga if league.lower() == "bundesliga" else League.Bundesliga_2
