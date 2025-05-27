from dataclasses import dataclass
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
    
    def handle_snake_collisions(self):
        """ Check if the head of one snake collides with another snake's body """
        dead_snakes = [] # snakes to be removed
        for snake_a in self.snakes:
            if snake_a.dead:
                continue
            head_position = (self.wraparound(snake_a.body[-1][0]), self.wraparound(snake_a.body[-1][1]))
            for snake_b in self.snakes:
                if snake_a == snake_b or snake_b.dead:
                    continue
                snake_b_positions = [(self.wraparound(part[0]), self.wraparound(part[1])) for part in snake_b.body]
                if head_position in snake_b_positions:
                    size_difference = snake_a.get_size() - snake_b.get_size()
                    if size_difference >= 3: # 3 is arbitrary threshold for now
                        # attacker snake_a is larger by at least 3, it eats snake_b
                        snake_b.die()
                        dead_snakes.append(snake_b)
                        snake_a.eat_snake()
                        snake_a.body[-1][2] = Part.LUMP
                    else:
                        # the attacker is too small, it dies from the collision
                        snake_a.die()
                        dead_snakes.append(snake_a)
                    break

        for dead_snake in dead_snakes:
            if dead_snake in self.snakes:
                self.snakes.remove(dead_snake)


    def handle_snake_collisions(self):
        """ Check if the head of one snake collides with another snake's body """
        dead_snakes = [] # snakes to be removed
        for snake_a in self.snakes:
            if snake_a.dead:
                continue
            head_position = (self.wraparound(snake_a.body[-1][0]), self.wraparound(snake_a.body[-1][1]))
            for snake_b in self.snakes:
                if snake_a == snake_b or snake_b.dead:
                    continue
                snake_b_positions = [(self.wraparound(part[0]), self.wraparound(part[1])) for part in snake_b.body]
                if head_position in snake_b_positions:
                    size_difference = snake_a.get_size() - snake_b.get_size()
                    if size_difference >= 3: # 3 is arbitrary threshold for now
                        # attacker snake_a is larger by at least 3, it eats snake_b
                        snake_b.die()
                        dead_snakes.append(snake_b)
                        snake_a.eat_snake()
                        snake_a.body[-1][2] = Part.LUMP
                    else:
                        # the attacker is too small, it dies from the collision
                        snake_a.die()
                        dead_snakes.append(snake_a)
                    break

        for dead_snake in dead_snakes:
            if dead_snake in self.snakes:
                self.snakes.remove(dead_snake)


    def redraw(self):
        for wall in self.walls:
            self.board[wall[0]][wall[1]] = "0"
        for food in self.foods:
            self.board[food[0]][food[1]] = ":"
        for snake in self.snakes:
            obstacle = self.board[
                self.wraparound(snake.body[-1][0])
            ][
                self.wraparound(snake.body[-1][1])
            ]
            if obstacle == ":":
                snake.body[-1][2] = Part.LUMP
                snake.score += 1 # increment score for eating food
                snake.grow += 1
            elif obstacle in "X+0":
                snake.die()
            for part in snake.body:
                self.board[self.wraparound(part[0])][self.wraparound(part[1])] = part[2].get_char()

    def clear(self):
        self.board = [[" "] * self.size for i in range(self.size)]

    def tick(self):
        # delete empty snakes
        self.snakes = [snake for snake in self.snakes if snake.body]
        for snake in self.snakes:
            snake.tick(self)

    def add_food(self, x, y):
        self[x, y] = Part.FOOD

    def add_wall(self, x, y):
        self[x, y] = Part.WALL
