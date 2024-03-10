from rich import print as rprint
from random import choices

win = "✅"
lose = "❌"
draw = "➖"

rprint("".join(choices((win, lose, draw), k=5)))
