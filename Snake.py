from enum import Enum


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

    def __init__(self, body=None, facing=Direction.RIGHT):
        self.facing = facing
        self.dead = False
        if body is None:
            # [x, y, Part]
            self.body = [[0, 0, Part.HEAD]]
        else:
            self.body = body

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

    def get_sensor_values(self, board, size=5):
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

        assert size % 2 == 1  # size cannot be off
        sensor_values = [[" "] * size for i in range(size)]
        r = size // 2

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

        for i in range(size):
            print(locations[size * i : size * i + size])


if __name__ == "__main__":
    # sn = Snake([[0,0,Part.HEAD]], facing=Direction.UP)
    # sn = Snake([[2,2,Part.HEAD]], facing=Direction.UP)
    sn = Snake([[2, 2, Part.HEAD]], facing=Direction.LEFT)
    # sn = Snake([[0,0,Part.HEAD]])
    from Board import BoardView

    b = BoardView()
    b.add_snake(sn)
    sn.get_sensor_values(b, 5)
