from Snake import Part


class Board:
    def __init__(self, snakes=(), size=10):
        self.grid = [[Part.EMPTY] * size for i in range(size)]
        self.size = size
        self.snakes = []
        for snake in snakes:
            snake.add_to_board(self)

    def __str__(self):
        return "\n".join("".join(str(part) for part in row) for row in self.grid)

    def __getitem__(self, index):
        x, y = index
        return self.grid[self.wraparound(x)][self.wraparound(y)]

    def __setitem__(self, index, value):
        x, y = index
        self.grid[self.wraparound(x)][self.wraparound(y)] = value

    def wraparound(self, number):
        return (number + self.size) % self.size

        for dead_snake in dead_snakes:
            if dead_snake in self.snakes:
                self.snakes.remove(dead_snake)

    def tick(self):
        # delete empty snakes
        self.snakes = [snake for snake in self.snakes if snake.body]
        for snake in self.snakes:
            snake.tick(self)

    def add_food(self, x, y):
        self[x, y] = Part.FOOD

    def add_wall(self, x, y):
        self[x, y] = Part.WALL

    def snake_at(self, x, y):
        for snake in self.snakes:
            if (x, y) in snake.body:
                return snake
        return None
