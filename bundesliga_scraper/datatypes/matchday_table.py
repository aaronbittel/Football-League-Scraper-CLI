"""Module that represents a table entry."""

from bs4 import BeautifulSoup
from colorama import Back, Fore, Style

from bundesliga_scraper import data_fetcher
from bundesliga_scraper.config import LEAGUE_TABELS_BASE_URLS
from bundesliga_scraper.datatypes.data import FootballData
from bundesliga_scraper.datatypes.table_entry import TableEntry


class MatchdayTable(FootballData):
    """Class representing a Football table."""

    def __init__(self, league: str, matchday: int) -> None:
        """Initializing MatchdayTable.

        Args:
            league (str): name of the Football league
            matchday (int): matchday of table
        """
        self.league = league
        self.matchday = matchday
        self.table_entries: list[TableEntry] = []

    def load(self) -> None:
        """Loads data from the web."""
        print("Fetching data from web ...")
        soup = data_fetcher.fetch_html(
            f"{LEAGUE_TABELS_BASE_URLS[self.league.lower()]}{self.matchday}"
        )
        self._extract_table_information(soup)

    def _styled_table_columns(self) -> str:
        """Returns a styled string representation of the table columns."""
        styled_column_str = (
            f"{Back.LIGHTBLACK_EX + Fore.MAGENTA + Style.BRIGHT}{"Matches":>37}"
        )
        styled_column_str += f"{"W":>4}{"T":>3}{"D":>3}{"Goals":>8}{"+/-":>6}{"P":>4}"
        styled_column_str += f"{Style.RESET_ALL}"
        return styled_column_str + "\n"

    def to_styled_string(self) -> str:
        """Returns a styled matchday string representation."""
        style_string = self._styled_table_columns()
        style_string += "\n".join(
            entry.styled_entry(placement)
            for placement, entry in enumerate(self.table_entries, start=1)
        )
        return style_string

    def _extract_table_information(self, soup: BeautifulSoup) -> None:
        """Extracts the table data and returns it as a list of TableEntries.

        Args:
            soup (BeautifulSoup): soup object containing the html

        """
        table = soup.select_one("table")

        if not table:
            return

        for tr in table.find_all("tr")[1:]:  # first table row is column information
            team_name = tr.find("img")["alt"]

            _, wins_ties_defeats, _, _, goals, _, *_ = (
                td for td in tr.find_all("td", class_="kick__table--ranking__number")
            )

            wins, ties, defeats = list(
                map(
                    int,
                    wins_ties_defeats.find(
                        "span", class_="kick__table--show-mobile"
                    ).text.split("-"),
                )
            )

            goals = tuple(map(int, goals.get_text(strip=True).split(":")))

            self.table_entries.append(
                TableEntry(
                    team_name=team_name,
                    points=wins * 3 + ties,
                    games=wins + ties + defeats,
                    wins=wins,
                    ties=ties,
                    defeats=defeats,
                    goals=goals,
                    diff=goals[0] - goals[1],
                )
            )
