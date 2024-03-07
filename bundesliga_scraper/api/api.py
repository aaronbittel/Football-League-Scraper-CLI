from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import requests

BASE_URL = "https://api.openligadb.de"


class League(StrEnum):
    Bundesliga = "bl1"
    Bundesliga_2 = "bl2"


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
            teamName=data["teamName"],
            points=int(data["points"]),
            opponentGoals=int(data["opponentGoals"]),
            goals=int(data["goals"]),
            matches=int(data["matches"]),
            won=int(data["won"]),
            lost=int(data["lost"]),
            draw=int(data["draw"]),
            goalDiff=int(data["goalDiff"]),
        )


def get_table(league: League, season: int) -> dict:
    """Fetches the Football table data for a particular league and a season."""
    url = build_get_table_url(league, season)
    response = requests.get(url, timeout=3)
    return response.json()


def build_get_table_url(league: League, season: int) -> str:
    return f"{BASE_URL}/getbltable/{league}/{season}"


def retrieve_table(league: League, season: int) -> TableEntry:
    data = get_table(league=league, season=season)
    return [TableEntry.from_dict(table_entry) for table_entry in data]


def print_table_entry(table_entry: TableEntry, placement: int):
    output = f"{placement:<4}"
    output += f"{table_entry.team_name:<30}"
    output += f"{table_entry.matches:<4}"
    output += f"{table_entry.won:<4}"
    output += f"{table_entry.lost:<4}"
    output += f"{table_entry.draw:<4}"
    output += f"{table_entry.goals:>3}:{table_entry.opponent_goals:<4}"
    output += f"{table_entry.goal_diff:<4}"
    output += f"{table_entry.points:<4}"
    print(output)


def main():
    bl_table = retrieve_table(League.Bundesliga, season=2023)
    for placement, entry in enumerate(bl_table, start=1):
        print_table_entry(entry, placement=placement)


if __name__ == "__main__":
    main()
