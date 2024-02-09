"""Module representing a fixture entry"""

import re
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime, timedelta

from bs4 import BeautifulSoup, element
from colorama import Back, Fore, Style

from bundesliga_scraper import data_fetcher
from bundesliga_scraper.config import CURRENT_DIR, LEAGUE_FIXTURES_BASE_URLS
from bundesliga_scraper.datatypes.data import FootballData


@dataclass
class FixtureEntry:
    """Class that represents a fixture entry of a given matchday"""

    home_team: str
    away_team: str
    played: bool
    home_goals: int = 0
    away_goals: int = 0

    def styled_entry(self) -> str:
        """Returns a styled entry of its values"""

        if self.played:
            styled_home_str = self.color_home_str() + f"{self.home_goals:^3}"
            styled_away_str = f"{self.away_goals:^3}" + self.color_away_str()
        else:
            styled_home_str = f"{self.home_team:>30}{" - ":^3}"
            styled_away_str = f"{" - ":^3}{self.away_team}"
        return f"{styled_home_str}:{styled_away_str}" + "\n"

    def color_home_str(self) -> str:
        """Determines color for home string

        MAGENTA if home team won else WHITE
        """
        styled_str = (
            f"{Fore.MAGENTA if self.home_goals > self.away_goals else Fore.WHITE}"
        )
        styled_str += f"{self.home_team:>30}{Style.RESET_ALL}"
        return styled_str

    def color_away_str(self) -> str:
        """Determines color for away string

        MAGENTA if away team won else WHITE
        """
        style_str = (
            f"{Fore.MAGENTA if self.away_goals > self.home_goals else Fore.WHITE}"
        )
        style_str += f"{self.away_team}{Style.RESET_ALL}"
        return style_str


class MatchdayFixture(FootballData):
    """Class that represent a Football League fixture

    It has a list of fixture entries and knows how to create a fixture from the html
    source as well as style them as strings
    """

    def __init__(self, league: str, matchday: int, disable_debug: bool = False) -> None:
        self.league = league
        self.matchday = matchday
        self.disable_debug = disable_debug
        self.complete_fixture: OrderedDict[datetime, list[FixtureEntry]] = OrderedDict()

    def load(self) -> None:
        """Loading fixture"""
        soup = None

        if self.disable_debug:
            print("Fetching data from the web ...")
            soup = data_fetcher.fetch_html(
                f"{LEAGUE_FIXTURES_BASE_URLS[self.league.lower()]}{self.matchday}"
            )
        else:
            print("Using local file to read data")
            if self.matchday < 21:
                with open(
                    CURRENT_DIR / "bundesliga_fixture.txt", "r", encoding="utf-8"
                ) as f:
                    soup = BeautifulSoup(f.read(), "html.parser")
            else:
                with open(
                    CURRENT_DIR / "bundesliga_fixture_not_played.txt",
                    "r",
                    encoding="utf-8",
                ) as f:
                    soup = BeautifulSoup(f.read(), "html.parser")

        self._extract_fixture_information(soup)

    def to_styled_string(self) -> str:
        styled_string = ""
        for date, matches in self.complete_fixture.items():
            styled_string += styled_date(date)
            for entry in matches:
                styled_string += entry.styled_entry()
            styled_string += "\n"
        return styled_string

    def _extract_fixture_information(
        self,
        soup: BeautifulSoup,
    ) -> None:
        """Extracts the fixture data from the soup object and returns it as a list of
        FixtureEntries

        Args:
            soup (BeautifulSoup): soup object containing the html

        """
        fixture_comp = soup.find(
            "fixturescomponent"
        ).div  # pyright: ignore[reportGeneralTypeIssues, reportOptionalMemberAccess]

        datetime_object = datetime.now()

        for (
            tag
        ) in fixture_comp.find_all():  # pyright: ignore[reportOptionalMemberAccess]
            if tag.name == "match-date-header":
                datetime_object = extract_datetime(tag.text)
                self.complete_fixture[datetime_object] = []

            elif tag.name == "div" and "matchRow" in tag.attrs["class"]:
                self.complete_fixture[datetime_object].append(extract_match(tag))


def styled_date(date: datetime) -> str:
    """Returns a styled datetime"""
    return (
        f"{Back.LIGHTBLACK_EX + Fore.MAGENTA + Style.BRIGHT} {date} {Style.RESET_ALL}"
        + "\n"
    )


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

    played = False
    if home_goals.isdigit():
        home_goals = int(home_goals)
        away_goals = int(away_goals)
        played = True
    else:
        home_goals, away_goals = 0, 0

    return FixtureEntry(
        home_team=home_team,
        away_team=away_team,
        home_goals=home_goals,
        away_goals=away_goals,
        played=played,
    )


def extract_datetime(tag_str: str) -> datetime:
    """Extracting datetime object from a tag"""
    _, _, date_string, time_string, *_ = re.sub(r"\s+", " ", tag_str).split(" ")
    date_object = datetime.strptime(date_string, "%d-%b-%Y").date()
    time_object = datetime.strptime(time_string, "%H:%M").time()

    # plus 1 hour because somehow I get -1 hour
    return datetime.combine(date=date_object, time=time_object) + timedelta(hours=1)
