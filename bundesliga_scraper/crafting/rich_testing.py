from rich.console import Console
from rich.panel import Panel

WINNING_STYLE = "[bold pale_green3]"
WINNING_STYLE_END = f"[/{WINNING_STYLE[1:]}"
HIGHLIGHT_STYLE = "[on orange3]"
HIGHLIGHT_STYLE_END = f"[/{HIGHLIGHT_STYLE[1:]}"

WIDTH = 70
NAME_SPACE = (WIDTH - 3) // 2
NAME_SPACE_2 = (WIDTH - 7) // 2

bayern = "FC Bayern München 8"
mainz = "1 Mainz 05"

dortmund = "2 Borussia Dortmund"
bremen = "SV Werder Bremen 1"

match1 = f"{WINNING_STYLE}{HIGHLIGHT_STYLE}{bayern.rjust(NAME_SPACE)}{WINNING_STYLE_END}{":":^3}{mainz.ljust(NAME_SPACE)}{HIGHLIGHT_STYLE_END}"
match2 = f"{bremen.rjust(NAME_SPACE)}{":":^3}{WINNING_STYLE}{dortmund.ljust(NAME_SPACE)}{WINNING_STYLE_END}"
match3 = (
    f"{bayern[:-2].rjust(NAME_SPACE_2)}{"- : -":^7}{dortmund[2:].ljust(NAME_SPACE_2)}"
)

total = "\n".join((match1, match2, match3))

panel = Panel(total, title="Bundesliga Matchday 25", width=WIDTH, padding=1)
console = Console()
console.print(panel)

string = """20:30
[bold pale_green3]              VfB Stuttgart 2[/bold pale_green3] : 0 1. FC Union Berlin"""

console.print(Panel(string))
