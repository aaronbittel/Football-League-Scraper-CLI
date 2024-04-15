import argparse


DEFAULT_NEXT = 3
DEFAULT_PREV = 2


def parse(args: argparse.Namespace, last_played_matchday_index: int) -> tuple[int, int]:
    if args.all:
        return 1, 34

    prev = DEFAULT_PREV if args.prev is None else args.prev
    nxt = DEFAULT_NEXT if args.next is None else args.next

    return last_played_matchday_index - prev + 1, last_played_matchday_index + nxt + 1
