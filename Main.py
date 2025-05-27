import unicurses

from Board import BoardView
from Snake import Snake, Part, Direction

from curses import wrapper
import time


def main(stdscr):
    stdscr.clear()

    board = BoardView()
    board.add_snake(
        Snake(
            [[0, 0, Part.TAIL], [0, 1, Part.BODY], [1, 1, Part.LUMP], [2, 1, Part.HEAD]]
        )
    )
    board.add_snake(
        Snake(
            [[5, 5, Part.TAIL], [5, 4, Part.BODY], [4, 4, Part.LUMP], [4, 3, Part.HEAD]]
        )
    )
    board.add_food(5, 5)
    board.add_wall(9, 9)
    key1 = 0
    key2 = 0
    while key1 != ord("Q"):
        direction1 = "asdw".find(chr(key1))
        direction2 = "jkli".find(chr(key2))
        if 0 <= direction1 <= 3 and 0 <= direction2 <= 3:
            board.snakes[0].facing = Direction(direction1)
            if len(board.snakes) > 1:
                board.snakes[1].facing = Direction(direction2)

        stdscr.clear()
        board.tick()
        stdscr.addstr(str(board))
        stdscr.refresh()
        key1 = stdscr.getch()
        key2 = stdscr.getch()


wrapper(main)
