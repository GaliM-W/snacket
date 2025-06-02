from Generations import Epoch
from itertools import product
from statistics import mean


def make_trial(trial):
    return {var: val for var, val in trial}


dependent_variables = {
    "walls": range(1, 100, 3),
    "food_threshold": (1, 150, 300),
}

independent_variables = {
    "avg_score": lambda history: mean(
        snake.score for round in history for snake in round
    ),
}

assignments = (
    [(key, value) for value in values] for key, values in dependent_variables.items()
)

trials = product(*assignments)


for trial in trials:
    trial = make_trial(trial)
    print(trial)
    history = Epoch(
        10,
        5,
        100,
        num_snakes=10,
        size=25,
        walls=trial["walls"],
        food_delay=100,
        initial_growth=3,
        food_threshold=trial["food_threshold"],
        display=lambda _: None,
    )
    for var, func in independent_variables.items():
        print(history)
        print(var, func(history))
