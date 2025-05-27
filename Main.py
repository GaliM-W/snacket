import unicurses

from Board import Board
from Snake import Snake, Part, Direction

from curses import wrapper
import time


def main(stdscr):
    stdscr.clear()

    board = Board()
    Snake([(0, 0), (0, 1), (1, 1), (2, 1)]).add_to_board(board)
    board.add_food(5, 5)
    board.add_wall(9, 9)
    key = 0
    while key != ord("Q"):
        direction = "asdw".find(chr(key))
        if 0 <= direction <= 3:
            for snake in board.snakes:
                snake.facing = Direction(direction)

        stdscr.clear()
        board.tick()
        stdscr.addstr(str(board))
        stdscr.refresh()
        key = stdscr.getch()


wrapper(main)
