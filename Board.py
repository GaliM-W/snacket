class Board:

    def __init__(self, snakes=None, size=10):
        if snakes is None:
            self.snakes = []
        self.board = [[" "] * size for i in range(size)]
        self.size = size

    def __str__(self):
        return "\n".join("".join(line) for line in self.board)

    def get_char(self, part):
        return "@X+.0:"[part.value]

    def add_snake(self, snake):
        self.snakes.append(snake)
        self.redraw(snake)

    def wraparound(self, number):
        return (number + self.size) % self.size

    def redraw(self, snake):
        for part in snake.body:
            self.board[self.wraparound(part[0])][self.wraparound(part[1])] = self.get_char(part[2])

    def clear(self):
        self.board = [[" "] * self.size for i in range(self.size)]

    def tick(self):
        self.clear()
        for snake in self.snakes:
            snake.tick()
            self.redraw(snake)