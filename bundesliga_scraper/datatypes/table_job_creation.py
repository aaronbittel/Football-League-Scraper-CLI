from dataclasses import dataclass, field
from bundesliga_scraper.datatypes import table_entry


@dataclass(frozen=True)
class TableCreationJob:
    title: str
    standings: list[table_entry.TableEntry] = field(default_factory=list)
    highlights: list[str] = field(default_factory=list)
    focus: int = None
