import unicurses

from Board import Board, Part, Direction
from Snake import Snake

from curses import wrapper


def main(stdscr):
    stdscr.clear()

    board = Board(food_threshold=3)
    Snake([(0, 0), (0, 1), (1, 1), (2, 1)]).add_to_board(board)
    Snake([(5, 5), (5, 4), (4, 4), (4, 3)]).add_to_board(board)
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
