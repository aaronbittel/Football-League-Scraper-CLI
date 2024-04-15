from rich import panel
from bundesliga_scraper.datatypes.fixture.fixture_creation import (
    LOSING_STYLE,
    LOSING_STYLE_END,
    MATCH_SEPERATOR,
    NEUTRAL_STYLE,
    NEUTRAL_STYLE_END,
    WINNING_STYLE,
    WINNING_STYLE_END,
)
from bundesliga_scraper.datatypes.fixture import fixture_entry


def create_team_components(
    team_name: str,
    results_fixtures: list[fixture_entry.FixtureEntry],
    future_fixtures: list[fixture_entry.FixtureEntry],
) -> tuple[panel.Panel, panel.Panel]:
    results_panel_content = get_results_string(team_name, results_fixtures)
    result_panel = panel.Panel(
        renderable=results_panel_content, title="Results", padding=1
    )

    fixtures_panel_content = get_fixtures_string(team_name, future_fixtures)
    fixture_panel = panel.Panel(
        renderable=fixtures_panel_content, title="Fixtures", padding=1
    )

    height_diff = results_panel_content.count("\n") - fixtures_panel_content.count("\n")
    if height_diff > 0:
        fixture_panel.renderable += "\n" * height_diff
    else:
        result_panel.renderable += "\n" * abs(height_diff)

    return result_panel, fixture_panel


def get_results_string(
    team_name: str, results_fixtures: list[fixture_entry.FixtureEntry]
) -> str:
    max_home_length = max(len(result.home_team) for result in results_fixtures)
    max_away_length = max(len(result.away_team) for result in results_fixtures)

    return "\n\n".join(
        get_result_string(team_name, result, max_home_length, max_away_length)
        for result in results_fixtures
    )


def get_style(team_name: str, result: fixture_entry.FixtureEntry) -> tuple[str, str]:
    if team_name in result.home_team:
        if result.home_team_won():
            return WINNING_STYLE, WINNING_STYLE_END
        elif result.away_team_won():
            return LOSING_STYLE, LOSING_STYLE_END
        return NEUTRAL_STYLE, NEUTRAL_STYLE_END
    else:
        if result.away_team_won():
            return WINNING_STYLE, WINNING_STYLE_END
        elif result.home_team_won():
            return LOSING_STYLE, LOSING_STYLE_END
        return NEUTRAL_STYLE, NEUTRAL_STYLE_END


def get_result_string(
    team_name: str,
    result_fixture: fixture_entry.FixtureEntry,
    max_length: int,
    max_away_length: int,
) -> str:
    style_open, style_closing = get_style(team_name, result_fixture)

    home_goal_string = f"[o u]| {result_fixture.home_goals} |[/]"
    away_goal_string = f"[o u]| {result_fixture.away_goals} |[/]"

    if team_name in result_fixture.home_team:
        return f"{style_open}{result_fixture.home_team.rjust(max_length)} {home_goal_string}{style_closing}{MATCH_SEPERATOR}{away_goal_string} {result_fixture.away_team.ljust(max_away_length)} ({result_fixture.matchday})"
    return f"{result_fixture.home_team.rjust(max_length)} {home_goal_string}{MATCH_SEPERATOR}{style_open}{away_goal_string} {result_fixture.away_team.ljust(max_away_length)}{style_closing} ({result_fixture.matchday})"


def get_fixtures_string(
    team_name: str, future_fixtures: list[fixture_entry.FixtureEntry]
) -> str:
    max_home_length = max(len(fixture.home_team) for fixture in future_fixtures)
    max_away_length = max(len(fixture.away_team) for fixture in future_fixtures)

    return "\n\n".join(
        get_fixture_string(team_name, fixture, max_home_length, max_away_length)
        for fixture in future_fixtures
    )


def get_fixture_string(
    team_name: str,
    fixture: fixture_entry.FixtureEntry,
    max_length: int,
    max_away_length: int,
) -> str:
    match_seperator = " [u o]| - |[/] : [u o]| - |[/] "

    if team_name in fixture.home_team:
        return f"{NEUTRAL_STYLE}{fixture.home_team.rjust(max_length)}{NEUTRAL_STYLE_END}{match_seperator}{fixture.away_team.ljust(max_away_length)} ({fixture.matchday})"
    return f"{fixture.home_team.rjust(max_length)}{match_seperator}{NEUTRAL_STYLE}{fixture.away_team.ljust(max_away_length)}{NEUTRAL_STYLE_END} ({fixture.matchday})"
