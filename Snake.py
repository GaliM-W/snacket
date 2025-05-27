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
        self.score = 0 # score is the number of food eaten / nutrients
        if body is None:
            # [x, y, Part]
            self.body = [(0, 0)]
        else:
            self.body = body
        self.sensor_size = sensor_size # 5x5 sensor by default
        self.genome = self.get_random_genome()

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
        sensory_modalities = "head", "body", "food", "wall"
        for s in sensory_modalities:
            genome[s] = [[" "] * self.sensor_size for i in range(self.sensor_size)]

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

                    w[i][j] =  weights # normalise the result so they sum to 1
                    print(i*self.sensor_size+j, weights, "total:", sum(weights)) if display == True else False

        return genome

    def die(self):
        self.dead = True

    def add_to_board(self, board):
        board.snakes.append(self)
        if not self.body:
            raise ValueError("Snake has no length")
        if len(self.body) > 1:
            x, y = self.body[0]
            board[x, y] = Part.TAIL
            for x, y in self.body[1:-1]:
                board[x, y] = Part.BODY
        x, y = self.body[-1]
        board[x, y] = Part.HEAD

    def tick(self, board):
        shrink = True
        if not self.dead:
            # move snake head
            delta_x, delta_y = self.facing.delta()
            head_x, head_y = self.body[-1]
            new_coordinate = (head_x + delta_x, head_y + delta_y)
            successful, shrink = self.try_move(new_coordinate, board)
            if successful:
                board[new_coordinate] = Part.HEAD
                self.body.append(new_coordinate)
            board[head_x, head_y] = Part.BODY

        if shrink:
            tail = self.body.pop(0)
            board[tail] = Part.EMPTY

    def try_move(self, coordinates, board):
        """
        Returns (successful, no_shrink) depending on whether snake survived moving
        and whether it should get shorter this round
        """
        match board[coordinates]:
            case Part.BODY | Part.HEAD | Part.LUMP | Part.TAIL:
                # TODO: handle colliding with snake
                self.die()
                return False, True
            case Part.WALL:
                self.die()
                return False, True
            case Part.FOOD:
                self.score += 1
                self.grow += 1
                return True, False
            case Part.EMPTY:
                return True, True
            case other:
                raise ValueError(f"{other} is not a part")

    def get_sensor_values(self, grid):
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
        assert grid[x][y] == Part.HEAD, grid

        assert self.sensor_size % 2 == 1  # size cannot be off
        sensor_values = [[None] * self.sensor_size for i in range(self.sensor_size)]
        r = self.sensor_size // 2

        locations = []

        match self.facing:
            case Direction.UP:
                # finding indices that surround the head direction
                for i in range(x - r, x + r + 1):
                    for j in range(y - r, y + r + 1):
                        locations.append(
                            (
                                i,
                                j,
                            )
                        )

            case Direction.RIGHT:
                for j in range(y + r, y - r - 1, -1):
                    for i in range(x - r, x + r + 1):
                        locations.append(
                            (
                                i,
                                j,
                            )
                        )

            case Direction.DOWN:
                # scan the board in the opposite direction to UP
                for i in range(x + r, x - r - 1, -1):
                    for j in range(y + r, y - r - 1, -1):
                        locations.append(
                            (
                                i,
                                j,
                            )
                        )

            case Direction.LEFT:
                for j in range(y - r, y + r + 1):
                    for i in range(x + r, x - r - 1, -1):
                        locations.append(
                            (
                                i,
                                j,
                            )
                        )

        # for i in range(self.sensor_size):
        #     print(locations[self.sensor_size * i : self.sensor_size * i + self.sensor_size])

        for i in range(len(locations)):
            a, b = locations[i]
            if a < 0 or a >= self.sensor_size or b < 0 or b >= self.sensor_size:
                # if location is out of bounds, then 0
                sensor_values[i // 5][i % 5] = 0
            else:
                sensor_values[i // 5][i % 5] = grid[a][b]

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
                print("obj", obj) if display == True else False
                if obj == 0:
                    continue
                elif obj == ":":
                    l, r, u = self.genome["food"][i][j]
                    print(l, r, u) if display == True else False
                    direction[Direction.LEFT] += l
                    direction[Direction.RIGHT] += r
                    direction[Direction.UP] += u
                # keep listing elif for other sensory modalities here
        print(direction) if display == True else False
        print(max(direction, key=direction.get)) if display == True else False

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
        board.append([i*5 + j for j in range(5)])

    board[0][0] = ":"
    # board[0][1] = ":"

    sn.get_sensor_values(board)
    # sn.get_random_genome(display=True)
    sn.get_next_movement(board, display=True)
