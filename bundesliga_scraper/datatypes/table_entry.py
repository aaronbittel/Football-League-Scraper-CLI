"""Module that represents a table entry"""

from dataclasses import dataclass

from bs4 import BeautifulSoup
from colorama import Fore, Style

from bundesliga_scraper import data_fetcher
from bundesliga_scraper.config import CURRENT_DIR, LEAGUE_TABELS_BASE_URLS


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
        soup = data_fetcher.fetch_html(
            f"{LEAGUE_TABELS_BASE_URLS[league.lower()]}{gameday}"
        )
    else:
        print("Using local file to read data")
        with open(CURRENT_DIR / "bundesliga_table.txt", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

    return extract_table_information(soup)


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
