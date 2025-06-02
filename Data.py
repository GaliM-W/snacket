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


INDEPENDENT_VARIABLES = {
    "walls": range(1, 500, 20),
    "food_threshold": (1, 150, 300),
    "size": (10, 20, 30),

}

DEPENDENT_VARIABLES = {
    "avg_score": then(all_snakes(lambda snake: snake.score), mean),
    "left": then(all_snakes(lambda snake: snake.turns[Direction.LEFT]), sum),
    "right": then(all_snakes(lambda snake: snake.turns[Direction.RIGHT]), sum),
    "straight": then(all_snakes(lambda snake: snake.turns[Direction.UP]), sum),
}



def run_trials(independent_variables, dependent_variables):
    assignments = (
        [(key, value) for value in values]
        for key, values in independent_variables.items()
    )

    trials = product(*assignments)
    for trial in trials:
        trial = make_trial(trial)
        history = Epoch(
            100,
            5,
            50,
            num_snakes=10,
            size=trial["size"],
            walls=trial["walls"],
            food_delay=100,
            initial_growth=3,
            food_threshold=trial["food_threshold"],
            display=None,
        )
        results = {var: func(history) for var, func in dependent_variables.items()}
        datum = trial | results
        yield datum


def write(independent_variables, dependent_variables, path="./data.json"):
    data = list(run_trials(independent_variables, dependent_variables))
    with open(path, "w") as f:
        dump(data, f)
    return path


def display():
    for datum in run_trials(INDEPENDENT_VARIABLES, DEPENDENT_VARIABLES):
        print(datum)


if __name__ == "__main__":
    write(INDEPENDENT_VARIABLES, DEPENDENT_VARIABLES, path="./data.json")
