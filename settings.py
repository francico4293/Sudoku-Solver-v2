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
    if (BOARD_LEFT < pygame.mouse.get_pos()[0] <= BOARD_LEFT + SQUARE_WIDTH) and \
            (BOARD_TOP < pygame.mouse.get_pos()[1] <= BOARD_TOP + SQUARE_HEIGHT):
        return BOARD_LEFT, BOARD_TOP
    elif (BOARD_LEFT + SQUARE_WIDTH < pygame.mouse.get_pos()[0] <= BOARD_LEFT + (SQUARE_WIDTH * 2)) and \
            (BOARD_TOP < pygame.mouse.get_pos()[1] <= BOARD_TOP + SQUARE_HEIGHT):
        return BOARD_LEFT + SQUARE_WIDTH, BOARD_TOP
    elif (BOARD_LEFT + (SQUARE_WIDTH * 2) < pygame.mouse.get_pos()[0] <= BOARD_LEFT + (SQUARE_WIDTH * 3)) and \
            (BOARD_TOP < pygame.mouse.get_pos()[1] <= BOARD_TOP + SQUARE_HEIGHT):
        return BOARD_LEFT + (SQUARE_WIDTH * 2), BOARD_TOP
    elif (BOARD_LEFT + (SQUARE_WIDTH * 3) < pygame.mouse.get_pos()[0] <= BOARD_LEFT + (SQUARE_WIDTH * 4)) and \
            (BOARD_TOP < pygame.mouse.get_pos()[1] <= BOARD_TOP + SQUARE_HEIGHT):
        return BOARD_LEFT + (SQUARE_WIDTH * 3), BOARD_TOP
    elif (BOARD_LEFT + (SQUARE_WIDTH * 4) < pygame.mouse.get_pos()[0] <= BOARD_LEFT + (SQUARE_WIDTH * 5)) and \
            (BOARD_TOP < pygame.mouse.get_pos()[1] <= BOARD_TOP + SQUARE_HEIGHT):
        return BOARD_LEFT + (SQUARE_WIDTH * 4), BOARD_TOP
    elif (BOARD_LEFT + (SQUARE_WIDTH * 5) < pygame.mouse.get_pos()[0] <= BOARD_LEFT + (SQUARE_WIDTH * 6)) and \
            (BOARD_TOP < pygame.mouse.get_pos()[1] <= BOARD_TOP + SQUARE_HEIGHT):
        return BOARD_LEFT + (SQUARE_WIDTH * 5), BOARD_TOP
    elif (BOARD_LEFT + (SQUARE_WIDTH * 6) < pygame.mouse.get_pos()[0] <= BOARD_LEFT + (SQUARE_WIDTH * 7)) and \
            (BOARD_TOP < pygame.mouse.get_pos()[1] <= BOARD_TOP + SQUARE_HEIGHT):
        return BOARD_LEFT + (SQUARE_WIDTH * 6), BOARD_TOP
    elif (BOARD_LEFT + (SQUARE_WIDTH * 7) < pygame.mouse.get_pos()[0] <= BOARD_LEFT + (SQUARE_WIDTH * 8)) and \
            (BOARD_TOP < pygame.mouse.get_pos()[1] <= BOARD_TOP + SQUARE_HEIGHT):
        return BOARD_LEFT + (SQUARE_WIDTH * 7), BOARD_TOP
    elif (BOARD_LEFT + (SQUARE_WIDTH * 8) < pygame.mouse.get_pos()[0] <= BOARD_LEFT + (SQUARE_WIDTH * 9)) and \
            (BOARD_TOP < pygame.mouse.get_pos()[1] <= BOARD_TOP + SQUARE_HEIGHT):
        return BOARD_LEFT + (SQUARE_WIDTH * 8), BOARD_TOP
    else:
        return None, None
