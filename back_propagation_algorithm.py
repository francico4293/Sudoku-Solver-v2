# Author: Colin Francis
# Description: Code for back propagation algorithm used to solve Sudoku puzzles
class SolveSudoku(object):
    def __init__(self, puzzle):
        self._board = Board(puzzle)

    def solve(self):
        pass

    def _back_prop(self):
        pass


class Board(object):
    def __init__(self, puzzle):
        self._layout = puzzle


if __name__ == "__main__":
    puzzle = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
              ["6", ".", ".", "1", "9", "5", ".", ".", "."],
              [".", "9", "8", ".", ".", ".", ".", "6", "."],
              ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
              ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
              ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
              [".", "6", ".", ".", ".", ".", "2", "8", "."],
              [".", ".", ".", "4", "1", "9", ".", ".", "5"],
              [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

    solve = SolveSudoku(puzzle)
