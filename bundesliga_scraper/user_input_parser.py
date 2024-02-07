"""Module for parsing the users input"""

import argparse
import sys

from bundesliga_scraper import data_fetcher

FLAGS = ["--table", "--fixture", "-s", "--start-session", "-h", "--help"]


def create_parser() -> argparse.ArgumentParser:
    """Creating the parser object and adding its arguments

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
        default="bundesliga",
        choices=["bundesliga", "2_bundesliga"],
        help="Executing the command for the given league",
    )

    parser.add_argument(
        "--table",
        nargs="?",
        const=21,
        type=int,
        help="Displaying the table of the given gameday (defaults to current)",
    )

    parser.add_argument(
        "--fixture",
        nargs="?",
        const=21,
        type=int,
        help="Displaying the fixture / results of the given gameday \
            (defaults to current)",
    )

    parser.add_argument(
        "-s",
        "--start-session",
        dest="session",
        action="store_true",
        help="Starts a session for the given league -> league is now default",
    )

    return parser


def parse_user_args(parser: argparse.ArgumentParser) -> None:
    """Parsing the arguments given by the user

    Args:
        parser (argparse.ArgumentParser): parser
    """

    args = parser.parse_args()

    if not any((args.table, args.fixture, args.session)):
        parser.print_help()

    handle_args(vars(args))  # convert Namespace to dictionary

    if args.session:
        start_session(parser, args.league)


def start_session(parser: argparse.ArgumentParser, league: str) -> None:
    """Controls the flow of the program inside a session

    Args:
        parser (argparse.ArgumentParser): parser
        league (str): the league the user created the session with
    """

    while True:
        user_input = input(">>> ").split(" ")

        if user_input[0].lower() == "exit":
            sys.exit(0)

        user_args = ""
        if user_input[0] in FLAGS:
            user_args = [league] + user_input
        else:
            user_args = user_input

        args = parser.parse_args(user_args)

        handle_args(vars(args))  # convert Namespace to dictionary


def handle_args(args: dict[str, str | int]) -> None:
    """Handling the arguments given by the user

    Args:
        args (dict[str, str  |  int]): dict of key value pairs given by the user
    """
    if args["table"]:
        handle_table_request(
            league=args["league"],  # pyright: ignore[reportGeneralTypeIssues]
            gameday=args["table"],  # pyright: ignore[reportGeneralTypeIssues]
        )

    if args["fixture"]:
        handle_fixture_request(
            league=args["league"],  # pyright: ignore[reportGeneralTypeIssues]
            gameday=args["fixture"],  # pyright: ignore[reportGeneralTypeIssues]
        )


def handle_table_request(league: str, gameday: int) -> None:
    """Handling the table request

    Args:
        league (str): supplied league
        gameday (int): gameday for the table
    """
    table_entries_list = data_fetcher.get_table_information(
        league=league, gameday=gameday
    )


def handle_fixture_request(league: str, gameday: int) -> None:
    """Handling fixture request

    Args:
        league (str): supplied league
        gameday (int): gameday for the fixture
    """

    print(f"fetching {league} fixture data for the gameday {gameday}")
