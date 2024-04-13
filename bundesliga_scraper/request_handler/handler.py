import argparse
from bundesliga_scraper.api import api
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
        for request_job, matchday_selector in parser.parse(args):
            standings = calculator.calculate(
                matchdays=cache[league]["all_matchdays"][
                    matchday_selector.from_ - 1 : matchday_selector.to
                ],
                matchday_selector=matchday_selector,
            )
            request_job.standings = standings
            table = rich.create_table(request_job)
            console = c.Console()
            console.print(table)

    elif args.subcommand == "fixture":
        print("FIXTURE REQUEST")
    else:
        print("TEAM REQUEST")


def get_active_matchday(current_matchday: m.Matchday) -> int:
    for fixture in current_matchday.fixtures:
        if fixture.match_is_finished or fixture.match_is_live:
            return current_matchday.matchday
    return current_matchday.matchday - 1
