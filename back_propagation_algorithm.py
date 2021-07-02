# Author: Colin Francis
# Description: Code for back propagation algorithm used to solve Sudoku puzzles
class SolveSudoku(object):
    """A class used to solve Sudoku puzzles."""
    def __init__(self, puzzle):
        """Creates a SolveSudoku object with a puzzle attribute."""
        self._puzzle = Puzzle(puzzle)

    def solve(self):
        """
        Used to solve Sudoku puzzles.

        :return:
        """
        row_index, col_index = 0, 0
        while '.' in self._puzzle.get_layout()[0]:
            if not self._puzzle.is_preset(row_index, col_index):
                for number in range(1, 10):
                    if not self._in_row(row_index, str(number)) and not self._in_col(col_index, str(number)):
                        self._puzzle.set(row_index, col_index, str(number))
                        self.print_board()
                        break
            col_index += 1

    def _back_prop(self):
        pass

    def _in_row(self, row_index: int, number: str) -> bool:
        """
        Searches the Sudoku puzzle to see if `number` exists in the specified row index.

        :param row_index: The row index in the Sudoku puzzle to search in.
        :param number: The number to search for.
        :return: True if the number is found in the row. Otherwise, False.
        """
        if number in self._puzzle.get_row(row_index):
            return True
        return False

    def _in_col(self, col_index: int, number: str) -> bool:
        """
        Searches the Sudoku puzzle to see if 'number' exists in the specified column
        index.

        :param col_index: The column index in the Sudoku puzzle to search in.
        :param number: The number to search for.
        :return: True if the number is found in the column. Otherwise, False.
        """
        for row in self._puzzle.get_layout():
            if row[col_index] == number:
                return True
        return False

    def print_board(self):
        for row in self._puzzle.get_layout():
            print(row)


class Puzzle(object):
    """Represents a Sudoku puzzle."""
    def __init__(self, puzzle):
        """Creates a puzzle object with layout and preset_layout attributes."""
        self._layout = puzzle
        self._preset_layout = self._find_presets()

    def get_layout(self) -> list:
        """Returns the current layout of the Sudoku puzzle."""
        return self._layout

    def get_row(self, row_index):
        return self._layout[row_index]

    def set(self, row_index, col_index, number):
        self._layout[row_index][col_index] = number

    def is_preset(self, row_index: int, col_index: int) -> bool:
        """
        Determines whether a board value is a preset value or not.

        :param row_index: The row corresponding to the value in the puzzle to check.
        :param col_index: The column corresponding to the value in the puzzle to check.
        :return: True if the value is preset. Otherwise, False.
        """
        if self._preset_layout[row_index][col_index]:
            return True
        else:
            return False

    def _find_presets(self) -> list:
        """
        Iterates through the initial Sudoku puzzle and determines which values are preset and
        which values are variable.

        :return: A matrix (list-of-lists) containing boolean values - True for preset, False
            for variable.
        """
        preset_values = []
        for row_index, row in enumerate(self._layout):
            preset_row = []
            for col_index, col_value in enumerate(row):
                if col_value == '.':
                    preset_row.append(False)
                else:
                    preset_row.append(True)
            preset_values.append(list(preset_row))
            preset_row.clear()
        return preset_values


if __name__ == "__main__":
    sudoku_puzzle = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
                     ["6", ".", ".", "1", "9", "5", ".", ".", "."],
                     [".", "9", "8", ".", ".", ".", ".", "6", "."],
                     ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
                     ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
                     ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
                     [".", "6", ".", ".", ".", ".", "2", "8", "."],
                     [".", ".", ".", "4", "1", "9", ".", ".", "5"],
                     [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

    solve = SolveSudoku(sudoku_puzzle)
    solve.solve()
