"""Module representing data."""

from typing import Protocol


class FootballData(Protocol):
    """Class representing data."""

    def load(self) -> None:
        """Loads data."""
        ...

    def to_styled_string(self) -> str:
        """Returns styled representation of the string."""
        ...
