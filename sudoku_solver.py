# Author: Colin Francis
# Description: An implementation of a Sudoku solver using pygame.

import pygame
import time
import math
from solver_settings import *


class SudokuSolver(object):
    pygame.font.init()

    def __init__(self):
        self._board = Board()
        self._running = True

    def run(self) -> None:
        while self._running:  # main program loop
            for event in pygame.event.get():
                # check if the user wants to exit
                if event.type == pygame.QUIT:
                    self._running = False

                # check if the user clicked their mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if the user clicked their mouse within the grid boundaries then show the
                    #   selected square
                    if (BOARD_LEFT <= pygame.mouse.get_pos()[0] <= BOARD_LEFT + BOARD_WIDTH) and \
                            (BOARD_TOP <= pygame.mouse.get_pos()[1] <= BOARD_TOP + BOARD_HEIGHT):
                        self._board.set_selected_square_coords(mouse_pos()[0], mouse_pos()[1])
                    # if user clicked their mouse within the solve button boundaries, then click the
                    #   solve button
                    elif (SOLVE_BUTTON_LEFT <= pygame.mouse.get_pos()[0] <= SOLVE_BUTTON_LEFT + BUTTON_WIDTH) and \
                            (SOLVE_BUTTON_TOP <= pygame.mouse.get_pos()[1] <= SOLVE_BUTTON_TOP + BUTTON_HEIGHT):
                        self._board.solve_button_click()
                    # if the user clicked their mouse within the clear button boundaries, then clear the
                    #   puzzle
                    elif (CLEAR_BUTTON_LEFT <= pygame.mouse.get_pos()[0] <= CLEAR_BUTTON_LEFT + BUTTON_WIDTH) and \
                            (CLEAR_BUTTON_TOP <= pygame.mouse.get_pos()[1] <= CLEAR_BUTTON_TOP + BUTTON_HEIGHT):
                        self._board.clear_board()

                # check for a number being entered
                if event.type == pygame.KEYDOWN:
                    # user entered 1
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        self._board.set_number_by_selected(1)
                    # user entered 2
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        self._board.set_number_by_selected(2)
                    # user entered 3
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        self._board.set_number_by_selected(3)
                    # user entered 4
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        self._board.set_number_by_selected(4)
                    # user entered 5
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        self._board.set_number_by_selected(5)
                    # user entered 6
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        self._board.set_number_by_selected(6)
                    # user entered 7
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        self._board.set_number_by_selected(7)
                    # user entered 8
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        self._board.set_number_by_selected(8)
                    # user entered 9
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        self._board.set_number_by_selected(9)
                    # clear selected square
                    elif event.key == pygame.K_BACKSPACE:
                        self._board.set_number_by_selected('.')

                # check if the puzzle is ready to be solved
                if self._board.solve_sudoku():
                    self._board.solve_button_unclick()  # un-click the solve button
                    self._solve()  # begin solving puzzle

            self._board.update(pygame.mouse.get_pos())  # update the board
            pygame.display.update()  # update the pygame display

    def _solve(self):
        """
        Used to solve Sudoku puzzles.

        :return:
        """
        self._board.lock_presets()

        row_index, col_index = 0, 0
        start_time = time.perf_counter()
        while not self._board.solved():
            if col_index > 8:
                col_index = 0
                row_index += 1

            self._board.set_selected_square_coords(
                BOARD_LEFT + (SQUARE_HEIGHT * col_index),
                BOARD_TOP + (SQUARE_WIDTH * row_index)
            )
            if self._board.get_number(row_index, col_index) == '.' and not \
                    self._board.is_preset(row_index, col_index):
                for number in range(1, 10):
                    if not self._board.in_row(row_index, str(number)) and not \
                            self._board.in_col(col_index, str(number)) and not \
                            self._board.in_square(row_index, col_index, str(number)):
                        self._board.set_number_by_index(row_index, col_index, str(number))
                        col_index += 1
                        break
                else:
                    row_index, col_index = self._back_prop(row_index, col_index - 1)
            elif not self._board.is_preset(row_index, col_index):
                start_number = int(self._board.get_number(row_index, col_index)) + 1
                for number in range(start_number, 10):
                    if not self._board.in_row(row_index, str(number)) and not \
                            self._board.in_col(col_index, str(number)) and not \
                            self._board.in_square(row_index, col_index, str(number)):
                        self._board.set_number_by_index(row_index, col_index, str(number))
                        col_index += 1
                        break
                else:
                    self._board.set_number_by_index(row_index, col_index, '.')
                    row_index, col_index = self._back_prop(row_index, col_index - 1)
            else:
                col_index += 1
            self._board.update(pygame.mouse.get_pos())  # update the game board
            pygame.display.update()  # update the display
        end_time = time.perf_counter()
        print(math.floor(end_time - start_time) / 60)

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
        if self._board.get_number(row_index, col_index) != '9' and not self._board.is_preset(row_index, col_index):
            return row_index, col_index

        if self._board.get_number(row_index, col_index) == '9' and not self._board.is_preset(row_index, col_index):
            self._board.set_number_by_index(row_index, col_index, '.')
            return self._back_prop(row_index, col_index - 1)
        elif self._board.is_preset(row_index, col_index):
            return self._back_prop(row_index, col_index - 1)


class Board(object):
    """Represents the Sudoku board."""
    pygame.display.set_caption("Sudoku Solver")

    def __init__(self):
        """Creates a Sudoku Board object."""
        self._window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self._window.fill(WHITE)
        self._surface.fill(WHITE)
        self._solve_button = Button(self._window, 'Solve Puzzle', SOLVE_BUTTON_LEFT, SOLVE_BUTTON_TOP)
        self._clear_button = Button(self._window, 'Clear Puzzle', CLEAR_BUTTON_LEFT, CLEAR_BUTTON_TOP)
        self._selected_square_coords = []
        self._puzzle = [[".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        ]
        # self._puzzle = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
        #                 ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        #                 [".", "9", "8", ".", ".", ".", ".", "6", "."],
        #                 ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        #                 ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        #                 ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        #                 [".", "6", ".", ".", ".", ".", "2", "8", "."],
        #                 [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        #                 [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
        self._puzzle_presets = []

    def update(self, mouse_position):
        """
        Collectively updates Board conditions (colors, numbers, etc.).

        :return: None.
        """
        # refresh the board before updating conditions
        self._window.blit(self._surface, (BOARD_LEFT, BOARD_TOP))
        # if selected square coordinates list is not empty then color the square, row,
        # and column
        if self._selected_square_coords:
            self._color_selected_square()
            self._color_square_col()
            self._color_square_row()
        self._clear_button.update(mouse_position)
        self._solve_button.update(mouse_position)
        self._place_numbers()  # draw numbers on the Sudoku board
        self._draw_grid()  # draw grid lines on the board

    def get_number(self, row_index: int, col_index: int) -> str:
        """
        Returns the number in the Sudoku puzzle found in the position specified by
        `row_index` and `col_index`.

        :param row_index: The index of the row to get the number from.
        :param col_index: The index of the column to get the number from.
        :return: The number corresponding to the specified row index and column
            index.
        """
        return self._puzzle[row_index][col_index]

    def set_number_by_index(self, row_index: int, col_index: int, number: str) -> None:
        """
        Sets the square in the Sudoku puzzle corresponding to `row_index` and
        `col_index`.

        :param row_index: The index of the row to place the number in.
        :param col_index: The index of the column to place the number in.
        :param number: The number to place in the puzzle.
        :return: None.
        """
        self._puzzle[row_index][col_index] = number

    def set_number_by_selected(self, number: any) -> None:
        """
        Sets the `number` in the puzzle row / col corresponding to the currently
        selected square.

        :param number: The number to set.
        :return: None.
        """
        # calculate row and column indices based on selected square coordinates
        row = (self._selected_square_coords[1] - BOARD_TOP) // SQUARE_HEIGHT
        col = (self._selected_square_coords[0] - BOARD_LEFT) // SQUARE_WIDTH

        # update underlying puzzle data structure with `number` at calculated
        #   row and column indices
        self._puzzle[row][col] = str(number)

    def set_selected_square_coords(self, x_coord: int, y_coord: int) -> None:
        """
        Sets the x-coordinate and y-coordinate of the selected square.

        :param x_coord: The x-coordinate of the selected square.
        :param y_coord: The y-coordinate of the selected square.
        :return: None.
        """
        # if coordinates list is empty, append x and y coordinates:
        if not self._selected_square_coords:
            self._selected_square_coords.append(x_coord)
            self._selected_square_coords.append(y_coord)
        # if coordinates list is not empty, update index 0 and 1 with x and y coordinates
        else:
            self._selected_square_coords[0], self._selected_square_coords[1] = x_coord, y_coord

    def solve_button_click(self) -> None:
        """
        Clicks the solve puzzle button.

        :return: None
        """
        self._solve_button.click()

    def solve_button_unclick(self) -> None:
        """
        Unclicks the solve puzzle button.

        :return: None.
        """
        self._solve_button.unclick()

    def clear_board(self) -> None:
        self._puzzle = [[".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", ".", "."],
                        ]

    def solve_sudoku(self) -> bool:
        """
        Return a boolean signaling whether or not the solving algorithm should begin
        execution.

        :return: True if solving algorithm should start. Otherwise, False.
        """
        return self._solve_button.is_clicked()

    def solved(self) -> bool:
        """
        Searches each row in the Sudoku puzzle to determine if a solution has been
        found.

        :return: True if a solution has been found. Otherwise, False.
        """
        if '.' in self._puzzle[0] or '.' in self._puzzle[1] or '.' in self._puzzle[2] or \
                '.' in self._puzzle[3] or '.' in self._puzzle[4] or '.' in self._puzzle[5] or \
                '.' in self._puzzle[5] or '.' in self._puzzle[7] or '.' in self._puzzle[8]:
            return False
        return True

    def is_preset(self, row_index: int, col_index: int) -> bool:
        """
        Determines whether a board value is a preset value or not.

        :param row_index: The row corresponding to the value in the puzzle to check.
        :param col_index: The column corresponding to the value in the puzzle to check.
        :return: True if the value is preset. Otherwise, False.
        """
        if self._puzzle_presets[row_index][col_index]:
            return True
        else:
            return False

    def lock_presets(self) -> None:
        """
        Locks preset puzzle values into place by setting the puzzle presets attribute
        equal to a boolean matrix where True is a preset value and False is a variable
        value.

        :return: None.
        """
        self._puzzle_presets = self._find_presets()

    def in_row(self, row_index: int, number: str) -> bool:
        """
        Searches the Sudoku puzzle to see if `number` exists in the specified row index.

        :param row_index: The row index in the Sudoku puzzle to search in.
        :param number: The number to search for.
        :return: True if the number is found in the row. Otherwise, False.
        """
        # return true if `number` is in the row corresponding to the row index
        if number in self._puzzle[row_index]:
            return True
        return False  # number not found in row, return false

    def in_col(self, col_index: int, number: str) -> bool:
        """
        Searches the Sudoku puzzle to see if 'number' exists in the specified column
        index.

        :param col_index: The column index in the Sudoku puzzle to search in.
        :param number: The number to search for.
        :return: True if the number is found in the column. Otherwise, False.
        """
        # iterate through each row in the puzzle
        for row in self._puzzle:
            # search for `number` in the current row at the column index
            if row[col_index] == number:
                return True  # number found, return True
        return False  # number not in column, return false

    def in_square(self, row_index: int, col_index: int, number: str) -> bool:
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
        # create a hash table for each Sudoku puzzle square and a list of corresponding
        #   puzzle values
        squares = {1: self._puzzle[0][:3] + self._puzzle[1][:3] + self._puzzle[2][:3],
                   2: self._puzzle[0][3:6] + self._puzzle[1][3:6] + self._puzzle[2][3:6],
                   3: self._puzzle[0][6:] + self._puzzle[1][6:] + self._puzzle[2][6:],
                   4: self._puzzle[3][:3] + self._puzzle[4][:3] + self._puzzle[5][:3],
                   5: self._puzzle[3][3:6] + self._puzzle[4][3:6] + self._puzzle[5][3:6],
                   6: self._puzzle[3][6:] + self._puzzle[4][6:] + self._puzzle[5][6:],
                   7: self._puzzle[6][:3] + self._puzzle[7][:3] + self._puzzle[8][:3],
                   8: self._puzzle[6][3:6] + self._puzzle[7][3:6] + self._puzzle[8][3:6],
                   9: self._puzzle[6][6:] + self._puzzle[7][6:] + self._puzzle[8][6:]
                   }

        # the row index of the number is 0, 1, or 2
        if row_index == 0 or row_index == 1 or row_index == 2:
            # column index of the number is 0, 1, or 2
            if 0 <= col_index < 3:
                if number in squares[1]:
                    return True
                return False
            # column index of the number is 3, 4, or 5
            elif 3 <= col_index < 6:
                if number in squares[2]:
                    return True
                return False
            # column index of the number is 6, 7, or 8
            else:
                if number in squares[3]:
                    return True
                return False
        # the row index of the number is 3, 4, or 5
        elif row_index == 3 or row_index == 4 or row_index == 5:
            # column index of the numbers is 0, 1, or 2
            if 0 <= col_index < 3:
                if number in squares[4]:
                    return True
                return False
            # column index of the numbers is 3, 4, or 5
            elif 3 <= col_index < 6:
                if number in squares[5]:
                    return True
                return False
            # column index of the numbers is 6, 7, or 8
            else:
                if number in squares[6]:
                    return True
                return False
        # the row index of the number is 6, 7 or 8
        else:
            # column index of the numbers is 0, 1, or 2
            if 0 <= col_index < 3:
                if number in squares[7]:
                    return True
                return False
            # column index of the numbers is 3, 4, or 5
            elif 3 <= col_index < 6:
                if number in squares[8]:
                    return True
                return False
            # column index of the numbers is 6, 7, or 8
            else:
                if number in squares[9]:
                    return True
                return False

    def _find_presets(self) -> list:
        """
        Iterates through the initial Sudoku puzzle and determines which values are preset and
        which values are variable.

        :return: A matrix (list-of-lists) containing boolean values - True for preset, False
            for variable.
        """
        preset_values = []
        for row_index, row in enumerate(self._puzzle):
            preset_row = []
            for col_index, col_value in enumerate(row):
                if col_value == '.':
                    preset_row.append(False)
                else:
                    preset_row.append(True)
            preset_values.append(list(preset_row))
            preset_row.clear()
        return preset_values

    def _place_numbers(self) -> None:
        """
        Places the numbers set in the puzzle onto the Sudoku Board.

        :return: None.
        """
        for row_index, row in enumerate(self._puzzle):
            for col_index, number in enumerate(row):
                if number != ".":
                    font = pygame.font.SysFont('Arial', 30)
                    number_surface = font.render(number, True, BLACK)
                    self._window.blit(number_surface,
                                      (BOARD_LEFT + (SQUARE_WIDTH * col_index) + (SQUARE_WIDTH / 2) - 5,
                                       BOARD_TOP + (SQUARE_HEIGHT * row_index) + (SQUARE_HEIGHT / 4) - 5
                                       )
                                      )

    def _color_selected_square(self) -> None:
        """
        Colors the selected square.

        :return: None.
        """
        # draw and color a pygame rectangle to show the selected square
        pygame.draw.rect(self._window,
                         SQUARE_BLUE,
                         pygame.Rect(self._selected_square_coords[0],
                                     self._selected_square_coords[1],
                                     SQUARE_WIDTH,
                                     SQUARE_HEIGHT)
                         )

    def _color_square_row(self) -> None:
        """
        Colors the row corresponding to the selected square.

        :return: None.
        """
        # create and blit a pygame Surface to show the row corresponding to the selected
        #   square
        row_surface = pygame.Surface((BOARD_WIDTH, SQUARE_HEIGHT))
        row_surface.set_alpha(100)
        row_surface.fill(SQUARE_BLUE)
        self._window.blit(row_surface, (BOARD_LEFT, self._selected_square_coords[1]))

    def _color_square_col(self) -> None:
        """
        Colors the column corresponding to the selected square.

        :return: None.
        """
        # create and blit a pygame Surface to show the column corresponding to the selected
        #   square
        col_surface = pygame.Surface((SQUARE_WIDTH, BOARD_HEIGHT))
        col_surface.set_alpha(100)
        col_surface.fill(SQUARE_BLUE)
        self._window.blit(col_surface, (self._selected_square_coords[0], BOARD_TOP))

    def _draw_grid(self) -> None:
        """
        Draws the grid used in Sudoku on the Board.

        :return: None.
        """
        # draw the outline of the grid
        pygame.draw.rect(
            self._window,
            BLACK,
            pygame.Rect(
                BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT),
            width=3
        )
        self._draw_vertical_grid_lines()  # draw vertical grid lines
        self._draw_horizontal_grid_lines()  # draw horizontal grid lines

    def _draw_vertical_grid_lines(self) -> None:
        """
        Draws vertical grid lines on the Board.

        :return: None.
        """
        line_count = 1
        for x_coord in range(BOARD_LEFT + SQUARE_WIDTH, BOARD_WIDTH + BOARD_LEFT + SQUARE_WIDTH, SQUARE_WIDTH):
            width = 1 if line_count % 3 != 0 else 3
            pygame.draw.line(self._window,
                             BLACK,
                             (x_coord, BOARD_TOP),
                             (x_coord, BOARD_HEIGHT + BOARD_TOP),
                             width=width
                             )
            line_count += 1

    def _draw_horizontal_grid_lines(self) -> None:
        """
        Draws horizontal grid lines on the Board.

        :return: None.
        """
        line_count = 1
        for y_coord in range(BOARD_TOP + SQUARE_HEIGHT, BOARD_HEIGHT + BOARD_TOP + SQUARE_HEIGHT, SQUARE_HEIGHT):
            width = 1 if line_count % 3 != 0 else 3
            pygame.draw.line(self._window,
                             BLACK,
                             (BOARD_LEFT, y_coord),
                             (BOARD_LEFT + BOARD_WIDTH, y_coord),
                             width=width
                             )
            line_count += 1

    def __str__(self) -> None:
        """
        Prints the current puzzle values in a human-readable format.

        :return: None.
        """
        output = ''  # initialize the string to return
        # iterate through each row in the puzzle
        for row in self._puzzle:
            # iterate through each value in the current row
            for index, value in enumerate(row):
                # append value to output string, if index is 8 then start a new line
                output = (output + value + '\n') if index == 8 else (output + value + ' ')
        return output


class Button(object):
    """Represents a button."""
    def __init__(self, board, text: str, left: int, top: int):
        """Creates a Button object."""
        self._clicked = False
        self._board = board
        self._text = text
        self._left = left
        self._top = top

    def update(self, mouse_position: tuple) -> None:
        """
        Updates the states of the Button.

        :param mouse_position: The current position of the user's mouse.
        :return: None.
        """
        if (self._left <= mouse_position[0] <= self._left + BUTTON_WIDTH) and \
                (self._top <= mouse_position[1] <= self._top + BUTTON_HEIGHT):
            color = DARK_GREY
        else:
            color = LIGHT_GREY
        self._draw_button(color)
        self._button_text()

    def is_clicked(self) -> bool:
        """
        Returns a boolean representing whether a Button has been clicked or not.

        :return: True if the button has been clicked. Otherwise, False.
        """
        return self._clicked

    def click(self) -> None:
        """
        Clicks a Button by setting the clicked attribute to True.

        :return: None.
        """
        self._clicked = True

    def unclick(self) -> None:
        """
        Un-clicks a Button by setting the clicked attribute to False.

        :return: None.
        """
        self._clicked = False

    def _draw_button(self, color: tuple) -> None:
        """
        Draws the button on the screen.

        :param color: The color of the button.
        :return: None.
        """
        pygame.draw.rect(self._board,
                         color,
                         pygame.Rect(self._left,
                                     self._top,
                                     BUTTON_WIDTH,
                                     BUTTON_HEIGHT)
                         )

    def _button_text(self) -> None:
        """
        Displays the text "Solve Puzzle" inside of the Button.

        :return: None.
        """
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render(self._text, True, BLACK)
        self._board.blit(text_surface, (self._left + 15, self._top + 2))


if __name__ == "__main__":
    sudoku = SudokuSolver()
    sudoku.run()
