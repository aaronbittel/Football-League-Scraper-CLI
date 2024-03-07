"""Parsing the users input."""

from __future__ import annotations

import argparse
import sys

from bundesliga_scraper.request_handler import request_handler

FLAGS = ["--table", "--fixture", "-s", "--start-session", "-h", "--help"]

LEAGUE_ABBR = {"bundesliga": "BL", "2_bundesliga": "2BL"}


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
        default="bundesliga",
        choices=["bundesliga", "2_bundesliga"],
        help="Executing the command for the given league",
    )

    parser.add_argument(
        "--table",
        nargs="?",
        const=-1,  # indicates current table
        type=int,
        help="Displaying the table of the given gameday (defaults to current)",
    )

    parser.add_argument(
        "--fixture",
        nargs="?",
        const=-1,  # indicates current fixture
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
    """Parsing the arguments given by the user.

    Args:
        parser (argparse.ArgumentParser): parser
    """
    args = parser.parse_args()

    if not any((args.table, args.fixture, args.session)):
        parser.print_help()

    request_handler.handle_args(vars(args))  # convert Namespace to dictionary

    if args.session:
        start_session(parser, args.league)


def start_session(parser: argparse.ArgumentParser, league: str) -> None:
    """Controls the flow of the program inside a session.

    Args:
        parser (argparse.ArgumentParser): parser
        league (str): the league the user created the session with
    """
    while True:
        user_input = input(f"({LEAGUE_ABBR[league.lower()]}) > ").split(" ")

        if user_input[0].lower() in ["exit", "exit()", "close", "close()"]:
            sys.exit(0)

        user_args = ""
        # if no league was given use league with which session was started
        if user_input[0] in FLAGS:
            user_args = [league, *user_input]
        elif user_input[0] in LEAGUE_ABBR and ("-s" or "--start-session" in user_input):
            league = user_input[0]
            user_args = user_input
        else:
            user_args = user_input

        args = parser.parse_args(user_args)

        request_handler.handle_args(vars(args))  # convert Namespace to dictionary
