from __future__ import annotations

from enum import StrEnum
from bundesliga_scraper.datatypes.table_entry import TableEntry
from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry
import requests
from datetime import datetime

BASE_URL = "https://api.openligadb.de"


class League(StrEnum):
    Bundesliga = "bl1"
    Bundesliga_2 = "bl2"


def get_table(league: League, season: int = 2023) -> dict:
    """Fetches the Football table data for a particular league and a season."""
    url = build_get_table_url(league, season)
    response = requests.get(url, timeout=3)
    return response.json()


def build_get_table_url(league: League, season: int = 2023) -> str:
    return f"{BASE_URL}/getbltable/{league}/{season}"


def retrieve_table(league: League, season: int = 2023) -> list[TableEntry]:
    data = get_table(league=league, season=season)
    return [TableEntry.from_dict(table_entry) for table_entry in data]


def retrieve_all_fixtures(
    league: League, season: int = 2023
) -> list[list[FixtureEntry]]:
    all_fixtures_list = get_match_data(league=league, season=season)
    all_fixtures = []
    for i in range(34):
        matchday = all_fixtures_list[i * 9 : (i * 9) + 9]
        matchday_fixtures = []
        for fixture in matchday:
            matchday_fixtures.append(FixtureEntry.from_dict(fixture))
        all_fixtures.append(matchday_fixtures)
    return all_fixtures


def get_match_data(league: League, season: int = 2023) -> dict:
    url = build_get_match_data_url(league=league, season=season)
    response = requests.get(url, timeout=3)
    return response.json()


def build_get_match_data_url(league: League, season: int = 2023) -> str:
    return f"{BASE_URL}/getmatchdata/{league}/{season}"


def retrieve_current_matchday(league: League) -> int:
    url = build_get_current_matchday_url(league)
    response = requests.get(url, timeout=3)
    data = response.json()
    return int(data["groupOrderID"])


def build_get_current_matchday_url(league: League) -> str:
    return f"{BASE_URL}/getcurrentgroup/{league}"


def main():
    all_fixtures = retrieve_all_fixtures(league=League.Bundesliga)
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
