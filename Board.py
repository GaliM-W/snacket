import random
from enum import Enum


class Board:
    def __init__(
        self,
        snakes=(),
        size=10,
        walls=0,
        food_delay=0,
        food_threshold=0,
        initial_growth=3,
    ):
        self.grid = [[Part.EMPTY] * size for i in range(size)]
        self.size = size
        self.food_delay = food_delay
        self.food_countdown = food_delay
        self.food_threshold = food_threshold
        self.perimeter_walls()
        self.snakes = []
        self.historical_snakes = set()
        self.initial_growth = initial_growth
        for snake in snakes:
            snake.add_to_board(self)
        # self.random_walls(walls)
        for i in range(food_threshold):
            self.random_food()
        self.turn_counter = 0

    def __str__(self):
        return "\n".join("".join(str(part) for part in row) for row in self.grid)

    def __getitem__(self, index):
        x, y = self.wraparound_pair(index)
        return self.grid[x][y]

    def __setitem__(self, index, value):
        x, y = self.wraparound_pair(index)
        self.grid[x][y] = value

    def wraparound(self, number):
        return (number + self.size) % self.size

    def wraparound_pair(self, coordinates):
        x, y = coordinates
        return self.wraparound(x), self.wraparound(y)

    def tick(self):
        # delete empty snakes
        self.turn_counter += 1
        # if (self.turn_counter > 20):
            # self.perimeter_walls()
            #if (self.turn_counter == 20):
                #self.random_walls()
        self.snakes = [snake for snake in self.snakes if snake.body]
        assert len(self.snakes) == len(
            set(self.snakes)
        ), "a single snake mustn't be added twice"
        for snake in self.snakes:
            snake.tick(self)
        if self.food_countdown:
            self.food_countdown -= 1
        else:
            self.food_countdown = self.food_delay
            self.random_food()

    def set_snake_directions(self, **kw):
        for snake in self.living_snakes():
            action = snake.get_next_movement(self, **kw)
            snake.turns[action] += 1  # record stats about turns
            match action:
                case Direction.LEFT:
                    snake.facing = snake.facing.left()
                case Direction.UP:  # straight ahead
                    pass
                case Direction.RIGHT:
                    snake.facing = snake.facing.right()
                case _:
                    raise ValueError(f"{action} is not an action")

    def add_food(self, x, y):
        self[x, y] = Part.FOOD

    def add_wall(self, x, y):
        self[x, y] = Part.WALL

    def random_food(self):
        if sum(row.count(Part.FOOD) for row in self.grid) >= self.food_threshold:
            return
        for _ in range(10):
            x, y = random.randrange(self.size), random.randrange(self.size)
            if self[x, y] == Part.EMPTY:
                self.add_food(x, y)
                return

    def random_walls(self, number):
        walls_added = 0
        while walls_added < number:
            x, y = random.randrange(self.size), random.randrange(self.size)
            if self[x, y] == Part.EMPTY:
                self.add_wall(x, y)
                walls_added += 1

    def snake_at(self, x, y):
        for snake in self.snakes:
            if self.wraparound_pair((x, y)) in snake.body:
                return snake
        return None

    def living_snakes(self):
        return [snake for snake in self.snakes if not snake.dead]


    def perimeter_walls(self):
        for i in range(self.size):
            self[0, i] = Part.WALL
            self[self.size-1, i] = Part.WALL
            self[i, 0] = Part.WALL
            self[i, self.size-1] = Part.WALL


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
                return "#"
            case Part.FOOD:
                return ":"
        raise ValueError(f"{self} is not a Part")


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def delta(self):
        match self:
            case Direction.UP:  # up
                return -1, 0
            case Direction.RIGHT:  # right
                return 0, 1
            case Direction.DOWN:  # down
                return 1, 0
            case Direction.LEFT:  # left
                return 0, -1
        raise ValueError(f"{self} is not a direction")

    def left(self):
        return Direction((self.value + 3) % 4)

    def backwards(self):
        return Direction((self.value + 2) % 4)

    def right(self):
        return Direction((self.value + 1) % 4)
