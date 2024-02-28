"""Extracts bundesliga table information from soup object."""


from bs4 import BeautifulSoup

from bundesliga_scraper.datatypes.table_entry import TableEntry


def extract_bundesliga_table_information(soup: BeautifulSoup) -> list[TableEntry]:
    """Extracts the table data and returns it as a list of TableEntries.

    Args:
        soup (BeautifulSoup): soup object containing the html

    """
    table = soup.select_one("table")

    if not table:
        return

    table_entries: list[TableEntry] = []

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

        table_entries.append(
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

    return table_entries
