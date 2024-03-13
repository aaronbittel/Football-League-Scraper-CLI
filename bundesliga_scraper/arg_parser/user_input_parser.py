"""Parsing the users input."""

from __future__ import annotations

import argparse

from bundesliga_scraper.request_handler.table_request_handler import (
    handle_table_request,
)
from bundesliga_scraper.request_handler.fixture_request_handler import (
    handle_fixture_request,
)


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

    table_parser = subparsers.add_parser("table", help="table help")
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
        dest="highlight",
        nargs="+",
        help="Give a list of teams that will be highlighted in the output.",
    )

    table_parser.set_defaults(func=handle_table_request)

    fixture_parser = subparsers.add_parser("fixture", help="fixture help")
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

    fixture_parser.set_defaults(func=handle_fixture_request)
    return parser


def parse_user_args(parser: argparse.ArgumentParser) -> None:
    """Parsing the arguments given by the user.

    Args:
        parser (argparse.ArgumentParser): parser
    """
    args = parser.parse_args()
    args.func(args)
