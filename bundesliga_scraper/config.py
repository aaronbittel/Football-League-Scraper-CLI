"""Module for all configurations"""

import os
from pathlib import Path

CURRENT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

LEAGUE_TABELS_BASE_URLS = {
    "bundesliga": "https://www.kicker.de/bundesliga/tabelle/2023-24/",
    "2_bundesliga": "https://www.kicker.de/2-bundesliga/tabelle/2023-24/",
}

LEAGUE_FIXTURES_BASE_URLS = {
    "bundesliga": "https://www.bundesliga.com/en/bundesliga/matchday/2023-2024/",
    "2_bundesliga": "https://www.bundesliga.com/en/2bundesliga/matchday/2023-2024/",
}
