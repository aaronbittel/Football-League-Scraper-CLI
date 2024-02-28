"""Module that represents a Fixture entry."""

from dataclasses import dataclass


@dataclass
class FixtureEntry:
    """Class that represents a fixture entry of a given matchday."""

    home_team: str
    away_team: str
    played: bool
    home_goals: int = 0
    away_goals: int = 0

    def _home_team_won(self) -> bool:
        """Returns true if home team won.

        Returns:
            bool: true if home team won
        """
        return self.home_goals > self.away_goals
