from Data import run_trials, INDEPENDENT_VARIABLES
import pickle

data = list(run_trials(INDEPENDENT_VARIABLES, {"data": lambda h: h}))
with open("data.pickle", "wb") as f:
    pickle.dump(data, f)
