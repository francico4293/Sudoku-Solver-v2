# Author: Colin Francis
# Description: Contains settings for sudoku solver

import pygame

# Screen Constants:
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 550

# Board Constants:
BOARD_LEFT, BOARD_TOP = 25, 75
BOARD_WIDTH, BOARD_HEIGHT = 450, 450
SQUARE_HEIGHT, SQUARE_WIDTH = 50, 50

# Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SQUARE_BLUE = (72, 199, 253)


# Utilities:
# Mouse Position Function
def mouse_pos():
    """

    :return:
    """
    for row in range(9):
        for col in range(9):
            if (BOARD_LEFT + (SQUARE_WIDTH * row) < pygame.mouse.get_pos()[0] <=
                BOARD_LEFT + (SQUARE_WIDTH * (row + 1))) and (BOARD_TOP + (SQUARE_HEIGHT * col)) < \
                    pygame.mouse.get_pos()[1] <= BOARD_TOP + (SQUARE_HEIGHT * (col + 1)):
                return BOARD_LEFT + (SQUARE_WIDTH * row), BOARD_TOP + (SQUARE_HEIGHT * col)
    return None, None
