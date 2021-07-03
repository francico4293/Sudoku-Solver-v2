# Author: Colin Francis
# Description: Code for back propagation algorithm used to solve Sudoku puzzles
import time


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
        start_time = time.perf_counter()
        while not self._solved():
            if col_index > 8:
                col_index = 0
                row_index += 1

            if self._puzzle.get_number(row_index, col_index) == '.' and not \
                    self._puzzle.is_preset(row_index, col_index):
                for number in range(1, 10):
                    if not self._in_row(row_index, str(number)) and not self._in_col(col_index, str(number)) and not \
                            self._in_square(row_index, col_index, str(number)):
                        self._puzzle.set(row_index, col_index, str(number))
                        col_index += 1
                        break
                else:
                    row_index, col_index = self._back_prop(row_index, col_index - 1)
            elif not self._puzzle.is_preset(row_index, col_index):
                start_number = int(self._puzzle.get_number(row_index, col_index)) + 1
                for number in range(start_number, 10):
                    if not self._in_row(row_index, str(number)) and not self._in_col(col_index, str(number)) and not \
                            self._in_square(row_index, col_index, str(number)):
                        self._puzzle.set(row_index, col_index, str(number))
                        col_index += 1
                        break
                else:
                    self._puzzle.set(row_index, col_index, '.')
                    row_index, col_index = self._back_prop(row_index, col_index - 1)
            else:
                col_index += 1
        end_time = time.perf_counter()
        print("Solution Speed: {:.2f}s".format(end_time - start_time))
        self.print_board()

    def _back_prop(self, row_index: int, col_index: int) -> tuple:
        """
        Recursively moves backwards through the Sudoku puzzle until a non-preset
        value less than 9 is found.

        :param row_index: The current row index in the puzzle.
        :param col_index: The current column index in the puzzle
        :return: A tuple containing the row index and column index where the
            non-preset value was found.
        """
        if col_index < 0:
            col_index = 8
            row_index -= 1

        # base case
        if self._puzzle.get_number(row_index, col_index) != '9' and not self._puzzle.is_preset(row_index, col_index):
            return row_index, col_index

        if self._puzzle.get_number(row_index, col_index) == '9' and not self._puzzle.is_preset(row_index, col_index):
            self._puzzle.set(row_index, col_index, '.')
            return self._back_prop(row_index, col_index - 1)
        elif self._puzzle.is_preset(row_index, col_index):
            return self._back_prop(row_index, col_index - 1)

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

    def _in_square(self, row_index: int, col_index: int, number: str) -> bool:
        """
        Searches the Sudoku puzzle to see if the `number` exists in the square
        region of the Sudoku board as indicated by the specified row index and
        column index.

        :param row_index: The row index of the Sudoku puzzle to search in.
        :param col_index: The column index of the Sudoku puzzle to search
            in.
        :param number: The number to search for.
        :return: True if the number is found in the square region. Otherwise,
            False.
        """
        squares = {1: self._puzzle.get_layout()[0][:3] + self._puzzle.get_layout()[1][:3] +
                   self._puzzle.get_layout()[2][:3],
                   2: self._puzzle.get_layout()[0][3:6] + self._puzzle.get_layout()[1][3:6] +
                   self._puzzle.get_layout()[2][3:6],
                   3: self._puzzle.get_layout()[0][6:] + self._puzzle.get_layout()[1][6:] +
                   self._puzzle.get_layout()[2][6:],
                   4: self._puzzle.get_layout()[3][:3] + self._puzzle.get_layout()[4][:3] +
                   self._puzzle.get_layout()[5][:3],
                   5: self._puzzle.get_layout()[3][3:6] + self._puzzle.get_layout()[4][3:6] +
                   self._puzzle.get_layout()[5][3:6],
                   6: self._puzzle.get_layout()[3][6:] + self._puzzle.get_layout()[4][6:] +
                   self._puzzle.get_layout()[5][6:],
                   7: self._puzzle.get_layout()[6][:3] + self._puzzle.get_layout()[7][:3] +
                   self._puzzle.get_layout()[8][:3],
                   8: self._puzzle.get_layout()[6][3:6] + self._puzzle.get_layout()[7][3:6] +
                   self._puzzle.get_layout()[8][3:6],
                   9: self._puzzle.get_layout()[6][6:] + self._puzzle.get_layout()[7][6:] +
                   self._puzzle.get_layout()[8][6:]
                   }

        if row_index == 0 or row_index == 1 or row_index == 2:
            if 0 <= col_index < 3:
                if number in squares[1]:
                    return True
                return False
            elif 3 <= col_index < 6:
                if number in squares[2]:
                    return True
                return False
            else:
                if number in squares[3]:
                    return True
                return False
        elif row_index == 3 or row_index == 4 or row_index == 5:
            if 0 <= col_index < 3:
                if number in squares[4]:
                    return True
                return False
            elif 3 <= col_index < 6:
                if number in squares[5]:
                    return True
                return False
            else:
                if number in squares[6]:
                    return True
                return False
        else:
            if 0 <= col_index < 3:
                if number in squares[7]:
                    return True
                return False
            elif 3 <= col_index < 6:
                if number in squares[8]:
                    return True
                return False
            else:
                if number in squares[9]:
                    return True
                return False

    def _solved(self) -> bool:
        """
        Searches each row in the Sudoku puzzle to determine if a solution has been
        found.

        :return: True if a solution has been found. Otherwise, False.
        """
        if '.' in self._puzzle.get_row(0) or '.' in self._puzzle.get_row(1) or '.' in self._puzzle.get_row(2) or \
                '.' in self._puzzle.get_row(3) or '.' in self._puzzle.get_row(4) or '.' in self._puzzle.get_row(5) or \
                '.' in self._puzzle.get_row(6) or '.' in self._puzzle.get_row(7) or '.' in self._puzzle.get_row(8):
            return False
        return True

    def print_board(self):
        for row in self._puzzle.get_layout():
            print(row)
        print()


class Puzzle(object):
    """Represents a Sudoku puzzle."""
    def __init__(self, puzzle):
        """Creates a puzzle object with layout and preset_layout attributes."""
        self._layout = puzzle
        self._preset_layout = self._find_presets()

    def get_layout(self) -> list:
        """
        Returns the current layout of the Sudoku puzzle.

        :return: A matrix (list-of-lists) representing the Sudoku puzzle in its
            current state.
        """
        return self._layout

    def get_row(self, row_index: int) -> list:
        """
        Returns the row that corresponds to the specified row index.

        :param row_index: The index of the row to get.
        :return: The row corresponding to the provided row index.
        """
        return self._layout[row_index]

    def get_number(self, row_index: int, col_index: int) -> str:
        """
        Returns the number in the Sudoku puzzle found in the position specified by
        `row_index` and `col_index`.

        :param row_index: The index of the row to get the number from.
        :param col_index: The index of the column to get the number from.
        :return: The number corresponding to the specified row index and column
            index.
        """
        return self._layout[row_index][col_index]

    def set(self, row_index: int, col_index: int, number: str) -> None:
        """
        Sets the square in the Sudoku puzzle corresponding to `row_index` and
        `col_index`.

        :param row_index: The index of the row to place the number in.
        :param col_index: The index of the column to place the number in.
        :param number: The number to place in the puzzle.
        :return: None.
        """
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
