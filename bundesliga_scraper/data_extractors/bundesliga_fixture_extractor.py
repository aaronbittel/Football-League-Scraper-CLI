"""Extracts Bundesliga fixture information from soup object."""


from datetime import datetime, timedelta

from bs4 import BeautifulSoup, element

from bundesliga_scraper.datatypes.fixture_entry import FixtureEntry


def extract_bundesliga_fixture_information(
    soup: BeautifulSoup,
) -> dict[datetime, list[FixtureEntry]]:
    """Extracts the fixture data and returns it as a list of FixtureEntries.

    Args:
        soup (BeautifulSoup): soup object containing the html

    """
    fixture_component: element.Tag | None = soup.select_one("fixturescomponent > div")

    datetime_object = datetime.now()

    if not fixture_component:
        return None

    complete_fixture: dict[datetime, list[FixtureEntry]] = {}

    for tag in fixture_component.find_all():
        if tag.name == "match-date-header":
            datetime_object = extract_datetime(tag)

            complete_fixture[datetime_object] = []

        elif tag.name == "div" and "matchRow" in tag.attrs["class"]:
            complete_fixture[datetime_object].append(extract_match(tag))

    return complete_fixture


def extract_match(tag: element.Tag) -> FixtureEntry:
    """Extract a fixtureEntry from the given tag.

    Args:
        tag (element.Tag): div tag


    Returns:
        FixtureEntry: FixtureEntry
    """
    home_team, away_team = (
        clublogo.img["alt"] for clublogo in tag.find_all("clublogo")
    )

    home_goals, away_goals = (
        score.get_text(strip=True) for score in tag.find_all(class_="score")
    )

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


def extract_datetime(time_tag: element.Tag) -> datetime:
    """Extracting datetime object from a tag."""
    _, date_string, time_string = time_tag.get_text(" ", strip=True).split(" ")
    date_object = datetime.strptime(date_string, "%d-%b-%Y").date()
    time_object = datetime.strptime(time_string, "%H:%M").time()

    # plus 1 hour because somehow I get -1 hour
    return datetime.combine(date=date_object, time=time_object) + timedelta(hours=1)
