# Author: Colin Francis
# Description: Implementation of the sudoku board using Pygame

import pygame
from settings import *


class SudokuSolver(object):
    """A class used to solve Sudoku puzzles."""
    def __init__(self, puzzle):
        """Creates a SudokuSolver object."""
        self._puzzle = puzzle
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
                if event.type == pygame.QUIT:
                    self._running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._board.set_selected(mouse_pos()[0], mouse_pos()[1])
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        self._board.set_number(1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        self._board.set_number(2)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        self._board.set_number(3)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        self._board.set_number(4)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        self._board.set_number(5)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        self._board.set_number(6)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        self._board.set_number(7)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        self._board.set_number(8)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        self._board.set_number(9)

            self._board.update_board(pygame.mouse.get_pos())
            pygame.display.update()


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

    def set_selected(self, x_coord: int, y_coord: int) -> None:
        """
        Sets the x-coordinate and y-coordinate of the selected square.

        :param x_coord: The x-coordinate of the selected square.
        :param y_coord: The y-coordinate of the selected square.
        :return: None.
        """
        self._selected_square[0], self._selected_square[1] = x_coord, y_coord

    def set_number(self, number: int) -> None:
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
    solve = SudokuSolver(sudoku_puzzle)
    solve.run()
