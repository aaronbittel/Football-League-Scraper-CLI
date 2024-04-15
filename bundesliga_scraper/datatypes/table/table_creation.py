from dataclasses import dataclass, field
from rich import style, box, table as rich_table
from bundesliga_scraper.datatypes.table import table_entry

HEADER_STYLE = style.Style(bold=False)
DEFAULT_COLUMN_SETTINGS = {"justify": "center", "header_style": style.Style(bold=False)}
HIGHLIGHT_STYLE = "white on orange3"


@dataclass(frozen=True)
class TableCreationJob:
    title: str
    standings: list[table_entry.TableEntry] = field(default_factory=list)
    highlights: list[str] = None
    focus: int = None


def create_table(table_creation_job: TableCreationJob) -> rich_table.Table:
    table = rich_table.Table(
        title=table_creation_job.title,
        box=box.ROUNDED,
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
        "Points",
        justify="center",
        header_style=HEADER_STYLE,
        style=style.Style(bold=True),
    )
    table.add_column("Last 5", **DEFAULT_COLUMN_SETTINGS)

    add_rows(table, table_creation_job)
    return table


def add_rows(table: rich_table.Table, table_creation_job: TableCreationJob) -> None:
    standings = table_creation_job.standings
    focus = table_creation_job.focus
    highlights = table_creation_job.highlights
    for placement, team in enumerate(standings, start=1):
        style = ""
        if focus is not None and not (focus - 2 <= placement <= focus + 3):
            continue
        if focus == placement:
            style = HIGHLIGHT_STYLE
        if highlights and any(
            highlight.lower() in team.team_name.lower() for highlight in highlights
        ):
            style = HIGHLIGHT_STYLE

        goal_diff_str = determine_goal_diff_color(team.goal_diff)
        placement_str = determine_placement_string(
            placement, team.get_standings_direction().value
        )

        table.add_row(
            placement_str,
            str(team.team_name),
            str(team.matches),
            str(team.won),
            str(team.draw),
            str(team.lost),
            f"{team.goals}:{team.opponent_goals}",
            goal_diff_str,
            str(team.points),
            "".join(team.get_last_5()),
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
