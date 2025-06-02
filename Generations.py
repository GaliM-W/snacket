from Board import Board, Part, Direction
from Snake import Snake
from random import random, choices
from copy import copy
import math

def MutateGeneBlock(geneBlock, mutation_chance=0.3, mutation_range=0.3):
    # We mutate the l,r,u genes for a given modality and cell together
    # Each gene mutation is random, and then the genes are scaled so that
    # they still sum to 1
    log_genes = []
    for i in range(len(geneBlock)):
        log_genes.append(math.log(max(geneBlock[i], 1e-10))) # Tried using log space to avoid explosions
    for i in range(len(log_genes)):
        if random() <= mutation_chance:
            mutation = (2 * mutation_range) * (random() - 0.5)
            log_genes[i] += mutation

    genes = [] # then converted it back here
    for i in range(len(log_genes)):
        genes.append(math.exp(log_genes[i]))

    normalizer = sum(genes)
    results = []
    for gene in genes:
        results.append(gene / normalizer)
    return results


def Reproduce(parent):
    # Create a new snake and give it a mutated version of the parent genome

    child = Snake()
    for modality in child.genome.keys():
        for geneSequence in range(len(parent.genome[modality])):
            for geneBlock in range(len(parent.genome[modality][geneSequence])):
                child.genome[modality][geneSequence][geneBlock] = MutateGeneBlock(
                    parent.genome[modality][geneSequence][geneBlock],
                    # mutation_chance=0.3,
                    # mutation_range=0.2,
                )
    return child


def Fitness(snake):
    # make sure this order matches the logging too
    return not snake.dead, snake.snakes_eaten, snake.score, snake.age, random()


# create a board and run its lifetime
# if you don't specify an input population, you must specify a target snake number
def Round(
    round_length,
    board_size=10,
    snake_population=None,
    num_snakes=0,
    round_n=0,
    display=None,
    msg=None,
    info=None,
    **kwargs,
):
    if info is None:
        info = lambda *a, **kw: None

    info(f"# BEGIN ROUND {round_n} #")

    # create the board and snakes
    board = Board(**kwargs)
    if not snake_population:
        for i in range(num_snakes):
            snake = Snake()
            snake.random_position(board, reset=True)
            snake.add_to_board(board)
    else:
        snake_population = list(snake_population)
        snakes_to_add = num_snakes - len(snake_population)
        weights = range(
            snakes_to_add + 1, 1, -1
        )  # favour snakes at start of list, as they tend to have higher fitness
        new_snakes = choices(snake_population, weights=weights, k=snakes_to_add)
        snake_population.extend(new_snakes)
        for snake in snake_population:
            snake = copy(snake)
            snake.random_position(board, reset=True)
            snake.add_to_board(board)

    # run the board lifetime
    info(f"{len(board.living_snakes())} living snakes")
    for turn in range(round_length):
        if display is not None:
            display(board)
        if len(board.living_snakes()) <= 1:
            if info is not None:
                info("Round finished early")
            break
        board.set_snake_directions(info=info, msg=msg)
        board.tick()
        # if info is not None:
        #     info(f"--turn {turn}")
    else:
        if display is not None:
            display(board)

    # fitness function considers whether snake survived or not,
    # score, and age, plus a small random factor
    return max(board.historical_snakes, key=Fitness)


# run a number of rounds. again, you must specify either population OR num_snakes
def Generation(num_rounds, round_length, msg=None, info=None, gen_n=0, **kwargs):
    if msg is not None:
        msg(f"## BEGIN GENERATION {gen_n} ##")

    # tbd: number generations

    # run a number of rounds per generation and collect winners
    winners = []
    for i in range(num_rounds):
        winsnake = Round(round_length, msg=msg, info=info, round_n=i, **kwargs)
        winners.append(winsnake)
    for winsnake in winners:
        if info is not None:
            alive, kills, score, age, _ = Fitness(winsnake)
            alive = "LIVE" if alive else "dead"
            turns = (
                winsnake.turns[Direction.LEFT],
                winsnake.turns[Direction.UP],
                winsnake.turns[Direction.RIGHT],
            )
            info(f"Winner: {alive=} {kills=} {score=} {age=} {turns=}")

    winners.sort(key=Fitness)

    next_gen = [Reproduce(winner) for winner in winners]

    return next_gen, winners


def Epoch(
    num_generations,
    num_rounds,
    round_length,
    epoch_n=0,
    snake_population=(),
    msg=None,
    **kwargs,
):
    # run a number of generations, using the output of one gen as the input for the next

    if msg is not None:
        msg(f"### BEGIN EPOCH {epoch_n} ###")
    generation = list(snake_population)
    gen_history = []
    for i in range(num_generations):
        generation, winners = Generation(
            num_rounds,
            round_length,
            gen_n=i,
            snake_population=generation,
            msg=msg,
            **kwargs,
        )
        gen_history.append(winners)
    return gen_history


if __name__ == "__main__":
    epoch = Epoch(5, 10, 5, num_snakes=10, display=print)
    for i, round in enumerate(epoch):
        # last round has all zeros as position, because it's freshly born snakes who have not been on a board yet
        print(f"Round {i}: {round}")
        print()
