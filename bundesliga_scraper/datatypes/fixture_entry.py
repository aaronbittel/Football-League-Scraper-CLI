"""Module representing a fixture entry"""

import re
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from bs4 import BeautifulSoup, element
from colorama import Fore, Style

from bundesliga_scraper import data_fetcher
from bundesliga_scraper.config import LEAGUE_FIXTURES_BASE_URLS


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
        styled_home_str = f"{Fore.MAGENTA if entry.home_goals > entry.away_goals else Fore.WHITE}{entry.home_team:>30}{Style.RESET_ALL}{entry.home_goals:^3}"  # pyright: ignore[reportGeneralTypeIssues]
        styled_away_str = f"{entry.away_goals:^3}{Fore.MAGENTA if entry.away_goals > entry.home_goals else Fore.WHITE}{entry.away_team}{Style.RESET_ALL}"  # pyright: ignore[reportGeneralTypeIssues]
    else:
        styled_home_str = f"{entry.home_team:>30}{" - ":^3}"
        styled_away_str = f"{" - ":^3}{entry.away_team}"
    return f"{styled_home_str}:{styled_away_str}"


def get_fixture_information(
    league: str, gameday: int, disable_debug: bool = False
) -> OrderedDict[datetime, list[FixtureEntry]]:
    """Handles getting the fixture data for the league and the specified gameday"""
    soup = None
    if disable_debug:
        print("Fetching data from the web ...")
        soup = data_fetcher.fetch_html(
            f"{LEAGUE_FIXTURES_BASE_URLS[league.lower()]}{gameday}"
        )
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
    fixture_comp = soup.find(
        "fixturescomponent"
    ).div  # pyright: ignore[reportGeneralTypeIssues, reportOptionalMemberAccess]

    datetime_object = datetime.now()

    for tag in fixture_comp.find_all():  # pyright: ignore[reportOptionalMemberAccess]
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
