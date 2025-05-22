from Snake import Part


class BoardView:

    def __init__(self, snakes=None, size=10):
        if snakes is None:
            self.snakes = []
        self.foods = []
        self.walls = []
        self.board = [[" "] * size for i in range(size)]
        self.size = size

    def __str__(self):
        return "\n".join("".join(line) for line in self.board)

    def add_snake(self, snake):
        self.snakes.append(snake)
        self.redraw()

    def add_food(self, x, y):
        self.foods.append((x, y))
        self.redraw()

    def add_wall(self, x, y):
        self.walls.append((x, y))
        self.redraw()

    def wraparound(self, number):
        return (number + self.size) % self.size

    def redraw(self):
        for wall in self.walls:
            self.board[wall[0]][wall[1]] = "0"
        for food in self.foods:
            self.board[food[0]][food[1]] = ":"
        for snake in self.snakes:
            obstacle = self.board[self.wraparound(snake.body[-1][0])][
                self.wraparound(snake.body[-1][1])
            ]
            if obstacle == ":":
                snake.body[-1][2] = Part.LUMP
            elif obstacle in "X+0":
                snake.die()
            for part in snake.body:
                self.board[self.wraparound(part[0])][self.wraparound(part[1])] = part[
                    2
                ].get_char()

    def clear(self):
        self.board = [[" "] * self.size for i in range(self.size)]

    def tick(self):
        self.clear()
        for snake in self.snakes:
            snake.tick()
        self.redraw()
