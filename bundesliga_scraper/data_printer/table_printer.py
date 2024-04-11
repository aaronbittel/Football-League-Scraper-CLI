"""Creating colorful strings of matchday table information."""

from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table
from rich.style import Style

from bundesliga_scraper.datatypes.table_entry import TableEntry


HEADER_STYLE = Style(bold=False)
DEFAULT_COLUMN_SETTINGS = {"justify": "center", "header_style": Style(bold=False)}
HIGHLIGHT_STYLE = "white on orange3"


def print_table_entries(
    title: str, table_list: list[TableEntry], highlights: list[str]
) -> None:
    print()
    table = create_table(title)
    add_rows(table, table_list, highlights)

    console = Console()
    console.print(table)


def create_table(title: str, last_5: bool = True) -> Table:
    table = Table(
        title=title,
        box=ROUNDED,
        # show_lines=True,
    )

    table.add_column("#", style="bold", header_style=HEADER_STYLE)
    table.add_column("Team", header_style=HEADER_STYLE)
    table.add_column("Matches", **DEFAULT_COLUMN_SETTINGS)
    table.add_column("W", **DEFAULT_COLUMN_SETTINGS)
    table.add_column("D", **DEFAULT_COLUMN_SETTINGS)
    table.add_column("L", **DEFAULT_COLUMN_SETTINGS)
    table.add_column("Goals", **DEFAULT_COLUMN_SETTINGS)
    table.add_column("+/-", **DEFAULT_COLUMN_SETTINGS)
    table.add_column(
        "Points", justify="center", header_style=HEADER_STYLE, style=Style(bold=True)
    )
    if last_5:
        table.add_column("Last 5", **DEFAULT_COLUMN_SETTINGS)

    return table


def add_rows(
    table: Table,
    table_entries: list[TableEntry],
    highlights: list[str],
    place: int = None,
) -> None:
    for placement, entry in enumerate(table_entries, start=1):
        style = ""
        if place is not None and not (place - 2 <= placement <= place + 3):
            continue
        if any(highlight in entry.team_name for highlight in highlights):
            style = HIGHLIGHT_STYLE
        goal_diff = determine_goal_diff_color(entry.goal_diff)
        placement = determine_placement_string(
            placement, entry.get_standings_direction().value
        )

        if place is None:
            table.add_row(
                str(placement),
                str(entry.team_name),
                str(entry.matches),
                str(entry.won),
                str(entry.draw),
                str(entry.lost),
                f"{entry.goals}:{entry.opponent_goals}",
                goal_diff,
                str(entry.points),
                # gets the results of the last 5 matches in reversed order
                "".join(entry.history.matches[:-6:-1]),
                style=style,
            )
        else:
            table.add_row(
                str(placement),
                str(entry.team_name),
                str(entry.matches),
                str(entry.won),
                str(entry.draw),
                str(entry.lost),
                f"{entry.goals}:{entry.opponent_goals}",
                goal_diff,
                str(entry.points),
                style=style,
            )


def determine_goal_diff_color(goal_diff: int) -> str:
    if goal_diff < 0:
        colored_goal_diff = str(f"[red]{goal_diff}")
    elif goal_diff > 0:
        colored_goal_diff = str(f"[green]{goal_diff}")
    else:
        colored_goal_diff = str(f"[white]{goal_diff}")
    return colored_goal_diff


def determine_placement_string(placement: int, directions_symbol: str) -> str:
    return (
        f"{placement}  {directions_symbol}"
        if placement <= 9
        else f"{placement} {directions_symbol}"
    )
