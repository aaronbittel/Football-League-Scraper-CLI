"""Module that represents a Fixture entry"""

from dataclasses import dataclass

from colorama import Fore, Style


@dataclass
class FixtureEntry:
    """Class that represents a fixture entry of a given matchday"""

    home_team: str
    away_team: str
    played: bool
    home_goals: int = 0
    away_goals: int = 0

    def styled_entry(self) -> str:
        """Returns a styled entry of its values"""

        if self.played:
            styled_home_str = self.color_home_str() + f"{self.home_goals:^3}"
            styled_away_str = f"{self.away_goals:^3}" + self.color_away_str()
        else:
            styled_home_str = f"{self.home_team:>30}{" - ":^3}"
            styled_away_str = f"{" - ":^3}{self.away_team}"
        return f"{styled_home_str}:{styled_away_str}" + "\n"

    def color_home_str(self) -> str:
        """Determines color for home string

        MAGENTA if home team won else WHITE
        """
        styled_str = f"{Fore.MAGENTA if self.home_goals > self.away_goals else Fore.WHITE}"
        styled_str += f"{self.home_team:>30}{Style.RESET_ALL}"
        return styled_str

    def color_away_str(self) -> str:
        """Determines color for away string

        MAGENTA if away team won else WHITE
        """
        style_str = f"{Fore.MAGENTA if self.away_goals > self.home_goals else Fore.WHITE}"
        style_str += f"{self.away_team}{Style.RESET_ALL}"
        return style_str
