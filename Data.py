from Generations import Epoch
from Board import Direction
from itertools import product
from statistics import mean
from json import dump


def make_trial(trial):
    return {var: val for var, val in trial}


def all_snakes(func):
    def inner(history):
        for round in history:
            for snake in round:
                yield func(snake)

    return inner

def then(f1, f2):
    return lambda history: f2(f1(history))


DEPENDENT_VARIABLES = {
    "walls": range(1, 500, 3),
    "food_threshold": (1, 150, 300),
}

INDEPENDENT_VARIABLES = {
    "avg_score": then(all_snakes(lambda snake: snake.score), mean),
    "left": then(all_snakes(lambda snake: snake.turns[Direction.LEFT]), sum),
    "right": then(all_snakes(lambda snake: snake.turns[Direction.RIGHT]), sum),
    "straight": then(all_snakes(lambda snake: snake.turns[Direction.UP]), sum),
}


def run_trials(dependent_variables, independent_variables):
    assignments = (
        [(key, value) for value in values]
        for key, values in dependent_variables.items()
    )

    trials = product(*assignments)
    for trial in trials:
        trial = make_trial(trial)
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
        results = {var: func(history) for var, func in independent_variables.items()}
        datum = trial | results
        yield datum


def write(dependent_variables, independent_variables, path="./data.json"):
    data = list(run_trials(dependent_variables, independent_variables))
    with open(path, "w") as f:
        dump(data, f)
    return path


def display():
    for datum in run_trials(DEPENDENT_VARIABLES, INDEPENDENT_VARIABLES):
        print(datum)


if __name__ == "__main__":
    write(DEPENDENT_VARIABLES, INDEPENDENT_VARIABLES, path="./data.json")
