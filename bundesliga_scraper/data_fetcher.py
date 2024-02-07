"""Module for fetching requested data and extracting information from HTML using 
request
"""

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class TableEntry:
    team: str
    points: int
    games: int
    wins: int
    ties: int
    defeats: int
    goals: tuple[int, int]
    diff: int


LEAGUE_TABELS_BASE_URLS = {
    "bundesliga": "https://www.kicker.de/bundesliga/tabelle/2023-24/",
    "2_bundesliga": "https://www.kicker.de/2-bundesliga/tabelle/2023-24/",
}


def get_table_information(league: str, gameday: int):
    """Handles getting the table data for the league and specified gameday

    Args:
        league (str): league
        gameday (int): gameday for table
    """
    soup = None
    # soup = fetch_html(f"{LEAGUE_TABELS_BASE_URLS[league.lower()]}{gameday}")
    with open("bundesliga_table.txt", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    return extract_table_information(soup)


def extract_table_information(soup: BeautifulSoup) -> list[TableEntry]:
    """Extracts the table data from the soup object and returns it as a list of
    TableEntries

    Args:
        soup (BeautifulSoup): soup object containing the html

    Returns:
        list[TableEntry]: List containing TableEntries, first entry -> top 1
    """
    table = soup.find("table")
    trs = table.find_all(  # pyright: ignore[reportGeneralTypeIssues, reportOptionalMemberAccess]
        "tr"
    )

    table_entries = []

    for tr in trs[1:]:  # first table row is column information
        team = tr.find("img")["alt"]
        _, wins_ties_defeats, _, _, goals, _, *_ = [
            td.text for td in tr.find_all("td", class_="kick__table--ranking__number")
        ]

        wins, ties, defeats = list(
            map(
                int,
                wins_ties_defeats.replace("\n", "").strip().split(" ")[0].split("-"),
            )
        )

        goals = tuple(map(int, goals.replace("\n", "").strip().split(":")))

        table_entry = TableEntry(
            team=team,
            points=wins * 3 + ties,
            games=wins + ties + defeats,
            wins=wins,
            ties=ties,
            defeats=defeats,
            goals=goals,  # pyright: ignore[reportGeneralTypeIssues]
            diff=goals[0] - goals[1],
        )

        table_entries.append(table_entry)

    return table_entries


def fetch_html(url: str) -> BeautifulSoup:
    """Fetching the html for the given url

    Args:
        url (str): url

    Returns:
        BeautifulSoup: Beautifulsoup object
    """
    response = requests.get(url, timeout=10)

    # TODO Handle response.status_code != 200

    return BeautifulSoup(response.text, "html.parser")
