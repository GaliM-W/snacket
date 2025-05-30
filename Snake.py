from enum import Enum
import random


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def delta(self):
        match self:
            case Direction.UP:  # up
                return 0, -1
            case Direction.RIGHT:  # right
                return 1, 0
            case Direction.DOWN:  # down
                return 0, 1
            case Direction.LEFT:  # left
                return -1, 0
        raise ValueError(f"{self} is not a direction")

    def left(self):
        return Direction((self.value + 3) % 4)

    def backwards(self):
        return Direction((self.value + 2) % 4)

    def right(self):
        return Direction((self.value + 1) % 4)


class Part(Enum):
    EMPTY = 0
    HEAD = 1
    LUMP = 2
    BODY = 3
    TAIL = 4
    WALL = 5
    FOOD = 6

    def __str__(self):
        match self:
            case Part.EMPTY:
                return " "
            case Part.HEAD:
                return "@"
            case Part.LUMP:
                return "X"
            case Part.BODY:
                return "+"
            case Part.TAIL:
                return "."
            case Part.WALL:
                return "0"
            case Part.FOOD:
                return ":"
        raise ValueError(f"{self} is not a Part")


class Snake:

    def __init__(self, body=None, facing=Direction.RIGHT, sensor_size=5):
        self.facing = facing
        self.dead = False
        self.score = 0  # score is the number of food eaten / nutrients
        if body is None:
            # [x, y, Part]
            self.body = [(0, 0)]
        else:
            self.body = body
        self.sensor_size = sensor_size  # 5x5 sensor by default
        self.genome = self.get_random_genome()
        self.grow = 0

    def __repr__(self):
        if self.dead:
            return f"<Snake score={self.score} (dead) {self.body}>"
        return f"<Snake score={self.score} {self.body}>"

    def get_size(self):
        return len(self.body)

    def eat_snake(self):
        """handles score and size increase post-snannibalism"""
        self.score += 3  # default to increasing by 3 for now
        self.grow += 1

    def die(self):
        self.dead = True

    def add_to_board(self, board):
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

    def random_position(self, board, reset=False):
        free = [
            (i, j)
            for i, row in enumerate(board.grid)
            for j, spot in enumerate(row)
            if spot == Part.EMPTY
        ]
        self.grow = 2
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
            self.dead = False
            self.score = 0

    def tick(self, board):
        if not self.dead:
            # move snake head
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
            board[tail] = Part.EMPTY

    def move_to(self, coordinates, board):
        match board[coordinates]:
            case Part.BODY | Part.HEAD | Part.LUMP | Part.TAIL:
                hit_snake = board.snake_at(*coordinates)
                size_difference = self.get_size() - hit_snake.get_size()
                if self == hit_snake:
                    self.die()
                elif size_difference >= 3:  # 3 is arbitrary threshold for now
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
            case Part.EMPTY:
                pass
            case other:
                raise ValueError(f"{other} is not a part")

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

        sensory_modalities = Part.HEAD, Part.BODY, Part.FOOD, Part.WALL
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
        # wall
        # other snake
        # other snake head and direction
        # food

        # get head position
        x, y = self.body[-1]
        assert board[x, y] == Part.HEAD, str(board)

        assert self.sensor_size % 2 == 1  # size cannot be off
        sensor_values = [[None] * self.sensor_size for i in range(self.sensor_size)]
        r = self.sensor_size // 2

        match self.facing:
            case Direction.UP:
                # finding indices that surround the head direction
                i_range = range(x - r, x + r + 1)
                j_range = range(y - r, y + r + 1)

            case Direction.RIGHT:
                i_range = range(y + r, y - r - 1, -1)
                j_range = range(x - r, x + r + 1)

            case Direction.DOWN:
                # scan the board in the opposite direction to UP
                i_range = range(x + r, x - r - 1, -1)
                j_range = range(y + r, y - r - 1, -1)

            case Direction.LEFT:
                i_range = range(y - r, y + r + 1)
                j_range = range(x + r, x - r - 1, -1)

        locations = [(i, j) for j in i_range for i in j_range]

        for i, (a, b) in enumerate(locations):
            if a < 0 or a >= self.sensor_size or b < 0 or b >= self.sensor_size:
                # if location is out of bounds, then 0
                sensor_values[i // 5][i % 5] = 0
            else:
                sensor_values[i // 5][i % 5] = board[a, b]

        return sensor_values

    def get_next_movement(self, board, display=False):
        """
        Iterates through the board
        If an item is identfied, then will search its array for the weight
        Weights for each direction (left, right, straight) are summed
        The direction with the maximum weight is returned as the next movement
        """
        sensor_values = self.get_sensor_values(board)
        direction = {Direction.LEFT: 0, Direction.RIGHT: 0, Direction.UP: 0}
        for i in range(self.sensor_size):
            for j in range(self.sensor_size):
                obj = sensor_values[i][j]
                if display:
                    print("obj", obj)
                match obj:
                    case Part.EMPTY:
                        continue
                    case Part.FOOD:
                        l, r, u = self.genome[Part.FOOD][i][j]
                        if display:
                            print(l, r, u)
                        direction[Direction.LEFT] += l
                        direction[Direction.RIGHT] += r
                        direction[Direction.UP] += u
                    case Part.BODY | Part.TAIL | Part.LUMP:
                        l, r, u = self.genome[Part.BODY][i][j]
                        if display:
                            print(l, r, u)
                        direction[Direction.LEFT] += l
                        direction[Direction.RIGHT] += r
                        direction[Direction.UP] += u
                    case Part.HEAD:
                        l, r, u = self.genome[Part.HEAD][i][j]
                        if display:
                            print(l, r, u)
                        direction[Direction.LEFT] += l
                        direction[Direction.RIGHT] += r
                        direction[Direction.UP] += u
                    case Part.WALL:
                        l, r, u = self.genome[Part.WALL][i][j]
                        if display:
                            print(l, r, u)
                        direction[Direction.LEFT] += l
                        direction[Direction.RIGHT] += r
                        direction[Direction.UP] += u
                # keep listing elif for other sensory modalities here
        if display:
            print(direction)
            print(max(direction, key=direction.get))

        # returns the key (direction) with the highest value (sum of weights)
        return max(direction, key=direction.get)


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
