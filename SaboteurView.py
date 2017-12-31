import pygame
from pygame.locals import *
from numpy import *
import SaboteurModel as sm

########################################################################################################################
#                                     Initialization and helper functions                                              #
########################################################################################################################


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

CARD_BACK_FILE = "Resources/SpecialCards/CardBack.jpg"

PATH_CARD_NSEW__FRONT_FILE = "Resources/PathCards/NSEW.jpg"
PATH_CARD_NSEWC_FRONT_FILE = "Resources/PathCards/NSEWC.jpg"
PATH_CARD_NSE___FRONT_FILE = "Resources/PathCards/NSE.jpg"
PATH_CARD_NSE_C_FRONT_FILE = "Resources/PathCards/NSEC.jpg"
PATH_CARD_NS_W__FRONT_FILE = "Resources/PathCards/NSW.jpg"
PATH_CARD_NS_WC_FRONT_FILE = "Resources/PathCards/NSWC.jpg"
PATH_CARD_NS____FRONT_FILE = "Resources/PathCards/NS.jpg"
PATH_CARD_NS__C_FRONT_FILE = "Resources/PathCards/NSC.jpg"
PATH_CARD_N_EW__FRONT_FILE = "Resources/PathCards/NEW.jpg"
PATH_CARD_N_EWC_FRONT_FILE = "Resources/PathCards/NEWC.jpg"
PATH_CARD_N_E___FRONT_FILE = "Resources/PathCards/NE.jpg"
PATH_CARD_N_E_C_FRONT_FILE = "Resources/PathCards/NEC.jpg"
PATH_CARD_N__W__FRONT_FILE = "Resources/PathCards/NW.jpg"
PATH_CARD_N__WC_FRONT_FILE = "Resources/PathCards/NWC.jpg"
PATH_CARD_N_____FRONT_FILE = "Resources/PathCards/N.jpg"
PATH_CARD_N___C_FRONT_FILE = "Resources/PathCards/NC.jpg"
PATH_CARD__SEW__FRONT_FILE = "Resources/PathCards/SEW.jpg"
PATH_CARD__SEWC_FRONT_FILE = "Resources/PathCards/SEWC.jpg"
PATH_CARD__SE___FRONT_FILE = "Resources/PathCards/SE.jpg"
PATH_CARD__SE_C_FRONT_FILE = "Resources/PathCards/SEC.jpg"
PATH_CARD__S_W__FRONT_FILE = "Resources/PathCards/SW.jpg"
PATH_CARD__S_WC_FRONT_FILE = "Resources/PathCards/SWC.jpg"
PATH_CARD__S____FRONT_FILE = "Resources/PathCards/S.jpg"
PATH_CARD__S__C_FRONT_FILE = "Resources/PathCards/SC.jpg"
PATH_CARD___EW__FRONT_FILE = "Resources/PathCards/EW.jpg"
PATH_CARD___EWC_FRONT_FILE = "Resources/PathCards/EWC.jpg"
PATH_CARD___E___FRONT_FILE = "Resources/PathCards/E.jpg"
PATH_CARD___E_C_FRONT_FILE = "Resources/PathCards/EC.jpg"
PATH_CARD____W__FRONT_FILE = "Resources/PathCards/W.jpg"
PATH_CARD____WC_FRONT_FILE = "Resources/PathCards/WC.jpg"

DEMOLISH_CARD_FRONT_FILE = "Resources/SpecialCards/Demolish.jpg"
SPY_CARD_FRONT_FILE = "Resources/SpecialCards/Spy.jpg"

BLOCK_PICK_CARD_FRONT_FILE = "Resources/SpecialCards/BlockPick.jpg"
UNBLOCK_PICK_CARD_FRONT_FILE = "Resources/SpecialCards/UnblockPick.jpg"

BLOCK_LAMP_CARD_FRONT_FILE = "Resources/SpecialCards/BlockLamp.jpg"
UNBLOCK_LAMP_CARD_FRONT_FILE = "Resources/SpecialCards/UnblockLamp.jpg"

BLOCK_CART_CARD_FRONT_FILE = "Resources/SpecialCards/BlockCart.jpg"
UNBLOCK_CART_CARD_FRONT_FILE = "Resources/SpecialCards/UnblockCart.jpg"

GOLD_DIGGER_FRONT_FILE = "Resources/SpecialCards/GoldDigger.jpg"
SABOTEUR_FRONT_FILE = "Resources/SpecialCards/Saboteur.jpg"

START_FRONT_FILE = "Resources/SpecialCards/StartCard.jpg"
GOLD_CARD_FRONT_FILE = "Resources/SpecialCards/Gold.jpg"
COAL_CARD_FRONT_FILE = "Resources/SpecialCards/Coal.jpg"
GOAL_CARD_BACK_FILE = "Resources/SpecialCards/GoalBack.jpg"


# Function to convert tuples into integer tuples
def convert_to_int_tuple(x):
    res = ()
    for element in x:
        res += (int(element),)
    return res


def divide_tuples(dividend, divisor):
    res = ()
    for i in range(min(len(dividend), len(divisor))):
        res += (dividend[i] // divisor[i],)
    return res


def wait():
    while 1:
        ''' Pause Until Input is Given '''
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
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
name_list_area_percentage = array((0.15, 1))
name_list_area_size = convert_to_int_tuple(screen_size * name_list_area_percentage)
name_list_area_position = (screen_size[0] - name_list_area_size[0] - 1, 0)
name_list_area = Rect(name_list_area_position, name_list_area_size)
name_list_area_background = pygame.image.load(PLAYER_LIST_AREA_BACKGROUND_FILE)
name_list_area_background = pygame.transform.smoothscale(name_list_area_background, name_list_area_size)

# Board Area
board_area_percentage = array((0.7, 1))
board_area_size = convert_to_int_tuple(screen_size * board_area_percentage)
board_area_position = (card_area_size[0], 0)


# board_area = Rect(board_area_position, board_area_size)


########################################################################################################################
#                                               CardView Class                                                         #
########################################################################################################################
class CardView:
    CARD_DICTIONARY = {
        "DEMOLISH": (DEMOLISH_CARD_FRONT_FILE, CARD_BACK_FILE),
        "SPY": (SPY_CARD_FRONT_FILE, CARD_BACK_FILE),

        "BLOCK_PICK": (BLOCK_PICK_CARD_FRONT_FILE, CARD_BACK_FILE),
        "UNBLOCK_PICK": (UNBLOCK_PICK_CARD_FRONT_FILE, CARD_BACK_FILE),

        "BLOCK_LAMP": (BLOCK_LAMP_CARD_FRONT_FILE, CARD_BACK_FILE),
        "UNBLOCK_LAMP": (UNBLOCK_LAMP_CARD_FRONT_FILE, CARD_BACK_FILE),

        "BLOCK_CART": (BLOCK_CART_CARD_FRONT_FILE, CARD_BACK_FILE),
        "UNBLOCK_CART": (UNBLOCK_CART_CARD_FRONT_FILE, CARD_BACK_FILE),

        "NSEW_": (PATH_CARD_NSEW__FRONT_FILE, CARD_BACK_FILE),
        "NSEWC": (PATH_CARD_NSEWC_FRONT_FILE, CARD_BACK_FILE),
        "NSE__": (PATH_CARD_NSE___FRONT_FILE, CARD_BACK_FILE),
        "NSE_C": (PATH_CARD_NSE_C_FRONT_FILE, CARD_BACK_FILE),
        "NS_W_": (PATH_CARD_NS_W__FRONT_FILE, CARD_BACK_FILE),
        "NS_WC": (PATH_CARD_NS_WC_FRONT_FILE, CARD_BACK_FILE),
        "NS___": (PATH_CARD_NS____FRONT_FILE, CARD_BACK_FILE),
        "NS__C": (PATH_CARD_NS__C_FRONT_FILE, CARD_BACK_FILE),
        "N_EW_": (PATH_CARD_N_EW__FRONT_FILE, CARD_BACK_FILE),
        "N_EWC": (PATH_CARD_N_EWC_FRONT_FILE, CARD_BACK_FILE),
        "N_E__": (PATH_CARD_N_E___FRONT_FILE, CARD_BACK_FILE),
        "N_E_C": (PATH_CARD_N_E_C_FRONT_FILE, CARD_BACK_FILE),
        "N__W_": (PATH_CARD_N__W__FRONT_FILE, CARD_BACK_FILE),
        "N__WC": (PATH_CARD_N__WC_FRONT_FILE, CARD_BACK_FILE),
        "N____": (PATH_CARD_N_____FRONT_FILE, CARD_BACK_FILE),
        "N___C": (PATH_CARD_N___C_FRONT_FILE, CARD_BACK_FILE),
        "_SEW_": (PATH_CARD__SEW__FRONT_FILE, CARD_BACK_FILE),
        "_SEWC": (PATH_CARD__SEWC_FRONT_FILE, CARD_BACK_FILE),
        "_SE__": (PATH_CARD__SE___FRONT_FILE, CARD_BACK_FILE),
        "_SE_C": (PATH_CARD__SE_C_FRONT_FILE, CARD_BACK_FILE),
        "_S_W_": (PATH_CARD__S_W__FRONT_FILE, CARD_BACK_FILE),
        "_S_WC": (PATH_CARD__S_WC_FRONT_FILE, CARD_BACK_FILE),
        "_S___": (PATH_CARD__S____FRONT_FILE, CARD_BACK_FILE),
        "_S__C": (PATH_CARD__S__C_FRONT_FILE, CARD_BACK_FILE),
        "__EW_": (PATH_CARD___EW__FRONT_FILE, CARD_BACK_FILE),
        "__EWC": (PATH_CARD___EWC_FRONT_FILE, CARD_BACK_FILE),
        "__E__": (PATH_CARD___E___FRONT_FILE, CARD_BACK_FILE),
        "__E_C": (PATH_CARD___E_C_FRONT_FILE, CARD_BACK_FILE),
        "___W_": (PATH_CARD____W__FRONT_FILE, CARD_BACK_FILE),
        "___WC": (PATH_CARD____WC_FRONT_FILE, CARD_BACK_FILE),
        "____C": (CARD_BACK_FILE, CARD_BACK_FILE),
        "_____": (CARD_BACK_FILE, CARD_BACK_FILE),

        "TYPE": (GOLD_DIGGER_FRONT_FILE, SABOTEUR_FRONT_FILE),

        "START": (START_FRONT_FILE, START_FRONT_FILE),
        "GOLD": (GOLD_CARD_FRONT_FILE, GOAL_CARD_BACK_FILE),
        "COAL": (COAL_CARD_FRONT_FILE, GOAL_CARD_BACK_FILE),
    }

    def __init__(self, card, card_size):
        """

        :param card:
        :param card_size:
        :type card: SM.Card
        :type card_size: ndarray of int
        """
        self.card = card
        self.card_size = card_size
        front_file, back_file = CardView.CARD_DICTIONARY.get(card.get_name())

        front_image = pygame.image.load(front_file)
        self.front_face = pygame.transform.smoothscale(front_image, self.card_size)

        back_image = pygame.image.load(back_file)
        self.back_face = pygame.transform.smoothscale(back_image, self.card_size)


########################################################################################################################
#                                               BoardView Class                                                        #
########################################################################################################################
class BoardView:

    # noinspection PyArgumentList
    def __init__(self, board, area_size):
        """

        :param board:
        :param area_size:
        :type board: SM.Board
        :type area_size: ndarray of int
        """
        self.board = board

        self.area_size = area_size
        self.board_card_size = area_size // array(self.board.cell_nr_width_height)

        self.gridView = [[CardView(self.board.grid[i][j], self.board_card_size)
                          for j in range(len(self.board.grid[i]))]
                         for i in range(len(self.board.grid))]
        self.board_surface = pygame.Surface(self.board_card_size * self.board.cell_nr_width_height).convert()

        for x in range(len(self.gridView)):
            for y in range(len(self.gridView[x])):
                screen_location = (x * self.board_card_size[0], y * self.board_card_size[1])
                if self.board.grid[x][y].revealed:
                    self.board_surface.blit(self.gridView[x][y].front_face,
                                            screen_location,
                                            self.gridView[x][y].front_face.get_rect())
                else:
                    self.board_surface.blit(self.gridView[x][y].back_face,
                                            screen_location,
                                            self.gridView[x][y].back_face.get_rect())

    def update(self, location=None):
        """

        :param location:
        :return:
        :type location: tuple of int
        """

        if location is None:
            for x in range(len(self.gridView)):
                for y in range(len(self.gridView[x])):
                    screen_location = (x * self.board_card_size[0], y * self.board_card_size[1])
                    self.gridView[x][y] = CardView(self.board.grid[x][y], self.board_card_size)
                    if self.board.grid[x][y].revealed:
                        self.board_surface.blit(self.gridView[x][y].front_face,
                                                screen_location,
                                                self.gridView[x][y].front_face.get_rect())
                    else:
                        self.board_surface.blit(self.gridView[x][y].back_face,
                                                screen_location,
                                                self.gridView[x][y].back_face.get_rect())
        else:
            x, y = location
            screen_location = (x * self.board_card_size[0], y * self.board_card_size[1])
            self.gridView[x][y] = CardView(self.board.grid[x][y], self.board_card_size)
            if self.board.grid[x][y].revealed:
                self.board_surface.blit(self.gridView[x][y].front_face,
                                        screen_location,
                                        self.gridView[x][y].front_face.get_rect())
            else:
                self.board_surface.blit(self.gridView[x][y].back_face,
                                        screen_location,
                                        self.gridView[x][y].back_face.get_rect())

            # check goals
            y = self.board.left_goal_location[1]
            for x in range(sm.NUMBER_OF_GOALS):
                x = self.board.left_goal_location[0] + 2 * x
                screen_location = (x * self.board_card_size[0], y * self.board_card_size[1])
                if self.board.grid[x][y].revealed:
                    self.board_surface.blit(self.gridView[x][y].front_face,
                                            screen_location,
                                            self.gridView[x][y].front_face.get_rect())
                else:
                    self.board_surface.blit(self.gridView[x][y].back_face,
                                            screen_location,
                                            self.gridView[x][y].back_face.get_rect())


black = (0, 0, 0)
pink = (255, 132, 188)
blue = (0, 0, 255)
smb = sm.Board()
b = BoardView(smb, board_area_size)

screen.blit(card_area_background, card_area_position)
screen.blit(name_list_area_background, name_list_area_position)

board_area = pygame.transform.smoothscale(b.board_surface, board_area_size)
screen.blit(board_area, board_area_position)
pygame.display.update()
b.board.print_board_with_coords()
wait()

# smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 2))
# smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 3))
# smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 4))
# smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 5))
# smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 6))
# smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 7))
# b.update((4,2))
# b.update((4,3))
# b.update((4,4))
# b.update((4,5))
# b.update((4,6))
# b.update((4,7))
# board_area = pygame.transform.smoothscale(b.board_surface, board_area_size)
# screen.blit(board_area, board_area_position)
# pygame.display.update()
# b.board.print_board_with_coords()
#
# wait()
# smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 8))
# b.update((4,8))
# board_area = pygame.transform.smoothscale(b.board_surface, board_area_size)
# screen.blit(board_area, board_area_position)
# pygame.display.update()
# b.board.print_board_with_coords()
# wait()

for i_ in range(2, 9):
    smb.place_card(sm.PathCard(True, True, True, True, True), (4, i_))
    b.update((4, i_))
    board_area = pygame.transform.smoothscale(b.board_surface, board_area_size)
    screen.blit(board_area, board_area_position)
    pygame.display.update()
    wait()

b.board.print_board_with_coords()

smb.place_card(sm.PathCard(True, True, True, True, True), (5, 9))
b.update((5, 9))
board_area = pygame.transform.smoothscale(b.board_surface, board_area_size)
screen.blit(board_area, board_area_position)
pygame.display.update()
wait()

b.board.print_board_with_coords()

smb.place_card(sm.PathCard(True, True, True, True, True), (3, 9))
b.update((3, 9))
board_area = pygame.transform.smoothscale(b.board_surface, board_area_size)
screen.blit(board_area, board_area_position)
pygame.display.update()
wait()

b.board.print_board_with_coords()
