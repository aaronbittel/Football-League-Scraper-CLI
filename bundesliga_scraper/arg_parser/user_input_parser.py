"""Parsing the users input."""

import argparse

from bundesliga_scraper.datatypes.fixture.fixture_request_handler import (
    handle_fixture_request,
)
from bundesliga_scraper.datatypes.table.table_request_handler import (
    table_request_handler,
)
from bundesliga_scraper.datatypes.team.team_request_handler import handle_team_request

from bundesliga_scraper.datatypes import utils
from bundesliga_scraper.datatypes.league import league
from bundesliga_scraper.datatypes.table import table_parser, table_creation
from rich import console as con


def create_parser() -> argparse.ArgumentParser:
    """Creating the parser object and adding its arguments.

    Returns:
        argparse.ArgumentParser: parser
    """
    parser = argparse.ArgumentParser(
        prog="Bundesliga Scraper",
        description="Scraping the Bundesliga",
        epilog="Welcome!",
        exit_on_error=False,
    )

    parser.add_argument(
        "league",
        choices=["bundesliga", "2_bundesliga"],
        help="Choose the league you want the information for.",
    )

    # parser.add_argument(
    #     "-s",
    #     "--start-session",
    #     dest="session",
    #     action="store_true",
    #     help="Starts a session for the given league -> league is now default",
    # )

    subparsers = parser.add_subparsers(dest="subcommand", help="sub-command-help")

    create_table_subcommand_parser(subparsers)
    create_fixture_subcommand_parser(subparsers)
    create_team_subcommand_parser(subparsers)

    return parser


def parse_user_args(parser: argparse.ArgumentParser) -> None:
    """Parsing the arguments given by the user.

    Args:
        parser (argparse.ArgumentParser): parser
    """
    args = parser.parse_args()
    requested_league = utils.get_league(args.league)
    football_league = league.League(requested_league)
    console = con.Console()
    if args.subcommand == "table":
        for title, matchday_selector in table_parser.parse(
            args, football_league.active_matchday
        ):
            standings = football_league.calculate_table(matchday_selector)
            table = table_creation.create_table(title, standings, args.highlights)
            console.print(table, justify="center")


def create_team_subcommand_parser(subparsers: argparse._SubParsersAction) -> None:
    team_parser = subparsers.add_parser(
        "team", help="Get Table and Fixture information specific about a team."
    )
    team_parser.add_argument(
        "team_name",
        nargs=1,
        help="Select a team of a league to get information specificly about that team.",
    )

    team_parser.add_argument(
        "--next",
        "-n",
        const=5,
        nargs="?",
        type=int,
        dest="next",
        help="Display the next [given] matchdays for the team, defaults to 5.",
    )

    team_parser.add_argument(
        "--prev",
        "-p",
        const=5,
        nargs="?",
        type=int,
        dest="prev",
        help="Display the previous [given] matchdays for the team, defaults to 5.",
    )

    team_parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        dest="all",
        help="Display all results and fixtures of the specified team.",
    )

    team_parser.set_defaults(func=handle_team_request)


def create_fixture_subcommand_parser(subparsers: argparse._SubParsersAction) -> None:
    fixture_parser = subparsers.add_parser(
        "fixture", help="Get Fixture information about the specified league."
    )
    fixture_parser.add_argument(
        "matchday",
        nargs="?",
        type=int,
        help="Displaying the fixture / results of the given gameday \
            (defaults to current)",
    )

    fixture_parser.add_argument(
        "-n",
        "--next",
        action="count",
        default=0,
        dest="next",
        help="Display the next fixture. Use once to show the immediate next fixture, \
          or multiple times to show fixtures further in the future.",
    )

    fixture_parser.add_argument(
        "-p",
        "--previous",
        action="count",
        default=0,
        dest="prev",
        help="Display the previous fixture. Use once to show the immediate previous fixture, \
          or multiple times to show fixtures further in the past.",
    )

    fixture_parser.add_argument(
        "-hl",
        "--highlight",
        dest="highlights",
        nargs="+",
        help="Give a list of teams that will be highlighted in the output.",
    )

    fixture_parser.set_defaults(func=handle_fixture_request)


def create_table_subcommand_parser(subparsers: argparse._SubParsersAction) -> None:
    table_parser = subparsers.add_parser(
        "table", help="Get Table information about the specified league."
    )
    table_parser.add_argument(
        "matchday",
        nargs="?",
        type=int,
        help="Display table of given matchday, if none is given displays current",
    )

    table_parser.add_argument(
        "-fr",
        "--first-round",
        action="store_true",
        dest="first_round",
        help="Displaying the table after the first round.",
    )

    table_parser.add_argument(
        "-sr",
        "--second-round",
        action="store_true",
        dest="second_round",
        help="Displaying the table after the second round.",
    )

    table_parser.add_argument(
        "-l",
        "--last",
        dest="last",
        type=int,
        help="Calculates the last {n} matchdays and displays it.",
    )

    table_parser.add_argument(
        "-s",
        "--since",
        dest="since",
        type=int,
        help="Calculates from given matchday to present.",
    )

    table_parser.add_argument(
        "-H",
        "--home",
        dest="home",
        action="store_true",
        help="Calculates and displays the home table.",
    )

    table_parser.add_argument(
        "-a",
        "--away",
        dest="away",
        action="store_true",
        help="Calculates and displays the away table.",
    )

    table_parser.add_argument(
        "-hl",
        "--highlight",
        dest="highlights",
        nargs="+",
        help="Give a list of teams that will be highlighted in the output.",
    )

    table_parser.set_defaults(func=table_request_handler)
