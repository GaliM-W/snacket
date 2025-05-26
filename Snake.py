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

    def get_char(self):
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
        if body is None:
            # [x, y, Part]
            self.body = [[0, 0, Part.HEAD]]
        else:
            self.body = body
        self.sensor_size = sensor_size # 5x5 sensor by default
        self.genome = self.get_random_genome()
    
    def get_random_genome(self, display=False):
        """
        Sensor is nxn based on sensor_size (default is 5x5)
         * 4 sensory modalities (head, body, food, wall)
         * nxn (5x5 = 25) inputs
         * 3 directions (l, r, s) where l + r + s = 1.0
         300 genes total
        """
        # mapping between each sensory modality and direction
        genome = {}
        sensory_modalities = "head", "body", "food", "wall"
        for s in sensory_modalities:
            genome[s] = [[" "] * self.sensor_size for i in range(self.sensor_size)]
        
        for s, w in genome.items():
            print("\n" + s) if display == True else False
            for i in range(self.sensor_size):
                for j in range(self.sensor_size):
                    weights = [random.random(), random.random(), random.random()] # left, right, straight

                    # normalising so they sum to 1.0
                    total = sum(weights)
                    for k in range(len(weights)):
                        weights[k] /= total
                    
                    w[i][j] =  weights # normalise the result so they sum to 1
                    print(i*self.sensor_size+j, weights, "total:", sum(weights)) if display == True else False

        return genome

    def die(self):
        self.dead = True

    def tick(self):
        if self.dead:
            return
        # move snake
        delta = self.facing.delta()
        self.body.append(
            [self.body[-1][0] + delta[0], self.body[-1][1] + delta[1], Part.HEAD]
        )

        # make sure its body parts are all correct
        if len(self.body) > 1:
            if self.body[1][2] is Part.LUMP:
                self.body[1][2] = Part.BODY
            else:
                self.body.pop(0)
                self.body[0][2] = Part.TAIL

        for i in range(len(self.body) - 1):

            if self.body[i][2] is Part.HEAD:
                self.body[i][2] = Part.BODY

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
        x, y, part = self.body[-1]
        assert part == Part.HEAD

        assert self.sensor_size % 2 == 1  # size cannot be off
        sensor_values = [[" "] * self.sensor_size for i in range(self.sensor_size)]
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

        for i in range(self.sensor_size):
            print(locations[self.sensor_size * i : self.sensor_size * i + self.sensor_size])

        for i in range(len(locations)):
            a, b = locations[i]
            if a < 0 or a >=self.sensor_size or b < 0 or b >= self.sensor_size:
                # if location is out of bounds, then 0
                sensor_values[i // 5][i % 5] = 0
            else:
                sensor_values[i // 5][i % 5] = board[a][b]
        
        for i in range(self.sensor_size):
            print(sensor_values[i], end="\n")
            



if __name__ == "__main__":
    sn = Snake([[0,0,Part.HEAD]], facing=Direction.UP, sensor_size=5)
    # sn = Snake([[2,2,Part.HEAD]], facing=Direction.UP)
    # sn = Snake([[2, 2, Part.HEAD]], facing=Direction.DOWN)
    # sn = Snake([[0,0,Part.HEAD]])
    from Board import BoardView

    b = BoardView()
    b.add_snake(sn)
    # replace board with test array to check
    board = []
    for i in range(5):
        board.append([i*5 + j for j in range(5)])

    sn.get_sensor_values(board)
    sn.get_random_genome(display=True)

