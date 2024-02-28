"""Creating colorful strings of matchday fixture information."""


from datetime import datetime

from colorama import Back, Fore, Style

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry


def styled_bundesliga_fixure(fixture: dict[datetime, list[FixtureEntry]]) -> str:
    """Returns a styled string representation of the matchday fixture."""
    styled_string = ""

    for date, matches in fixture.items():
        styled_string += styled_date(date)

        for fixture_entry in matches:
            styled_string += styled_entry(fixture_entry)

        styled_string += "\n"

    return styled_string


def styled_date(date: datetime) -> str:
    """Returns a styled datetime."""
    return (
        f"{Back.LIGHTBLACK_EX + Fore.MAGENTA + Style.BRIGHT} {date} {Style.RESET_ALL}"
        + "\n"
    )


def styled_entry(fixture_entry: FixtureEntry) -> str:
    """Returns a styled entry of its values."""
    if fixture_entry.played:
        styled_home_str = (
            color_home_str(fixture_entry) + f"{fixture_entry.home_goals:^3}"
        )

        styled_away_str = f"{fixture_entry.away_goals:^3}" + color_away_str(
            fixture_entry
        )

    else:
        styled_home_str = f"{fixture_entry.home_team:>30}{" - ":^3}"

        styled_away_str = f"{" - ":^3}{fixture_entry.away_team}"

    return f"{styled_home_str}:{styled_away_str}" + "\n"


def color_home_str(fixture_entry: FixtureEntry) -> str:
    """Determines color for home string.

    MAGENTA if home team won else WHITE
    """
    home_won = fixture_entry._home_team_won()

    styled_str = f"{Fore.MAGENTA if home_won else Fore.WHITE}"

    styled_str += f"{fixture_entry.home_team:>30}{Style.RESET_ALL}"
    return styled_str


def color_away_str(fixture_entry: FixtureEntry) -> str:
    """Determines color for away string.

    MAGENTA if away team won else WHITE
    """
    away_won = not fixture_entry._home_team_won()

    style_str = f"{Fore.MAGENTA if away_won else Fore.WHITE}"

    style_str += f"{fixture_entry.away_team}{Style.RESET_ALL}"
    return style_str
