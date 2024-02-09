"""Module that represents a table entry"""

from dataclasses import dataclass

from bs4 import BeautifulSoup
from colorama import Back, Fore, Style

from bundesliga_scraper import data_fetcher
from bundesliga_scraper.config import CURRENT_DIR, LEAGUE_TABELS_BASE_URLS
from bundesliga_scraper.datatypes.data import FootballData


@dataclass
class TableEntry:
    """Team entry that represents a row in a football table"""

    team_name: str
    points: int
    games: int
    wins: int
    ties: int
    defeats: int
    goals: tuple[int, int]
    diff: int

    def styled_entry(self, placement: int) -> str:
        """Returns a styled entry of its values"""
        repr_str = f"{placement:<4}"
        repr_str += f"{self.team_name:<30}{self.games:^5}{self.wins:^3}{self.ties:^3}"
        repr_str += f"{self.defeats:^3}{self.goals[0]:>4}:{self.goals[1]:<4}"
        repr_str += f"{Fore.GREEN if self.diff >= 0 else Fore.RED}"
        repr_str += f"{self.diff:+}".center(5)
        repr_str += f"{Style.RESET_ALL}{Style.BRIGHT}{self.points:^5}{Style.RESET_ALL}"

        return repr_str


class MatchdayTable(FootballData):
    """Class representing a Football table"""

    def __init__(self, league: str, matchday: int, disable_debug: bool = False) -> None:
        self.league = league
        self.matchday = matchday
        self.disable_debug = disable_debug
        self.table_entries: list[TableEntry] = []

    def load(self) -> None:
        soup = None
        if self.disable_debug:
            print("Fetching data from web ...")
            soup = data_fetcher.fetch_html(
                f"{LEAGUE_TABELS_BASE_URLS[self.league.lower()]}{self.matchday}"
            )
        else:
            print("Using local file to read data")
            with open(CURRENT_DIR / "bundesliga_table.txt", "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

        self._extract_table_information(soup)

    def _styled_table_columns(self) -> str:
        """Returns a styled string representation of the table columns"""
        styled_column_str = f"{Back.LIGHTBLACK_EX + Fore.MAGENTA + Style.BRIGHT}{"Matches":>37}"
        styled_column_str += f"{"W":>4}{"T":>3}{"D":>3}{"Goals":>8}{"+/-":>6}{"P":>4}"
        styled_column_str += f"{Style.RESET_ALL}"
        return styled_column_str + "\n"

    def to_styled_string(self) -> str:
        style_string = self._styled_table_columns()
        style_string += "\n".join(
            entry.styled_entry(placement)
            for placement, entry in enumerate(self.table_entries, start=1)
        )
        return style_string

    def _extract_table_information(self, soup: BeautifulSoup) -> None:
        """Extracts the table data from the soup object and returns it as a list of
        TableEntries

        Args:
            soup (BeautifulSoup): soup object containing the html

        """
        table = soup.find("table")
        trs = table.find_all(  # pyright: ignore[reportGeneralTypeIssues, reportOptionalMemberAccess]
            "tr"
        )

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

            self.table_entries.append(
                TableEntry(
                    team_name=team,
                    points=wins * 3 + ties,
                    games=wins + ties + defeats,
                    wins=wins,
                    ties=ties,
                    defeats=defeats,
                    goals=goals,  # pyright: ignore[reportGeneralTypeIssues]
                    diff=goals[0] - goals[1],
                )
            )
