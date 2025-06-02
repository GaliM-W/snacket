import matplotlib.pyplot as plt 
import numpy as np
from Generations import Epoch

winning_snakes, all_snakes = Epoch(
    1000,
    5,
    100,
    num_snakes=10,
    size=25,
    food_delay=3,
    initial_growth=3,
    food_threshold=70,
    display=None
)

print(len(winning_snakes))
for gen in winning_snakes:
    print(gen)
    print(len(gen))

time = []
score = []
age = []
snakes_eaten = []
fitnesses = []

for i in range(len(winning_snakes)):
    for sn in winning_snakes[i]:
        time.append(i)
        score.append(sn.score)
        age.append(sn.age)
        snakes_eaten.append(sn.snakes_eaten)
        fitnesses.append(sum(sn.fitness[1:3]) + 1 if sn.fitness[0] == True else sum(sn.fitness[1:3]))

print(fitnesses)

x = time
y = score

plt.scatter(x, y, alpha=0.1)
plt.xlabel("Generations")
plt.ylabel("Score")
plt.title("Score of winning snagents over Time")



z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), "r--", alpha=0.8, label='Trendline')

plt.show()

x = time
y = age

plt.scatter(x, y, alpha=0.1)
plt.xlabel("Generations")
plt.ylabel("Score")
plt.title("Age of winning snagents over Time")



z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), "r--", alpha=0.8, label='Trendline')

x = time
y = fitnesses

plt.show()

plt.scatter(x, y, alpha=0.1)
plt.xlabel("Generations")
plt.ylabel("Score")
plt.title("Fitness of winning snagents over Time")



z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), "r--", alpha=0.8, label='Trendline')

plt.show()