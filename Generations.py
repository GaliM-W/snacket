from Board import BoardView
from Snake import Snake, Part
from random import random


# create a board and run its lifetime
# if you don't specify an input population, you must specify a target snake number
def Round(round_length, board_size=10, snake_population=[], num_snakes=0):

    print("#### BEGIN ROUND ####")

    #create the board and snakes
    board = BoardView(size=board_size)
    i = 0
    if (snake_population == []):
        while i < num_snakes:
            board.add_snake(Snake())
            i += 1
    else:
        num_snakes = 0
        for i in snake_population:
            board.add_snake(i)
            num_snakes += 1

    # run the board lifetime
    turns = 0
    living_snakes = len(board.snakes)
    while turns < round_length and living_snakes > 1:
        #board.tick()
        # if a snake dies, decrement living_snakes
        turns += 1

    if living_snakes == 1:
        # select the living snake and return it
        return board.snakes[0]
    elif living_snakes == 0:
        # get the max score of dead snakes and return that snake
        # in case of ties, choose randomly
        return board.snakes[1]
    else:
        # get the max score of living snakes
        # in case of ties, choose randomly
        return board.snakes[2]


def MutateGene(gene, mutation_chance=0.1, mutation_range=0.1):
    n = random()
    if n <= mutation_chance:
        mutation = ((2 * mutation_range) * (random())) - mutation_range
        gene += mutation
    return gene


def Reproduce(parent1):
    # do some shit
    child = Snake()
    #for i in range(len(child.genome)):
    #    child.genome[i] = MutateGene(parent.genome[i])
    return child


# run a number of rounds. again, you must specify either population OR num_snakes
def Generation(num_rounds, round_length, board_size=10, snake_population=[], num_snakes=0):

    print("#### BEGIN GENERATION ####")
    # tbd: number generations

    # run a number of rounds per generation and collect winners
    i = 0
    winners = []
    while i < num_rounds:
        winsnake = Round(round_length, board_size=board_size, snake_population=snake_population, num_snakes=num_snakes)
        winners.append(winsnake)
        i += 1

    # at this point we need to pick pairs of snakes and reproduce another full generation
    # I'm arbitrarily choosing to have them reproduce with neighbors to the right in the array
    # looping around, so final snake reproduces with the first
    j = 0
    next_gen = []
    for j in range(len(winners)):
        next_gen.append(Reproduce(winners[j]))

    return next_gen


def Epoch(num_generations, num_rounds, round_length, board_size=10, snake_population=[], num_snakes=0):
    # run a number of generations, using the output of one gen as the input for the next

    print("#### BEGIN EPOCH ####")
    i = 0
    generation = snake_population
    gen_history = []
    while i < num_generations:
        generation = Generation(num_rounds, round_length, board_size, generation, num_snakes)
        gen_history.append(generation)
        i += 1
    return gen_history


<<<<<<< HEAD
#print(Epoch(3, 5, 5, num_snakes=10))
=======
print(Epoch(3, 5, 5, num_snakes=10))
>>>>>>> 86917543e03043d1ddcd91aa2df1cce4cc21fc8f
