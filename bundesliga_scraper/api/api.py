from __future__ import annotations

import requests

from bundesliga_scraper.datatypes.constants import League
from bundesliga_scraper.datatypes.fixture.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.table import table_entry

BASE_URL = "https://api.openligadb.de"


def get_table(league: League, season: int = 2023) -> dict:
    """Fetches the Football table data for a particular league and a season."""
    url = build_get_table_url(league, season)
    response = requests.get(url, timeout=3)
    return response.json()


def build_get_table_url(league: League, season: int = 2023) -> str:
    return f"{BASE_URL}/getbltable/{league}/{season}"


def retrieve_table(league: League, season: int = 2023) -> list[table_entry.TableEntry]:
    data = get_table(league=league, season=season)
    return [table_entry.TableEntry.from_dict(table_entry) for table_entry in data]


def retrieve_all_matchdays(
    league: League, season: int = 2023
) -> dict[int, list[FixtureEntry]]:
    all_fixtures_list = get_match_data(league=league, season=season)

    all_fixtures = [
        FixtureEntry.from_dict(fixture_data) for fixture_data in all_fixtures_list
    ]

    return _extract_season_matchdays(all_fixtures)


def get_match_data(league: League, season: int = 2023, team_filter: str = "") -> dict:
    url = build_get_match_data_url(
        league=league, season=season, team_filter=team_filter
    )
    response = requests.get(url, timeout=3)
    return response.json()


def build_get_match_data_url(
    league: League, season: int = 2023, team_filter: str = ""
) -> str:
    return f"{BASE_URL}/getmatchdata/{league}/{season}/{team_filter}"


def retrieve_team_match_data(
    league: League, team: str, season: int = 2023
) -> list[FixtureEntry]:
    team_data = get_match_data(league=league, team_filter=team, season=season)
    return [FixtureEntry.from_dict(fixture) for fixture in team_data]


def retrieve_current_matchday(league: League) -> int:
    url = build_get_current_matchday_url(league)
    response = requests.get(url, timeout=3)
    data = response.json()
    return int(data["groupOrderID"])


def build_get_current_matchday_url(league: League) -> str:
    return f"{BASE_URL}/getcurrentgroup/{league}"


def build_get_available_teams_url(league: League, season: int = 2023) -> str:
    return f"{BASE_URL}/getavailableteams/{league}/{season}"


def get_available_teams(league: League, season: int = 2023) -> dict:
    url = build_get_available_teams_url(league=league, season=season)
    response = requests.get(url, timeout=3)
    return response.json()


def retrieve_matchday_fixtures(
    league: League, group_order_id: int, season: int = 2023
) -> list[FixtureEntry]:
    fixtures_data = get_matchday_fixtures(league, group_order_id, season)
    return [FixtureEntry.from_dict(data) for data in fixtures_data]


def get_matchday_fixtures(
    league: League, group_order_id: int, season: int = 2023
) -> dict:
    url = build_get_matchday_fixtures(league, group_order_id, season)
    response = requests.get(url, timeout=3)
    return response.json()


def build_get_matchday_fixtures(
    league: League, group_order_id: int, season: int = 2023
) -> str:
    return f"{BASE_URL}/getmatchdata/{league}/{season}/{group_order_id}"


def _extract_season_matchdays(
    all_fixtures: list[FixtureEntry],
) -> list[list[FixtureEntry]]:
    season_matchdays: list[list[FixtureEntry]] = []
    for i in range(1, 35):
        season_matchdays.append([])
    for fixture in all_fixtures:
        matchday = fixture.matchday
        season_matchdays[matchday - 1].append(fixture)

    return season_matchdays


def main() -> None:
    print(retrieve_matchday_fixtures(league=League.Bundesliga, group_order_id=1))


if __name__ == "__main__":
    main()
