"""Module that represents a table entry."""

from dataclasses import dataclass


@dataclass
class TableEntry:
    """Team entry that represents a row in a football table."""

    team_name: str
    points: int
    games: int
    wins: int
    ties: int
    defeats: int
    goals: tuple[int, int]
    diff: int
