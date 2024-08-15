from __future__ import annotations

from datetime import datetime

import requests

from bundesliga_scraper.datatypes.constants import LEAGUE_NAMES, League
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
from bundesliga_scraper.datatypes.matchday import Matchday
from bundesliga_scraper.datatypes.table import Table
from bundesliga_scraper.datatypes.table_entry import TableEntry

BASE_URL = "https://api.openligadb.de"


def get_table(league: League, season: int = 2024) -> dict:
    """Fetches the Football table data for a particular league and a season."""
    url = build_get_table_url(league, season)
    response = requests.get(url, timeout=3)
    return response.json()


def build_get_table_url(league: League, season: int = 2024) -> str:
    return f"{BASE_URL}/getbltable/{league}/{season}"


def retrieve_table(league: League, season: int = 2024) -> list[TableEntry]:
    data = get_table(league=league, season=season)
    return [TableEntry.from_dict(table_entry) for table_entry in data]


def retrieve_all_matchdays(league: League, season: int = 2024) -> list[Matchday]:
    all_fixtures_list = get_match_data(league=league, season=season)

    all_fixtures = [
        FixtureEntry.from_dict(fixture_data) for fixture_data in all_fixtures_list
    ]

    return _extract_season_matchdays(all_fixtures)


def get_match_data(league: League, season: int = 2024, team_filter: str = "") -> dict:
    url = build_get_match_data_url(
        league=league, season=season, team_filter=team_filter
    )
    response = requests.get(url, timeout=3)
    return response.json()


def build_get_match_data_url(
    league: League, season: int = 2024, team_filter: str = ""
) -> str:
    return f"{BASE_URL}/getmatchdata/{league}/{season}/{team_filter}"


def retrieve_team_match_data(
    league: League, team: str, season: int = 2024
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


def build_get_available_teams_url(league: League, season: int = 2024) -> str:
    return f"{BASE_URL}/getavailableteams/{league}/{season}"


def get_available_teams(league: League, season: int = 2024) -> dict:
    url = build_get_available_teams_url(league=league, season=season)
    response = requests.get(url, timeout=3)
    return response.json()


def initialize_league_table(league: League, season: int = 2024) -> Table:
    data = get_available_teams(league=league, season=season)
    teams_dict: dict[str, TableEntry] = {
        entry["teamName"]: TableEntry(entry["teamName"]) for entry in data
    }
    return Table(league_name=LEAGUE_NAMES[league], teams=teams_dict)


def _extract_season_matchdays(all_fixtures: list[FixtureEntry]) -> list[Matchday]:
    season_matchdays: list[Matchday] = []
    for i in range(1, 35):
        season_matchdays.append(Matchday(matchday=i, fixtures=[]))
    for fixture in all_fixtures:
        matchday = fixture.matchday
        season_matchdays[matchday - 1].fixtures.append(fixture)

    return season_matchdays


def main():
    all_fixtures = retrieve_all_matchdays(league=League.Bundesliga)
    matchday = all_fixtures[23]

    print(f"Matchday: {matchday[0].matchday}")
    current_date = datetime.today()
    for fixture in matchday:
        date = fixture.date
        if date != current_date:
            current_date = date
            print(date)
        print(
            f"{fixture.home_team:>30}{fixture.home_goals:>3}:{fixture.away_goals:<3}{fixture.away_team}"
        )


if __name__ == "__main__":
    main()
