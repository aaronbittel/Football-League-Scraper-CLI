"""Module that represents a Fixture entry."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from bundesliga_scraper.datatypes.constants import League, MatchResult


@dataclass(frozen=True)
class FixtureEntry:
    """Class that represents a fixture entry of a given matchday."""

    home_team: str
    away_team: str
    home_goals: int
    away_goals: int
    matchday: int
    match_is_finished: bool
    match_is_live: bool
    date: datetime

    @classmethod
    def from_dict(cls, data: dict) -> FixtureEntry:
        home_team = data["team1"]["teamName"]
        away_team = data["team2"]["teamName"]
        goals = data["goals"]
        match_is_finished = bool(data["matchIsFinished"])
        match_is_live = False
        match_results = data["matchResults"]
        date = datetime.strptime(data["matchDateTime"], r"%Y-%m-%dT%H:%M:%S")
        matchday = int(data["group"]["groupOrderID"])

        if match_is_finished:
            # in Bundesliga matchResults[1] is end of game result
            if data["leagueShortcut"] == League.Bundesliga:
                home_goals = int(data["matchResults"][1]["pointsTeam1"])
                away_goals = int(data["matchResults"][1]["pointsTeam2"])
            # in 2. Bundesliga matchResults[0] is end of game results
            elif data["leagueShortcut"] == League.Bundesliga_2:
                home_goals = int(data["matchResults"][0]["pointsTeam1"])
                away_goals = int(data["matchResults"][0]["pointsTeam2"])
        elif match_results or timedelta(hours=0) < datetime.now() - date < timedelta(
            hours=1
        ):
            match_is_live = True
            home_goals, away_goals = 0, 0
            for goal in goals:
                if goal["scoreTeam1"] == 0:
                    away_goals += 1
                else:
                    home_goals += 1
        else:
            home_goals, away_goals = 0, 0

        return cls(
            home_team=home_team,
            away_team=away_team,
            home_goals=home_goals,
            away_goals=away_goals,
            matchday=matchday,
            match_is_finished=match_is_finished,
            match_is_live=match_is_live,
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

    def get_result(self) -> MatchResult:
        if self.home_team_won():
            return MatchResult.HOME_WON
        if self.away_team_won():
            return MatchResult.AWAY_WON
        return MatchResult.DRAW

    def is_in_future(self):
        return not self.match_is_finished and not self.match_is_live

    def get_home_team(self) -> str:
        return self.home_team

    def __repr__(self) -> str:
        return f"{self.home_team} : {self.away_team}"
        # result_str = (
        #     f"{self.home_goals:>3}:{self.away_goals:<3}"
        #     if self.match_is_finished or self.match_is_live
        #     else " - : - "
        # )
        # return f"{self.home_team:>30}{result_str}{self.away_team}"
