from enum import Enum

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Part(Enum):
    HEAD = 0
    LUMP = 1
    BODY = 2
    TAIL = 3

class Snake:

    def __init__(self, body=None, facing=Direction.RIGHT):
        self.facing = facing
        if body is None:
            self.body = [[0,0,Part.HEAD]]
        else:
            self.body = body

    def turn_left(self):
        self.facing = Direction((self.facing.value + 3) % 4)

    def turn_right(self):
        self.facing = Direction((self.facing.value + 1) % 4)

    def delta(self):
        match self.facing.value:
            case 0:
                return 0, -1
            case 1:
                return 1, 0
            case 2:
                return 0, 1
            case 3:
                return -1, 0
        return 0, 0

    def tick(self):
        # move snake
        delta = self.delta()
        self.body.append([self.body[-1][0] + delta[0], self.body[-1][1] + delta[1], Part.HEAD])

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

