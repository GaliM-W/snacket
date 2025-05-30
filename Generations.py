from Board import Board
from Snake import Snake, Part
from random import random


def MutateGene(gene, mutation_chance=0.1, mutation_range=0.1):
    n = random()
    if n <= mutation_chance:
        mutation = ((2 * mutation_range) * (random())) - mutation_range
        gene += mutation
    return gene


def Reproduce(parent):
    child = Snake()
    for modality in child.genome.keys():
        for geneSequence in range(len(parent.genome[modality])):
            for geneBlock in range(len(parent.genome[modality][geneSequence])):
                for gene in range(
                    len(parent.genome[modality][geneSequence][geneBlock])
                ):
                    child.genome[modality][geneSequence][geneBlock][gene] = MutateGene(
                        parent.genome[modality][geneSequence][geneBlock][gene]
                    )
    return child


# create a board and run its lifetime
# if you don't specify an input population, you must specify a target snake number
def Round(
    round_length, board_size=10, snake_population=None, num_snakes=0, display=False
):

    print("#### BEGIN ROUND ####")

    # create the board and snakes
    board = Board(size=board_size)
    if snake_population is None:
        for i in range(num_snakes):
            snake = Snake()
            snake.random_position(board, reset=False)
            snake.add_to_board(board)
    else:
        snake_population = list(snake_population)
        while len(snake_population) < num_snakes:
            snake_population.append(random.choice(snake_population))
        for snake in snake_population:
            snake.random_position(board, reset=False)
            snake.add_to_board(board)

    # run the board lifetime
    turns = 0
    print(f"{len(board.living_snakes())} living snakes")
    for turn in range(round_length):
        if len(board.living_snakes()) <= 1:
            break
        board.tick()
        print(f"--turn {turn}")

    match board.living_snakes():
        case []:
            return max(board.historical_snakes, key=lambda s: s.score + random())
        case [snake]:
            return snake
        case snakes:
            return max(snakes, key=lambda s: s.score + random())


# run a number of rounds. again, you must specify either population OR num_snakes
def Generation(
    num_rounds,
    round_length,
    board_size=10,
    snake_population=None,
    num_snakes=0,
    display=False,
):

    print("#### BEGIN GENERATION ####")

    # tbd: number generations

    # run a number of rounds per generation and collect winners
    winners = []
    for i in range(num_rounds):
        winsnake = Round(
            round_length,
            board_size=board_size,
            snake_population=snake_population,
            num_snakes=num_snakes,
        )
        winners.append(winsnake)

    # at this point we need to pick pairs of snakes and reproduce another full generation
    # I'm arbitrarily choosing to have them reproduce with neighbors to the right in the array
    # looping around, so final snake reproduces with the first
    j = 0
    next_gen = []
    for j in range(len(winners)):
        next_gen.append(Reproduce(winners[j]))
        # next_gen.append(winners[j])

    return next_gen


def Epoch(
    num_generations,
    num_rounds,
    round_length,
    board_size=10,
    snake_population=None,
    num_snakes=0,
    display=False,
):
    # run a number of generations, using the output of one gen as the input for the next

    print("#### BEGIN EPOCH ####")
    generation = snake_population
    gen_history = []
    for i in range(num_generations):
        generation = Generation(
            num_rounds,
            round_length,
            board_size,
            snake_population=generation,
            num_snakes=num_snakes,
        )
        gen_history.append(generation)
    return gen_history


if __name__ == "__main__":
    epoch = Epoch(5, 10, 5, num_snakes=10)
    for i, round in enumerate(epoch):
        # last round has all zeros as position, because it's freshly born snakes who have not been on a board yet
        print(f"Round {i}: {round}")
        print()
