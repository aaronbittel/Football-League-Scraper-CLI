"""Module that represents a table entry."""

from dataclasses import dataclass

from colorama import Fore, Style


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

    def styled_entry(self, placement: int) -> str:
        """Returns a styled entry of its values."""
        repr_str = f"{placement:<4}"
        repr_str += (
            f"{self.team_name:<30}{self.games:^5}{self.wins:^3}{self.ties:^3}"
        )
        repr_str += f"{self.defeats:^3}{self.goals[0]:>4}:{self.goals[1]:<4}"
        repr_str += self._styled_diff_str()
        repr_str += (
            f"{Style.RESET_ALL}{Style.BRIGHT}{self.points:^5}{Style.RESET_ALL}"
        )

        return repr_str

    def _styled_diff_str(self) -> str:
        """Returns a styled diff string based on the number

        Green if > 0, White == 0 and Red < 0
        """
        repr_str = ""
        if self.diff > 0:
            repr_str += f"{Fore.GREEN}"
        elif self.diff < 0:
            repr_str += f"{Fore.RED}"
        else:
            repr_str += f"{Fore.WHITE}"
        repr_str += f"{self.diff:+}".center(5)
        return repr_str + f"{Style.RESET_ALL}"
