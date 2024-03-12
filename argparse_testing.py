import argparse


def handle_table_request(args):
    print("HI FROM TABLE")
    print(args)


def handle_fixture_request(args):
    print("HELLO FROM FIXTURE", args)


# create the top-level parser
parser = argparse.ArgumentParser(prog="PROG")
parser.add_argument(
    "league",
    choices=["bundesliga", "2_bundesliga"],
    help="Choose the league you want the information for.",
)

parser.add_argument(
    "-s",
    "--start-session",
    action="store_true",
    default=False,
    help="Starts a session saving the league, options for compact mode",
)
subparsers = parser.add_subparsers(dest="subcommand", help="sub-command help")

# create the parser for the "table" command
parser_table = subparsers.add_parser("table", help="table help")
parser_table.add_argument(
    "matchday",
    nargs="?",
    type=int,
    default=-1,
    help="Display table of given matchday, defaults to current",
)

parser_table.add_argument("-c", "--compact", action="store_true", default=False)

parser_table.add_argument(
    "-H", "--highlight", action="store", nargs="+", dest="highlighted_teams"
)

parser_table.set_defaults(func=handle_table_request)

# create the parser for the "fixture" command
parser_fixture = subparsers.add_parser("fixture", help="fixture help")
parser_fixture.add_argument(
    "matchday",
    nargs="?",
    type=int,
    default=-1,
    help="Display fixtures of given matchday, defaults to current",
)

parser_fixture.set_defaults(func=handle_fixture_request)

# parse the argument list
# args = parser.parse_args(
#     [
#         "bundesliga",
#         "-s",
#         "table",
#         "12",
#         "-c",
#         "--highlight",
#         "Bayern",
#         "Dortmund",
#         "Augsburg",
#     ]
# )
args = parser.parse_args(["2_bundesliga", "fixture", "12", "--start-session"])

args.func(args)
