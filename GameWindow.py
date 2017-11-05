import pygame, os, sys
import numpy
from numpy import *
from pygame.locals import *

#################################################################
#                  Initializations and constants                #
#################################################################

# Initialize pygame
pygame.init()

# Set window to full screen and get screen info
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = screen.get_size()

# Game clock rename (used to set up frames per second)
clock = pygame.time.Clock()

# Set window title
pygame.display.set_caption("Saboteur")

CARD_AREA_BACKGROUND_FILE = "Resources/CardAreaBackground.png"
PLAYER_LIST_AREA_BACKGROUND_FILE = "Resources/PlayerListBackground.png"
#PATH_CARD_BACK_FILE = "Resources/PathBack.jpg"
PATH_CARD_BACK_FILE = "Resources/Coal.jpg"


#################################################################
#               End Initializations and constants               #
#################################################################


# Function to convert tuples into integer tuples
def convert_to_int_tuple(x):
    res = ()
    for element in x:
        res += (int(element),)
    return res


def wait():
    while 1:
        ''' Pause Until Input is Given '''
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN and e.key == K_SPACE:
            break


# Set window area sizes based on screen size

# Card Area
card_area_percentage = array((0.15, 1))
card_area_size = convert_to_int_tuple(screen_size * card_area_percentage)
card_area_position = 0, 0
card_area = Rect(card_area_position, card_area_size)
card_area_background = pygame.image.load(CARD_AREA_BACKGROUND_FILE)
card_area_background = pygame.transform.smoothscale(card_area_background, card_area_size)

# Player List Area
player_list_area_percentage = array((0.15, 1))
player_list_area_size = convert_to_int_tuple(screen_size * player_list_area_percentage)
player_list_area_position = (screen_size[0] - player_list_area_size[0] - 1, 0)
player_list_area = Rect(player_list_area_position, player_list_area_size)
player_list_background = pygame.image.load(PLAYER_LIST_AREA_BACKGROUND_FILE)
player_list_background = pygame.transform.smoothscale(player_list_background, player_list_area_size)

# Board Area
board_area_percentage = array((0.7, 1))
board_area_size = convert_to_int_tuple(screen_size * board_area_percentage)
board_area_position = (card_area_size[0], 0)
board_area = Rect(board_area_position, board_area_size)


#################################################################
#                          Card Class                           #
#################################################################

class Card:

    def __init__(self, card_size, front_face_file, back_face_file=None, revealed=True):
        self.card_size = card_size
        self.front_face = pygame.image.load(front_face_file)
        self.front_face = pygame.transform.smoothscale(self.front_face, self.card_size)
        self.revealed = revealed

        if back_face_file is None:
            self.back_face = self.front_face
        else:
            self.back_face = pygame.image.load(back_face_file)
            self.back_face = pygame.transform.smoothscale(self.back_face, self.card_size)


#################################################################
#                          Board Class                          #
#################################################################

class Board:

    def __init__(self, board_cell_numbers=None):
        # Board size, number of cells: Width/Height, Width >= 5, Height >= 9
        self.DEFAULT_BOARD_SIZE = array((9, 11))
        if board_cell_numbers is None:
            self.board_cell_numbers = self.DEFAULT_BOARD_SIZE
        else:
            self.board_cell_numbers = board_cell_numbers
        self.card_size = board_area_size // self.board_cell_numbers
        # create a grid with the specified dimensions, but no lower than 5 width and 9 height
        self.grid = [[Card(self.card_size, PATH_CARD_BACK_FILE)
                      for x in range(max(self.board_cell_numbers[0], 9))]
                     for y in range(max(self.board_cell_numbers[1], 5))]
        self.board_surface = pygame.Surface(board_area_size).convert()

    def draw_board(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pos = (j * self.card_size[0], i * self.card_size[1])
                self.board_surface.blit(self.grid[i][j].front_face, pos, self.grid[i][j].front_face.get_rect())


black = (0, 0, 0)
pink = (255, 132, 188)
blue = (0, 0, 255)
b = Board()
b.draw_board()

screen.blit(card_area_background, card_area_position)
screen.blit(player_list_background, player_list_area_position)
screen.blit(b.board_surface, board_area_position)
pygame.display.update()

# clock.tick(1)


# this calls the 'main' function when this script is executed
# if __name__ == '__main__':
#    main()
wait()