import unicurses

from Board import Board, Part, Direction
from Snake import Snake
from Generations import Epoch

from curses import wrapper
from time import sleep

results = None

def main(stdscr):
    stdscr.clear()
    messages = []
    info = []

    def display(board):
        stdscr.clear()
        stdscr.addstr(str(board) + "\n")
        try:
            for message in info:
                stdscr.addstr(message + "\n")
            info.clear()
            for message in messages:
                stdscr.addstr(message + "\n")
                stdscr.getch()
            if not messages:
                # sleep(0.1)
                pass
            messages.clear()
        except Exception as err:
            raise Exception(f"Messages were {messages}, info was {info}, board is {board}") from err
        stdscr.refresh()

    results = Epoch(
        500,
        5,
        100,
        num_snakes=10,
        size=25,
        food_delay=3,
        initial_growth=3,
        food_threshold=25,
        display=display,
        msg=messages.append,
        info=info.append,
    )


wrapper(main)

print(results)
