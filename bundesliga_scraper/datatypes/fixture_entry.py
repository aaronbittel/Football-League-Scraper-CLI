"""Module that represents a Fixture entry."""

from dataclasses import dataclass

from colorama import Fore, Style


@dataclass
class FixtureEntry:
    """Class that represents a fixture entry of a given matchday."""

    home_team: str
    away_team: str
    played: bool
    home_goals: int = 0
    away_goals: int = 0

    def styled_entry(self) -> str:
        """Returns a styled entry of its values."""
        if self.played:
            styled_home_str = self.color_home_str() + f"{self.home_goals:^3}"
            styled_away_str = f"{self.away_goals:^3}" + self.color_away_str()
        else:
            styled_home_str = f"{self.home_team:>30}{" - ":^3}"
            styled_away_str = f"{" - ":^3}{self.away_team}"
        return f"{styled_home_str}:{styled_away_str}" + "\n"

    def color_home_str(self) -> str:
        """Determines color for home string.

        MAGENTA if home team won else WHITE
        """
        home_won = self._home_team_won()
        styled_str = f"{Fore.MAGENTA if home_won else Fore.WHITE}"
        styled_str += f"{self.home_team:>30}{Style.RESET_ALL}"
        return styled_str

    def color_away_str(self) -> str:
        """Determines color for away string.

        MAGENTA if away team won else WHITE
        """
        away_won = not self._home_team_won()
        style_str = f"{Fore.MAGENTA if away_won else Fore.WHITE}"
        style_str += f"{self.away_team}{Style.RESET_ALL}"
        return style_str

    def _home_team_won(self) -> bool:
        """Returns true if home team won.

        Returns:
            bool: true if home team won
        """
        return self.home_goals > self.away_goals