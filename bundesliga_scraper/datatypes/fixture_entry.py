"""Module that represents a Fixture entry."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class Result(Enum):
    HOME_WON = auto()
    AWAY_WON = auto()
    DRAW = auto()


@dataclass
class FixtureEntry:
    """Class that represents a fixture entry of a given matchday."""

    home_team: str
    away_team: str
    home_goals: int
    away_goals: int
    matchday: int
    match_is_finished: bool
    date: datetime

    @classmethod
    def from_dict(cls, data: dict) -> FixtureEntry:
        home_team = data["team1"]["teamName"]
        away_team = data["team2"]["teamName"]
        match_is_finished = bool(data["matchIsFinished"])
        date = datetime.strptime(data["matchDateTime"], r"%Y-%m-%dT%H:%M:%S")
        matchday = int(data["group"]["groupOrderID"])

        if match_is_finished:
            home_goals = int(data["matchResults"][1]["pointsTeam1"])
            away_goals = int(data["matchResults"][1]["pointsTeam2"])
        else:
            home_goals, away_goals = 0, 0

        return cls(
            home_team=home_team,
            away_team=away_team,
            home_goals=home_goals,
            away_goals=away_goals,
            matchday=matchday,
            match_is_finished=match_is_finished,
            date=date,
        )

    def home_team_won(self) -> bool:
        """Returns true if home team won.

        Returns:
            bool: true if home team won
        """
        return self.home_goals > self.away_goals

    def away_team_won(self) -> bool:
        return self.away_goals > self.home_goals

    def get_result(self) -> Result:
        if self.home_team_won():
            return Result.HOME_WON
        if self.away_team_won():
            return Result.AWAY_WON
        return Result.DRAW

    def get_home_team(self) -> str:
        return self.home_team

    def __str__(self) -> str:
        return f"{self.home_team}${self.away_team}${self.home_goals}${self.away_goals}${self.matchday}${self.match_is_finished}${self.date}"
