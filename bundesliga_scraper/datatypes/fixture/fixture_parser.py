import argparse


def parse(args: argparse.Namespace, current_matchday: int) -> int:
    matchday = args.matchday if args.matchday is not None else current_matchday
    return matchday + args.next - args.prev
