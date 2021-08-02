# Description: Implementation of the sudoku board using Pygame
import pygame
from settings import *


class SudokuSolver(object):
    def __init__(self, puzzle):
        self._puzzle = puzzle
        self._board = Board()
        self._running = True

    def run(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            self._board.update_board()
            pygame.display.update()


class Board(object):
    def __init__(self):
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._screen.fill(WHITE)
        pygame.display.set_caption('Sudoku Solver')

    def update_board(self):
        self._draw_grid()

    def _draw_grid(self):
        pygame.draw.rect(self._screen, BLACK, pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT), width=3)


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
