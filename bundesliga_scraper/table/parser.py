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
    league: str
    from_: int = 1
    to: int = 34
    include_postponed_matches: bool = True
    home: bool = True
    away: bool = True


@dataclass
class TableRequestJob:
    title: str
    highlights: list[str]
    standings: list[TableEntry] = field(default_factory=list)


# yields MatchdaySelector objects and doesn't accept any input parameters or send any values back
def parse(
    args: Namespace,
) -> Generator[tuple[TableRequestJob, MatchdaySelector], None, None]:
    league = get_league(args.league)
    league_name = LEAGUE_NAMES[league]
    highlights = args.highlights
    active_matchday = h.cache[league]["active_matchday"]

    if args.first_round:
        request_job = get_first_round_request_job(league_name, highlights)
        selector = get_first_round_selector(league, active_matchday)
        yield request_job, selector

    if args.second_round:
        request_job = get_second_round_request_job(league_name, highlights)
        selector = get_second_round_selector(league, active_matchday)
        yield request_job, selector
    if args.last:
        request_job = get_last_request_job(
            league_name=league_name, n=args.last, highlights=highlights
        )
        selector = get_last_selector(league, args.last, active_matchday)
        yield request_job, selector

    if args.since:
        request_job = get_since_request_job(
            league_name=league_name, n=args.last, highlights=highlights
        )
        selector = get_since_selector(league, args.since, active_matchday)
        yield request_job, selector

    if args.home:
        request_job = get_home_request_job(league_name, highlights)
        selector = get_home_selector(league, active_matchday)
        yield request_job, selector

    if args.away:
        request_job = get_away_request_job(league_name, highlights)
        selector = get_away_selector(league, active_matchday)
        yield request_job, selector

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
        request_job = get_matchday_request_job(
            league_name=league_name, n=matchday, highlights=highlights
        )
        selector = get_matchday_selector(league, matchday, active_matchday)
        yield request_job, selector


def get_first_round_request_job(
    league_name: str, highlights: list[str]
) -> TableRequestJob:
    return TableRequestJob(
        title=f"{league_name} First Round Table",
        highlights=highlights if highlights else [],
    )


def get_second_round_request_job(
    league_name: str, highlights: list[str]
) -> TableRequestJob:
    return TableRequestJob(
        title=f"{league_name} Second Round Table",
        highlights=highlights if highlights else [],
    )


def get_last_request_job(
    league_name: str, n: int, highlights: list[str]
) -> TableRequestJob:
    return TableRequestJob(
        title=f"{league_name} Table Last {n} Matchdays",
        highlights=highlights if highlights else [],
    )


def get_since_request_job(
    league_name: str, n: int, highlights: list[str]
) -> TableRequestJob:
    return TableRequestJob(
        title=f"{league_name} Table Since Matchday {n}",
        highlights=highlights if highlights else [],
    )


def get_home_request_job(league_name: str, highlights: list[str]) -> TableRequestJob:
    return TableRequestJob(
        title=f"{league_name} Home Table",
        highlights=highlights if highlights else [],
    )


def get_away_request_job(league_name: str, highlights: list[str]) -> TableRequestJob:
    return TableRequestJob(
        title=f"{league_name} Away Table",
        highlights=highlights if highlights else [],
    )


def get_matchday_request_job(
    league_name: str, n: int, highlights: list[str]
) -> TableRequestJob:
    return TableRequestJob(
        title=f"{league_name} Table Matchday {n}",
        highlights=highlights if highlights else [],
    )


def get_home_selector(league: League, active_matchday: int) -> MatchdaySelector:
    return MatchdaySelector(league=league, to=active_matchday, away=False)


def get_away_selector(league: League, active_matchday: int) -> MatchdaySelector:
    return MatchdaySelector(league=league, to=active_matchday, home=False)


def get_matchday_selector(
    league: League, matchday: int, active_matchday: int
) -> MatchdaySelector:
    matchday = min(active_matchday, max(1, matchday))
    return MatchdaySelector(league=league, to=matchday, include_postponed_matches=False)


def get_last_selector(league: League, n: int, active_matchday: int) -> MatchdaySelector:
    matchday = active_matchday - n + 1
    if matchday < 1:
        matchday = 1
    return MatchdaySelector(league=league, from_=matchday, to=active_matchday)


def get_since_selector(
    league: League, since: int, active_matchday: int
) -> MatchdaySelector:
    if since > active_matchday:
        since = active_matchday

    return MatchdaySelector(league=league, from_=since, to=active_matchday)


def get_first_round_selector(league: League, active_matchday: int) -> MatchdaySelector:
    matchday = min(FIRST_ROUND_MATCHDAY, active_matchday)
    return MatchdaySelector(league=league, to=matchday)


def get_second_round_selector(league: League, active_matchday: int) -> MatchdaySelector:
    if active_matchday <= FIRST_ROUND_MATCHDAY:
        # TODO Implement a 0-Table
        raise ValueError(
            f"No second half table available. Its only matchday {active_matchday}"
        )
    return MatchdaySelector(
        league=league, from_=FIRST_ROUND_MATCHDAY + 1, to=active_matchday
    )
