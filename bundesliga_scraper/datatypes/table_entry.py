"""Module that represents a table entry."""

from __future__ import annotations
from dataclasses import dataclass
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry, Result


@dataclass
class TableEntry:
    team_name: str
    points: int = 0
    opponent_goals: int = 0
    goals: int = 0
    matches: int = 0
    won: int = 0
    lost: int = 0
    draw: int = 0
    goal_diff: int = 0

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

    def update(self, fixture: FixtureEntry) -> None:
        match_result: Result = fixture.get_result()

        if self.team_name == fixture.get_home_team():
            self.goals += fixture.home_goals
            self.opponent_goals += fixture.away_goals
            if match_result == Result.HOME_WON:
                self.points += 3
                self.won += 1
            elif match_result == Result.AWAY_WON:
                self.lost += 1
            else:
                self.points += 1
                self.draw += 1
        else:
            self.goals += fixture.away_goals
            self.opponent_goals += fixture.home_goals
            if match_result == Result.HOME_WON:
                self.lost += 1
            elif match_result == Result.AWAY_WON:
                self.points += 3
                self.won += 1
            else:
                self.points += 1
                self.draw += 1

        self.matches += 1
        self.goal_diff = self.goals - self.opponent_goals

    def __lt__(self, other: TableEntry) -> bool:
        if self.points < other.points:
            return True
        if self.points == other.points and self.goal_diff < other.goal_diff:
            return True
        return False

    def __gt__(self, other: TableEntry) -> bool:
        if self.points > other.points:
            return True
        if self.points == other.points and self.goal_diff > other.goal_diff:
            return True
        return False

    def __eq__(self, other: TableEntry) -> bool:
        return self.points == other.points and self.goal_diff == other.goal_diff
