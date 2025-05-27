from Snake import Part
import random


class Board:
    def __init__(self, snakes=(), size=10, food_delay=0, food_threshold=0):
        self.grid = [[Part.EMPTY] * size for i in range(size)]
        self.size = size
        self.food_delay = food_delay
        self.food_countdown = food_delay
        self.food_threshold = food_threshold
        self.snakes = []
        for snake in snakes:
            snake.add_to_board(self)

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
        self.snakes = [snake for snake in self.snakes if snake.body]
        for snake in self.snakes:
            snake.tick(self)
        if self.food_countdown:
            self.food_countdown -= 1
        else:
            self.food_countdown = self.food_delay
            self.random_food()

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

    def snake_at(self, x, y):
        for snake in self.snakes:
            if self.wraparound_pair((x, y)) in snake.body:
                return snake
        return None
