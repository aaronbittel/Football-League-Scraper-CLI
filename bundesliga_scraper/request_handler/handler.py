import argparse

from bundesliga_scraper.api import api
from bundesliga_scraper.datatypes.table_job_creation import TableCreationJob
from bundesliga_scraper.table import rich_table_creation as rich
from bundesliga_scraper.request_handler import utils
from bundesliga_scraper.table import calculator
from bundesliga_scraper.datatypes import matchday as m
from bundesliga_scraper.table import parser
from rich import console as c


cache: dict[str, any] = {}


def handler(args: argparse.Namespace) -> None:
    global cache
    league = utils.get_league(args.league)
    if args.subcommand == "table":
        cache = {
            league: {
                "all_matchdays": api.retrieve_all_matchdays(league),
                "current_matchday": api.retrieve_current_matchday(league),
            }
        }
        cache[league]["active_matchday"] = get_active_matchday(
            cache[league]["all_matchdays"][cache[league]["current_matchday"] - 1]
        )
        for title, matchday_selector in parser.parse(args):
            standings = calculator.calculate(
                matchdays=cache[league]["all_matchdays"][
                    matchday_selector.from_ - 1 : matchday_selector.to
                ],
                matchday_selector=matchday_selector,
            )
            highlights = args.highlights if args.highlights else []
            request_job = TableCreationJob(title, standings, highlights)
            table = rich.create_table(request_job)
            console = c.Console()
            console.print(table)

    elif args.subcommand == "fixture":
        args.func(args)
    else:
        team = args.team_name[0]
        all_matchdays = api.retrieve_all_matchdays(league)
        current_matchday = api.retrieve_current_matchday(league)
        matchday_selector = parser.MatchdaySelector(to=current_matchday)
        standings = calculator.calculate(
            matchdays=all_matchdays[matchday_selector.from_ - 1 : matchday_selector.to],
            matchday_selector=matchday_selector,
        )

        focus = 0
        for pl, entry in enumerate(standings, start=1):
            if team.lower() in entry.team_name.lower():
                focus = pl
                break

        request_job = TableCreationJob(
            title="", standings=standings, focus=focus, highlights=[]
        )
        table = rich.create_table(request_job)
        console = c.Console()
        console.print(table, justify="center")


def get_active_matchday(current_matchday: m.Matchday) -> int:
    for fixture in current_matchday.fixtures:
        if fixture.match_is_finished or fixture.match_is_live:
            return current_matchday.matchday
    return current_matchday.matchday - 1
