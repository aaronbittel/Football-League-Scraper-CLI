from random import randint

from rich import print
from rich import print as rprint
from rich.console import Console
from rich.highlighter import Highlighter
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

grid = Table.grid(expand=True)
grid.add_column()
grid.add_column(justify="right")
grid.add_row("Raising shields", "[bold magenta]COMPLETED [green]:heavy_check_mark:")

rprint(grid)


table = Table(title="Bundesliga Matchday 25")

table.add_column("#", justify="center", style="cyan", no_wrap=True)
table.add_column("Team")
table.add_column("SP.", justify="center")
table.add_column("S", justify="center")
table.add_column("U", justify="center")
table.add_column("N", justify="center")
table.add_column("Tore", justify="center")
table.add_column("Diff", justify="center", style="green")
table.add_column("Punkte", justify="center")

style = "bold magenta on white"

table.add_row("1", "Bayer 04 Leverkusen", "14", "11", "3", "0", "39:12", "27", "36")
table.add_row(
    Text.assemble("2", style=style),
    Text.assemble("FC Bayern München", style=style),
    Text.assemble("13", style=style),
    Text.assemble("10", style=style),
    Text.assemble("2", style=style),
    Text.assemble("1", style=style),
    Text.assemble("44:14", style=style),
    Text.assemble("30", style=style),
    Text.assemble("32", style=style),
)
table.add_row("3", "VfB Stuttgart", "14", "10", "1", "3", "34:16", "18", "31")
table.add_row("14", "Borussia Dortmund", "14", "7", "4", "3", "28:23", "[red]-5", "25")

console = Console()
console.print(table)


class RainbowHighlighter(Highlighter):
    def highlight(self, text):
        for index in range(len(text)):
            text.stylize(f"color({randint(16, 255)})", index, index + 1)


rainbow = RainbowHighlighter()
rprint(rainbow("I must not fear. Fear is the mind-killer."))

panel = Panel(Text("Hello", justify="right"))
print(panel)

console.print("Danger, Will Robinson!", style="blink bold red underline on white")
