from bundesliga_scraper.datatypes.table_entry import TableEntry
from bundesliga_scraper.table.parser import TableRequestJob
from rich import table as t, box, style

HEADER_STYLE = style.Style(bold=False)
DEFAULT_COLUMN_SETTINGS = {"justify": "center", "header_style": style.Style(bold=False)}
HIGHLIGHT_STYLE = "white on orange3"


def create_table(table_request_job: TableRequestJob) -> t.Table:
    table = t.Table(
        title=table_request_job.title,
        box=box.ROUNDED,
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
        "Points",
        justify="center",
        header_style=HEADER_STYLE,
        style=style.Style(bold=True),
    )
    table.add_column("Last 5", **DEFAULT_COLUMN_SETTINGS)

    add_rows(table, table_request_job.standings, table_request_job.highlights)
    return table


def add_rows(
    table: t.Table, standings: list[TableEntry], highlights: list[str]
) -> None:
    for placement, team in enumerate(standings, start=1):
        style = ""
        if any(highlight.lower() in team.team_name.lower() for highlight in highlights):
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
