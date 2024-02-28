"""Creating colorful strings of matchday table information."""

from colorama import Back, Fore, Style

from bundesliga_scraper.datatypes.table_entry import TableEntry


def styled_bundesliga_table_information(table_entries: list[TableEntry]) -> str:
    """Returns a styled string reprensentation of a bundesliga matchday table.

    Args:
        table_entries (list[TableEntry]): Bundesliga teams' table information
    """
    styled_table_column_string = styled_table_columns()
    styled_table_entries_string = styled_table_entries(table_entries)
    return f"{styled_table_column_string}{styled_table_entries_string}"


def styled_table_columns() -> str:
    """Returns a styled string representation of the table columns."""
    styled_column_str = (
        f"{Back.LIGHTBLACK_EX + Fore.MAGENTA + Style.BRIGHT}{"Matches":>37}"
    )
    styled_column_str += f"{"W":>4}{"T":>3}{"D":>3}{"Goals":>8}{"+/-":>6}{"P":>4}"
    styled_column_str += f"{Style.RESET_ALL}"
    return styled_column_str + "\n"


def styled_table_entries(table_entries: list[TableEntry]) -> str:
    """Returns a styled matchday string representation."""
    return "\n".join(
        styled_table_entry(entry, placement)
        for placement, entry in enumerate(table_entries, start=1)
    )


def styled_table_entry(table_entry: TableEntry, placement: int) -> str:
    """Returns a styled entry of its values."""
    repr_str = f"{placement:<4}"
    repr_str += f"{table_entry.team_name:<30}{table_entry.games:^5}"
    repr_str += f"{table_entry.wins:^3}{table_entry.ties:^3}"
    repr_str += (
        f"{table_entry.defeats:^3}{table_entry.goals[0]:>4}:{table_entry.goals[1]:<4}"
    )
    repr_str += styled_diff_str(table_entry.diff)
    repr_str += (
        f"{Style.RESET_ALL}{Style.BRIGHT}{table_entry.points:^5}{Style.RESET_ALL}"
    )

    return repr_str


def styled_diff_str(diff: int) -> str:
    """Returns a styled diff string based on the number.

    Green if > 0, White == 0 and Red < 0

    Args:
        diff (int): difference goals scored and goals received
    """
    repr_str = ""
    if diff > 0:
        repr_str += f"{Fore.GREEN}"
    elif diff < 0:
        repr_str += f"{Fore.RED}"
    else:
        repr_str += f"{Fore.WHITE}"
    repr_str += f"{diff:+}".center(5)
    return repr_str + f"{Style.RESET_ALL}"
