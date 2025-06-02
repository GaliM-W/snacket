# import unicurses

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
    last_key = ""
    skip = 0

    def display(board):
        nonlocal last_key
        nonlocal skip
        if skip:
            if messages:
                skip -= 1
            info.clear()
            messages.clear()
            return
        try:
            #for message in info:
                #stdscr.addstr(message + "\n")
            info.clear()
            for message in messages:
                stdscr.addstr(message + "\n")
                last_key = stdscr.getkey()
            if not messages:
                if last_key != "n":
                    last_key = stdscr.getkey()
            messages.clear()
        except Exception as err:
            raise Exception(
                f"Messages were {messages}, info was {info}, board is {board}"
            ) from err
        stdscr.refresh()
        stdscr.clear()
        if last_key == "e":
            stdscr.addstr(repr(eval(stdscr.getstr())) + "\n")
            last_key = ""
        elif last_key == "s":
            skip = int(stdscr.getstr())
            last_key = ""
        try:
            stdscr.addstr(str(board) + "\n")
        except Exception as err:
            raise ValueError("Board size might be too large for terminal") from err

    results = Epoch(
        1000,
        5,
        100,
        num_snakes=10,
        size=25,
        walls=10,
        food_delay=3,
        initial_growth=3,
        food_threshold=70,
        display=display,
        msg=messages.append,
        info=info.append,
    )


wrapper(main)

print(results)
