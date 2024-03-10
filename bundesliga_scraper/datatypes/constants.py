from enum import Enum, StrEnum, auto


class League(StrEnum):
    Bundesliga = "bl1"
    Bundesliga_2 = "bl2"


class MatchResult(Enum):
    HOME_WON = auto()
    AWAY_WON = auto()
    DRAW = auto()


class ResultSymbol(Enum):
    WIN = "✅"
    LOSE = "❌"
    DRAW = "➖"
