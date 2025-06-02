from Board import Part, Direction
from collections import defaultdict
import random

SIZE_THRESHOLD = -2

class Snake:
    def __init__(self, body=None, facing=Direction.RIGHT, sensor_size=5, hunger_threshold=20):
        self.facing = facing
        if body is None:
            self.body = [(0, 0)]
        else:
            self.body = body
        self.sensor_size = sensor_size  # 5x5 sensor by default
        self.hunger_threshold = hunger_threshold
        self.reset()
        self.genome = self.get_random_genome()
        self.grow = 0
    def __copy__(self):
        new = Snake(body=self.body, facing=self.facing, sensor_size=self.sensor_size, hunger_threshold=self.hunger_threshold)
        new.genome = self.genome
        new.grow = self.grow
        new.dead = self.dead
        new.score = self.score
        new.age = self.age
        new.last_eaten = self.last_eaten
        new.snakes_eaten = self.snakes_eaten
        return new

    def reset(self):
        self.dead = False
        self.score = 0
        self.age = 0
        self.turns = defaultdict(int)
        self.last_eaten = 0
        self.snakes_eaten = 0

    def __repr__(self):
        if self.dead:
            return f"<Snake score={self.score} (dead) {self.body}>"
        return f"<Snake score={self.score} {self.body} turns {dict(self.turns)}>"

    def tick(self, board):
        if self.age - self.last_eaten > self.hunger_threshold:
            self.die()
        if not self.dead:
            # move snake head
            self.age += 1
            delta_x, delta_y = self.facing.delta()
            head_x, head_y = self.body[-1]
            new_coordinate = board.wraparound_pair((head_x + delta_x, head_y + delta_y))
            self.move_to(new_coordinate, board)
            if not self.dead:
                board[new_coordinate] = Part.HEAD
                self.body.append(new_coordinate)
            board[head_x, head_y] = Part.BODY

        if self.grow > 0:  # handle snake growth
            self.grow -= 1
            if len(self.body) > 1:
                neck = self.body[-2]
                board[neck] = Part.LUMP
        else:
            tail = self.body.pop(0)
            if len(self.body) > 1:
                if board[self.body[0]] != Part.LUMP:
                    board[self.body[0]] = Part.TAIL
                # assert board[tail] in [Part.BODY, Part.TAIL, Part.LUMP]
            board[tail] = Part.EMPTY

    def add_to_board(self, board):
        assert self not in board.snakes
        board.snakes.append(self)
        board.historical_snakes.add(self)
        if not self.body:
            raise ValueError(f"Snake {self} has no length")
        if len(self.body) > 1:
            x, y = self.body[0]
            board[x, y] = Part.TAIL
            for x, y in self.body[1:-1]:
                board[x, y] = Part.BODY
        x, y = self.body[-1]
        board[x, y] = Part.HEAD

    def move_to(self, coordinates, board):
        match board[coordinates]:
            case Part.BODY | Part.HEAD | Part.LUMP | Part.TAIL:
                hit_snake = board.snake_at(*coordinates)
                size_difference = self.get_size() - hit_snake.get_size()
                if self == hit_snake:
                    self.die()
                elif size_difference >= SIZE_THRESHOLD:  # 3 is arbitrary threshold for now
                    # attacker self is larger by at least 3, it eats hit_snake
                    hit_snake.die()  # TODO: this should only take effect after all snakes have moved
                    self.eat_snake()
                else:
                    # the attacker is too small, it dies from the collision
                    self.die()
            case Part.WALL:
                self.die()
            case Part.FOOD:
                self.score += 1
                self.grow += 1
                self.last_eaten = self.age
            case Part.EMPTY:
                pass
            case other:
                raise ValueError(f"{other} is not a part")

    def random_position(self, board, reset=False):
        free = [
            (i, j)
            for i, row in enumerate(board.grid)
            for j, spot in enumerate(row)
            if spot == Part.EMPTY
        ]
        self.grow = board.initial_growth
        self.body = [random.choice(free)]
        self.facing = random.choice(
            [
                Direction.UP,
                Direction.RIGHT,
                Direction.DOWN,
                Direction.LEFT,
            ]
        )
        if reset:
            self.reset()

    def get_random_genome(self, display=False):
        """
        Sensor is nxn based on sensor_size (default is 5x5)
         * 4 sensory modalities (head, body, food, wall)
         * nxn (5x5 = 25) inputs
         * 3 directions (l, r, u) where l + r + u = 1.0
         300 genes total
        """
        # mapping between each sensory modality and direction
        genome = {}

        sensory_modalities = Part.HEAD, Part.BODY, Part.FOOD, Part.WALL, Part.EMPTY
        genome = {
            sense: [[None] * self.sensor_size for i in range(self.sensor_size)]
            for sense in sensory_modalities
        }

        for s, w in genome.items():
            if display:
                print("\n" + str(s))
            for i in range(self.sensor_size):
                for j in range(self.sensor_size):
                    weights = [
                        random.random(),
                        random.random(),
                        random.random(),
                    ]  # left, right, up

                    # normalising so they sum to 1.0
                    total = sum(weights)
                    for k in range(len(weights)):
                        weights[k] /= total

                    w[i][j] = weights  # normalise the result so they sum to 1
                    if display:
                        print(i * self.sensor_size + j, weights, "total:", sum(weights))

        return genome

    def get_sensor_values(self, board):
        """
        Returns an nxn array of the objects the snake senses around its head (default is 5x5)
        Must be an odd number, if not will -1
        It is aligned with the direction of the snake head
        """

        def reverse_range(r):
            return range(r.stop - r.step, r.start - r.step, -r.step)

        def transposed(grid):
            return [list(row) for row in zip(*grid)]

        # get head position
        x, y = self.body[-1]
        # assert (
        #     board[x, y] == Part.HEAD
        # ), f"Expected head, got {repr(board[x, y])} at {(x, y)} in:\n{str(board)}\n(snake = {self})"

        assert self.sensor_size % 2 == 1  # size cannot be off
        sensor_values = [[None] * self.sensor_size for i in range(self.sensor_size)]
        r = self.sensor_size // 2

        i_range = range(x - r, x + r + 1)
        j_range = range(y - r, y + r + 1)
        transpose = False

        match self.facing:
            case Direction.UP:
                pass

            case Direction.RIGHT:
                j_range = reverse_range(j_range)
                transpose = True

            case Direction.DOWN:
                i_range = reverse_range(i_range)
                j_range = reverse_range(j_range)

            case Direction.LEFT:
                i_range = reverse_range(i_range)
                transpose = True

            case _:
                raise ValueError(f"{self.facing} is not a valid snake direction")

        locations = [[(i, j) for j in j_range] for i in i_range]
        if transpose:
            locations = transposed(locations)

        for i in range(self.sensor_size):
            for j in range(self.sensor_size):
                sensor_values[i][j] = board[locations[i][j]]

        return sensor_values

    def get_next_movement(self, board, msg=None, info=None, weighted_chance=False):
        """
        Iterates through the board
        If an item is identfied, then will search its array for the weight
        Weights for each direction (left, right, straight) are summed
        The direction with the maximum weight is returned as the next movement
        """
        sensor_values = self.get_sensor_values(board)
        direction = {Direction.LEFT: 0, Direction.RIGHT: 0, Direction.UP: 0}
        extra_display = False
        for i in range(self.sensor_size):
            for j in range(self.sensor_size):
                obj = sensor_values[i][j]
                if msg and extra_display:
                    print("obj", obj)
                match obj:
                    case Part.FOOD:
                        l, r, u = self.genome[Part.FOOD][i][j]
                    case Part.BODY | Part.TAIL | Part.LUMP:
                        l, r, u = self.genome[Part.BODY][i][j]
                    case Part.HEAD:
                        l, r, u = self.genome[Part.HEAD][i][j]
                    case Part.WALL:
                        l, r, u = self.genome[Part.WALL][i][j]
                        # if i == 2 and j == 1:
                        #     info("About to hit a wall")
                        #     l += 10
                        #     r += 10
                    case Part.EMPTY:
                        l, r, u = self.genome[Part.EMPTY][i][j]
                    case _:
                        raise ValueError(f"{obj} is not a Part")
                if msg and extra_display:
                    print(l, r, u)
                direction[Direction.LEFT] += l
                direction[Direction.RIGHT] += r
                direction[Direction.UP] += u
                # keep listing elif for other sensory modalities here
        if msg and extra_display:
            print(direction)
            print(max(direction, key=direction.get))
        
        if weighted_chance:
            directions = list(direction.keys())
            weights = list(direction.values())
            return random.choices(directions, weights, k=1)[0]

        # returns the key (direction) with the highest value (sum of weights)
        return max(direction, key=direction.get)

    def get_size(self):
        return len(self.body)

    def eat_snake(self):
        """handles score and size increase post-snannibalism"""
        self.score += 3  # default to increasing by 3 for now
        self.grow += 1
        self.last_eaten = self.age
        self.snakes_eaten += 1

    def die(self):
        self.dead = True


if __name__ == "__main__":
    # sn = Snake([(0,0)], facing=Direction.UP, sensor_size=5)
    sn = Snake([(2, 2)], facing=Direction.UP)
    # sn = Snake([(2, 2)], facing=Direction.DOWN)
    # sn = Snake([(0,0)])
    from Board import Board

    b = Board()
    sn.add_to_board(b)
    # replace board with test array to check
    board = []
    for i in range(5):
        board.append([i * 5 + j for j in range(5)])

    board[0][0] = ":"
    # board[0][1] = ":"

    raise NotImplementedError("This isn't a real board, should pass b instead:")
    sn.get_sensor_values(board)
    # sn.get_random_genome(display=True)
    sn.get_next_movement(board, display=True)
