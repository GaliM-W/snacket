class Board:

    def __init__(self, snakes=None, size=10):
        if snakes is None:
            self.snakes = []
        self.board = [[" "] * size for i in range(size)]
        self.size = size

    def __str__(self):
        return "\n".join("".join(line) for line in self.board)

    def get_char(self, part):
        match part.value:
            case 0:
                return "O"
            case 1:
                return "X"
            case 2:
                return "+"
            case 3:
                return "."

    def add_snake(self, snake):
        self.snakes.append(snake)
        self.redraw(snake)

    def redraw(self, snake):
        for part in snake.body:
            self.board[part[0]][part[1]] = self.get_char(part[2])

    def clear(self):
        self.board = [[" "] * self.size for i in range(self.size)]

    def tick(self):
        self.clear()
        for snake in self.snakes:
            snake.tick()
            self.redraw(snake)