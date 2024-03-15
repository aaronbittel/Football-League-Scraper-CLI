import plotext as plt
import random

GAMES = 25

current1, current2 = 0, 0
y1 = []
y2 = []
points_per_matchday1 = random.choices([0, 1, 3], k=GAMES, weights=[1, 2, 5])
points_per_matchday2 = random.choices([0, 1, 3], k=GAMES, weights=[3, 2, 3])

for p1, p2 in zip(points_per_matchday1, points_per_matchday2):
    current1 += p1
    current2 += p2
    y1.append(current1)
    y2.append(current2)

max_y = max(y1[-1], y2[-1])

plt.theme(theme="pro")
plt.xticks(list(range(1, GAMES + 1, 1)))
plt.yticks(list(range(0, max_y + 1, 2)))
plt.scatter(y1)
plt.scatter(y2)
plt.title("Line Plot")
plt.show()
