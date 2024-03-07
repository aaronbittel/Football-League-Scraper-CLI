"""Module that represents a Fixture entry."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


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

    def _home_team_won(self) -> bool:
        """Returns true if home team won.

        Returns:
            bool: true if home team won
        """
        return self.home_goals > self.away_goals
