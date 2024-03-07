"""Module that represents a table entry."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TableEntry:
    team_name: str
    points: int
    opponent_goals: int
    goals: int
    matches: int
    won: int
    lost: int
    draw: int
    goal_diff: int

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> TableEntry:
        return cls(
            team_name=data["teamName"],
            points=int(data["points"]),
            opponent_goals=int(data["opponentGoals"]),
            goals=int(data["goals"]),
            matches=int(data["matches"]),
            won=int(data["won"]),
            lost=int(data["lost"]),
            draw=int(data["draw"]),
            goal_diff=int(data["goalDiff"]),
        )
