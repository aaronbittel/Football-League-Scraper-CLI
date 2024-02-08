"""Module for fetching requested data and extracting information from HTML using 
request
"""

import re
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import requests
from bs4 import BeautifulSoup, element
from colorama import Fore, Style

LEAGUE_TABELS_BASE_URLS = {
    "bundesliga": "https://www.kicker.de/bundesliga/tabelle/2023-24/",
    "2_bundesliga": "https://www.kicker.de/2-bundesliga/tabelle/2023-24/",
}

LEAGUE_FIXTURES_BASE_URLS = {
    "bundesliga": "https://www.bundesliga.com/en/bundesliga/matchday/2023-2024/",
    "2_bundesliga": "https://www.bundesliga.com/en/2bundesliga/matchday/2023-2024/",
}


@dataclass
class TeamTableEntry:
    """Team entry that represents a row in a football table"""

    team_name: str
    points: int
    games: int
    wins: int
    ties: int
    defeats: int
    goals: tuple[int, int]
    diff: int

    def styled_entry(self) -> str:
        """Returns a styled entry of its values"""
        return create_styled_table_entry(self)


@dataclass
class FixtureEntry:
    """Class that represents a fixture entry of a given matchday"""

    home_team: str
    away_team: str
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None

    def styled_entry(self) -> str:
        """Returns a styled entry of its values"""
        return create_styled_fixture_entry(self)


def create_styled_fixture_entry(entry: FixtureEntry) -> str:
    """Sytles the given FixtureEntry"""

    if isinstance(entry.home_goals, int) and isinstance(entry.away_goals, int):
        styled_home_str = f"{Fore.MAGENTA if entry.home_goals > entry.away_goals else Fore.WHITE}{entry.home_team:>30}{entry.home_goals:^3}{Style.RESET_ALL}"  # pyright: ignore[reportGeneralTypeIssues]
        styled_away_str = f"{entry.away_goals:^3}{Fore.MAGENTA if entry.away_goals > entry.home_goals else Fore.WHITE}{entry.away_team}{Style.RESET_ALL}"  # pyright: ignore[reportGeneralTypeIssues]
    else:
        styled_home_str = f"{entry.home_team:>30}{" - ":^3}"
        styled_away_str = f"{" - ":^3}{entry.away_team}"
    return f"{styled_home_str}:{styled_away_str}"


def create_styled_table_entry(entry: TeamTableEntry) -> str:
    """Styles the given TeamTableEntry"""

    repr_str = f"{entry.team_name:<30}{entry.games:^5}{entry.wins:^3}{entry.ties:^3}"
    repr_str += f"{entry.defeats:^3}{entry.goals[0]:>4}:{entry.goals[1]:<4}"
    repr_str += f"{Fore.GREEN if entry.diff >= 0 else Fore.RED}"
    repr_str += f"{entry.diff:+}".center(5)
    repr_str += f"{Style.RESET_ALL}{Style.BRIGHT}{entry.points:^5}{Style.RESET_ALL}"

    return repr_str


def get_table_information(
    league: str, gameday: int, disable_debug: bool = False
) -> list[TeamTableEntry]:
    """Handles getting the table data for the league and specified gameday

    Args:
        league (str): league
        gameday (int): gameday for table
    """
    soup = None
    if disable_debug:
        print("Fetching data from web ...")
        soup = fetch_html(f"{LEAGUE_TABELS_BASE_URLS[league.lower()]}{gameday}")
    else:
        print("Using local file to read data")
        with open("bundesliga_table.txt", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

    return extract_table_information(soup)


def get_fixture_information(
    league: str, gameday: int, disable_debug: bool = False
) -> OrderedDict[datetime, list[FixtureEntry]]:
    """Handles getting the fixture data for the league and the specified gameday"""
    soup = None
    if disable_debug:
        print("Fetching data from the web ...")
        soup = fetch_html(f"{LEAGUE_FIXTURES_BASE_URLS[league.lower()]}{gameday}")
    else:
        print("Using local file to read data")
        if gameday < 21:
            with open("bundesliga_fixture.txt", "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
        else:
            with open("bundesliga_fixture_not_played.txt", "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

    return extract_fixture_information(soup)


def extract_fixture_information(
    soup: BeautifulSoup,
) -> OrderedDict[datetime, list[FixtureEntry]]:
    """Extracts the fixture data from the soup object and returns it as a list of
    FixtureEntries

    Args:
        soup (BeautifulSoup): soup object containing the html

    Returns:
        list[FixtureEntry]: List containing FixtureEntries
    """
    complete_fixture = OrderedDict()
    fixture_component = soup.find(
        "fixturescomponent"
    ).div  # pyright: ignore[reportGeneralTypeIssues, reportOptionalMemberAccess]

    datetime_object = datetime.now()

    for tag in fixture_component.find_all():
        if tag.name == "match-date-header":
            datetime_object = extract_datetime(tag.text)
            complete_fixture[datetime_object] = []

        elif tag.name == "div" and "matchRow" in tag.attrs["class"]:
            complete_fixture[datetime_object].append(extract_match(tag))

    return complete_fixture


def extract_match(tag: element.Tag) -> FixtureEntry:
    """Extract a fixtureEntry from the given tag

    Args:
        tag (element.Tag): div tag

    Returns:
        FixtureEntry: FixtureEntry
    """
    home_team, away_team = [
        clublogo.img["alt"] for clublogo in tag.find_all("clublogo")
    ]

    home_goals, away_goals = [score.text for score in tag.find_all(class_="score")]

    home_goals = re.sub(r"\s+", "", home_goals)
    away_goals = re.sub(r"\s+", "", away_goals)

    if home_goals.isdigit():
        home_goals = int(home_goals)
        away_goals = int(away_goals)
    else:
        home_goals, away_goals = None, None

    return FixtureEntry(
        home_team=home_team,
        away_team=away_team,
        home_goals=home_goals,
        away_goals=away_goals,
    )


def extract_datetime(tag_str: str) -> datetime:
    """Extracting datetime object from a tag"""
    _, _, date_string, time_string, *_ = re.sub(r"\s+", " ", tag_str).split(" ")
    date_object = datetime.strptime(date_string, "%d-%b-%Y").date()
    time_object = datetime.strptime(time_string, "%H:%M").time()

    # plus 1 hour because somehow I get -1 hour
    return datetime.combine(date=date_object, time=time_object) + timedelta(hours=1)


def extract_table_information(soup: BeautifulSoup) -> list[TeamTableEntry]:
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
            td for td in tr.find_all("td", class_="kick__table--ranking__number")
        ]

        wins, ties, defeats = list(
            map(
                int,
                wins_ties_defeats.find(
                    "span", class_="kick__table--show-mobile"
                ).text.split("-"),
            )
        )

        goals = tuple(map(int, goals.text.replace("\n", "").strip().split(":")))

        table_entry = TeamTableEntry(
            team_name=team,
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
