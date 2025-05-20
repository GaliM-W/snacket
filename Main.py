import curses

import unicurses

from Board import Board
from Snake import Snake, Part

from curses import wrapper
import time

def main(stdscr):
    stdscr.clear()

    board = Board()
    board.add_snake(Snake([[0, 0, Part.TAIL], [0, 1, Part.BODY], [1, 1, Part.LUMP], [2, 1, Part.HEAD]]))

    for i in range(10):
        time.sleep(0.1)
        stdscr.clear()
        stdscr.addstr(str(board))
        board.tick()
        stdscr.refresh()
        stdscr.getkey()

wrapper(main)