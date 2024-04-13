from argparse import Namespace
from dataclasses import dataclass, field
from typing import Generator


from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES, League
from bundesliga_scraper.datatypes.table_entry import TableEntry
import bundesliga_scraper.request_handler.handler as h
from bundesliga_scraper.request_handler.utils import get_league


FIRST_ROUND_MATCHDAY = 17


@dataclass(frozen=True)
class MatchdaySelector:
    from_: int = 1
    to: int = 34
    include_postponed_matches: bool = True
    home: bool = True
    away: bool = True


# yields MatchdaySelector objects and doesn't accept any input parameters or send any values back
def parse(
    args: Namespace,
) -> Generator[tuple[str, MatchdaySelector], None, None]:
    league = get_league(args.league)
    league_name = LEAGUE_NAMES[league]
    active_matchday = h.cache[league]["active_matchday"]

    if args.first_round:
        title = f"{league_name} First Round Table"
        yield title, get_first_round_selector(active_matchday)

    if args.second_round:
        title = f"{league_name} Second Round Table"
        yield title, get_second_round_selector(active_matchday)

    if args.last:
        title = f"{league_name} Table Last {args.last} Matchdays"
        yield title, get_last_selector(args.last, active_matchday)

    if args.since:
        title = f"{league_name} Table Since Matchday {args.since}"
        yield title, get_since_selector(args.since, active_matchday)

    if args.home:
        title = f"{league_name} Home Table"
        yield title, get_home_selector(active_matchday)

    if args.away:
        title = f"{league_name} Away Table"
        yield title, get_away_selector(active_matchday)

    if args.matchday or not any(
        (
            args.first_round,
            args.second_round,
            args.last,
            args.since,
            args.home,
            args.away,
        )
    ):
        matchday = active_matchday if args.matchday is None else args.matchday
        title = f"{league_name} Table Matchday {matchday}"
        yield title, get_matchday_selector(matchday, active_matchday)


def get_home_selector(active_matchday: int) -> MatchdaySelector:
    return MatchdaySelector(to=active_matchday, away=False)


def get_away_selector(active_matchday: int) -> MatchdaySelector:
    return MatchdaySelector(to=active_matchday, home=False)


def get_matchday_selector(matchday: int, active_matchday: int) -> MatchdaySelector:
    matchday = min(active_matchday, max(1, matchday))
    return MatchdaySelector(to=matchday, include_postponed_matches=False)


def get_last_selector(n: int, active_matchday: int) -> MatchdaySelector:
    matchday = active_matchday - n + 1
    if matchday < 1:
        matchday = 1
    return MatchdaySelector(from_=matchday, to=active_matchday)


def get_since_selector(since: int, active_matchday: int) -> MatchdaySelector:
    if since > active_matchday:
        since = active_matchday

    return MatchdaySelector(from_=since, to=active_matchday)


def get_first_round_selector(active_matchday: int) -> MatchdaySelector:
    matchday = min(FIRST_ROUND_MATCHDAY, active_matchday)
    return MatchdaySelector(to=matchday)


def get_second_round_selector(active_matchday: int) -> MatchdaySelector:
    if active_matchday <= FIRST_ROUND_MATCHDAY:
        # TODO Implement a 0-Table
        raise ValueError(
            f"No second half table available. Its only matchday {active_matchday}"
        )
    return MatchdaySelector(from_=FIRST_ROUND_MATCHDAY + 1, to=active_matchday)
