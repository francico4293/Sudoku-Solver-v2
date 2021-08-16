# Author: Colin Francis
# Description: Implementation of the sudoku board using Pygame

import pygame
import time
from settings import *


class SudokuSolver(object):
    """A class used to solve Sudoku puzzles."""
    def __init__(self):
        """Creates a SudokuSolver object."""
        self._board = Board()
        self._running = True
        pygame.font.init()

    def run(self) -> None:
        """
        Load a blank puzzle board, input the puzzle, and run the solver.

        :return: None.
        """
        while self._running:
            for event in pygame.event.get():
                # check if the user is trying to exit
                if event.type == pygame.QUIT:
                    self._running = False

                # check for a grid square being selected
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (BOARD_LEFT <= pygame.mouse.get_pos()[0] <= BOARD_LEFT + BOARD_WIDTH) and \
                            (BOARD_TOP <= pygame.mouse.get_pos()[1] <= BOARD_TOP + BOARD_HEIGHT):
                        self._board.set_selected_coords(mouse_pos()[0], mouse_pos()[1])
                    elif (BUTTON_LEFT <= pygame.mouse.get_pos()[0] <= BUTTON_LEFT + BUTTON_WIDTH) and \
                            (BUTTON_TOP <= pygame.mouse.get_pos()[1] <= BUTTON_TOP + BUTTON_HEIGHT):
                        self._board.click()

                # check for a number being entered
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        self._board.set_number_by_selected(1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        self._board.set_number_by_selected(2)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        self._board.set_number_by_selected(3)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        self._board.set_number_by_selected(4)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        self._board.set_number_by_selected(5)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        self._board.set_number_by_selected(6)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        self._board.set_number_by_selected(7)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        self._board.set_number_by_selected(8)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        self._board.set_number_by_selected(9)

                if self._board.solve():
                    self._solve()

            self._board.update_board(pygame.mouse.get_pos())  # update the game board
            pygame.display.update()  # update the display

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

            self._board.set_selected_coords(BOARD_LEFT + (SQUARE_HEIGHT * col_index),
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
            self._board.update_board(pygame.mouse.get_pos())  # update the game board
            pygame.display.update()  # update the display
        end_time = time.perf_counter()
        print("Solution Speed: {:.2f}s".format(end_time - start_time))
        # self.print_board()

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
    """Represents a Sudoku Board."""
    def __init__(self):
        """Creates a Board object."""
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self._screen.fill(WHITE)
        self._surface.fill(WHITE)
        self._button = Button(self._screen)
        self._selected_square = [None] * 2
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
        self._puzzle_presets = None
        pygame.display.set_caption('Sudoku Solver')

    def update_board(self, mouse_position):
        """
        Updates the state of the Sudoku Board.

        :return: None.
        """
        self._screen.blit(self._surface, (BOARD_LEFT, BOARD_TOP))
        if self._selected_square != [None] * 2:
            self._color_selected()
            self._color_row()
            self._color_col()
        self._button.update(mouse_position)
        self._place_numbers()
        self._draw_grid()

    def solve(self) -> bool:
        return self._button.is_clicked()

    def click(self):
        self._button.click()

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

    def lock_presets(self):
        self._puzzle_presets = self._find_presets()

    def set_selected_coords(self, x_coord: int, y_coord: int) -> None:
        """
        Sets the x-coordinate and y-coordinate of the selected square.

        :param x_coord: The x-coordinate of the selected square.
        :param y_coord: The y-coordinate of the selected square.
        :return: None.
        """
        self._selected_square[0], self._selected_square[1] = x_coord, y_coord

    def set_number_by_selected(self, number: int) -> None:
        """
        Sets the `number` in the puzzle row / col corresponding to the currently
        selected square.

        :param number: The number to set.
        :return: None.
        """
        if self._selected_square == [None] * 2:
            return

        row = (self._selected_square[1] - BOARD_TOP) // SQUARE_HEIGHT
        col = (self._selected_square[0] - BOARD_LEFT) // SQUARE_WIDTH

        self._puzzle[row][col] = str(number)

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

    def in_row(self, row_index: int, number: str) -> bool:
        """
        Searches the Sudoku puzzle to see if `number` exists in the specified row index.

        :param row_index: The row index in the Sudoku puzzle to search in.
        :param number: The number to search for.
        :return: True if the number is found in the row. Otherwise, False.
        """
        if number in self._puzzle[row_index]:
            return True
        return False

    def in_col(self, col_index: int, number: str) -> bool:
        """
        Searches the Sudoku puzzle to see if 'number' exists in the specified column
        index.

        :param col_index: The column index in the Sudoku puzzle to search in.
        :param number: The number to search for.
        :return: True if the number is found in the column. Otherwise, False.
        """
        for row in self._puzzle:
            if row[col_index] == number:
                return True
        return False

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

    def _place_numbers(self) -> None:
        """
        Places the numbers set in the puzzle onto the Sudoku Board.

        :return: None.
        """
        # TODO: Find a better way to center the number
        for row_index, row in enumerate(self._puzzle):
            for col_index, number in enumerate(row):
                if number != ".":
                    font = pygame.font.SysFont('Arial', 30)
                    number_surface = font.render(number, True, BLACK)
                    self._screen.blit(number_surface,
                                      (BOARD_LEFT + (SQUARE_WIDTH * col_index) + (SQUARE_WIDTH / 2) - 5,
                                       BOARD_TOP + (SQUARE_HEIGHT * row_index) + (SQUARE_HEIGHT / 4) - 5
                                       )
                                      )

    def _draw_grid(self) -> None:
        """
        Draws the grid used in Sudoku on the Board.

        :return: None.
        """
        pygame.draw.rect(self._screen,
                         BLACK,
                         pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT),
                         width=3
                         )
        self._draw_vert_grid_lines()
        self._draw_horz_grid_lines()

    def _draw_vert_grid_lines(self) -> None:
        """
        Draws vertical grid lines on the Board.

        :return: None.
        """
        grid_count = 1
        for x_coord in range(BOARD_LEFT + SQUARE_WIDTH, BOARD_WIDTH + BOARD_LEFT + SQUARE_WIDTH, SQUARE_WIDTH):
            width = 1 if grid_count % 3 != 0 else 3
            pygame.draw.line(self._screen,
                             BLACK,
                             (x_coord, BOARD_TOP),
                             (x_coord, BOARD_HEIGHT + BOARD_TOP),
                             width=width
                             )
            grid_count += 1

    def _draw_horz_grid_lines(self) -> None:
        """
        Draws horizontal grid lines on the Board.

        :return: None.
        """
        grid_count = 1
        for y_coord in range(BOARD_TOP + SQUARE_HEIGHT, BOARD_HEIGHT + BOARD_TOP + SQUARE_HEIGHT, SQUARE_HEIGHT):
            width = 1 if grid_count % 3 != 0 else 3
            pygame.draw.line(self._screen,
                             BLACK,
                             (BOARD_LEFT, y_coord),
                             (BOARD_LEFT + BOARD_WIDTH, y_coord),
                             width=width
                             )
            grid_count += 1

    def _color_selected(self) -> None:
        """
        Colors the selected square.

        :return: None.
        """
        pygame.draw.rect(self._screen,
                         SQUARE_BLUE,
                         pygame.Rect(self._selected_square[0],
                                     self._selected_square[1],
                                     SQUARE_WIDTH,
                                     SQUARE_HEIGHT)
                         )

    def _color_row(self) -> None:
        """
        Colors the row corresponding to the selected square.

        :return: None.
        """
        row_surface = pygame.Surface((BOARD_WIDTH, SQUARE_HEIGHT))
        row_surface.set_alpha(100)
        row_surface.fill(SQUARE_BLUE)
        self._screen.blit(row_surface, (BOARD_LEFT, self._selected_square[1]))

    def _color_col(self) -> None:
        """
        Colors the column corresponding to the selected square.

        :return: None.
        """
        col_surface = pygame.Surface((SQUARE_WIDTH, BOARD_HEIGHT))
        col_surface.set_alpha(100)
        col_surface.fill(SQUARE_BLUE)
        self._screen.blit(col_surface, (self._selected_square[0], BOARD_TOP))

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


class Button(object):
    """"""
    def __init__(self, board):
        """"""
        self._clicked = False
        self._board = board

    def update(self, mouse_position: tuple) -> None:
        """
        Updates the states of the Button.

        :param mouse_position: The current position of the user's mouse.
        :return: None.
        """
        if (BUTTON_LEFT <= mouse_position[0] <= BUTTON_LEFT + BUTTON_WIDTH) and \
                (BUTTON_TOP <= mouse_position[1] <= BUTTON_TOP + BUTTON_HEIGHT):
            color = DARK_GREY
        else:
            color = LIGHT_GREY
        self._draw_button(color)
        self._button_text()

    def is_clicked(self):
        return self._clicked

    def click(self):
        self._clicked = True

    def _draw_button(self, color: tuple) -> None:
        """
        Draws the button on the screen.

        :param color: The color of the button.
        :return: None.
        """
        pygame.draw.rect(self._board,
                         color,
                         pygame.Rect(BUTTON_LEFT,
                                     BUTTON_TOP,
                                     BUTTON_WIDTH,
                                     BUTTON_HEIGHT)
                         )

    def _button_text(self) -> None:
        """
        Displays the text "Solve Puzzle" inside of the Button.

        :return: None.
        """
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render('Solve Puzzle', True, BLACK)
        self._board.blit(text_surface, (BUTTON_LEFT + 15, BUTTON_TOP + 2))


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
    solve = SudokuSolver()
    solve.run()
