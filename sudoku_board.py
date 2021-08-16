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

    def run(self) -> None:
        """

        :return:
        """
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._board.set_selected(mouse_pos()[0], mouse_pos()[1])

            self._board.update_board()
            pygame.display.update()


class Board(object):
    """Represents a Sudoku Board."""
    def __init__(self):
        """Creates a Board object."""
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self._screen.fill(WHITE)
        self._surface.fill(WHITE)
        self._selected_square = [None] * 2
        pygame.display.set_caption('Sudoku Solver')

    def update_board(self):
        """
        Updates the state of the Sudoku Board.

        :return: None.
        """
        self._screen.blit(self._surface, (BOARD_LEFT, BOARD_TOP))
        if self._selected_square != [None] * 2:
            self._color_selected()
            self._color_row()
            self._color_col()
        self._draw_grid()

    def set_selected(self, x_coord: int, y_coord: int) -> None:
        """
        Sets the x-coordinate and y-coordinate of the selected square.

        :param x_coord: The x-coordinate of the selected square.
        :param y_coord: The y-coordinate of the selected square.
        :return: None.
        """
        self._selected_square[0], self._selected_square[1] = x_coord, y_coord

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
