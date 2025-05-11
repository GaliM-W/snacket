from Board import Board
from Snake import Snake, Part

board = Board()
board.add_snake(Snake([[0, 0, Part.TAIL], [0, 1, Part.BODY], [1, 1, Part.LUMP], [2, 1, Part.HEAD]]))
print(board)
board.tick()
print(board)
board.tick()
print(board)
board.tick()
print(board)
board.tick()
print(board)