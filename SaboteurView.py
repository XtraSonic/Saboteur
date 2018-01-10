import pygame
import pygame.surfarray as surfarray
from pygame.locals import *
from numpy import *
import SaboteurModel as sm

# Initialize pygame
pygame.init()
pygame.font.init()


class ViewController:
    # <editor-fold desc="View constants -> file paths">
    FILE_HAND_AREA_BACKGROUND = "Resources/CardAreaBackground.png"
    FILE_PLAYER_LIST_AREA_BACKGROUND = "Resources/PlayerListBackground.png"
    FILE_DECK_INFO_BACKGROUND = "Resources/PlayerListBackground.png "  # todo change bg

    FILE_CARD_BACK = "Resources/SpecialCards/CardBack.jpg"

    FILE_PATH_CARD_NSEW__FRONT = "Resources/PathCards/NSEW.jpg"
    FILE_PATH_CARD_NSEWC_FRONT = "Resources/PathCards/NSEWC.jpg"
    FILE_PATH_CARD_NSE___FRONT = "Resources/PathCards/NSE.jpg"
    FILE_PATH_CARD_NSE_C_FRONT = "Resources/PathCards/NSEC.jpg"
    FILE_PATH_CARD_NS_W__FRONT = "Resources/PathCards/NSW.jpg"
    FILE_PATH_CARD_NS_WC_FRONT = "Resources/PathCards/NSWC.jpg"
    FILE_PATH_CARD_NS____FRONT = "Resources/PathCards/NS.jpg"
    FILE_PATH_CARD_NS__C_FRONT = "Resources/PathCards/NSC.jpg"
    FILE_PATH_CARD_N_EW__FRONT = "Resources/PathCards/NEW.jpg"
    FILE_PATH_CARD_N_EWC_FRONT = "Resources/PathCards/NEWC.jpg"
    FILE_PATH_CARD_N_E___FRONT = "Resources/PathCards/NE.jpg"
    FILE_PATH_CARD_N_E_C_FRONT = "Resources/PathCards/NEC.jpg"
    FILE_PATH_CARD_N__W__FRONT = "Resources/PathCards/NW.jpg"
    FILE_PATH_CARD_N__WC_FRONT = "Resources/PathCards/NWC.jpg"
    FILE_PATH_CARD_N_____FRONT = "Resources/PathCards/N.jpg"
    FILE_PATH_CARD_N___C_FRONT = "Resources/PathCards/NC.jpg"
    FILE_PATH_CARD__SEW__FRONT = "Resources/PathCards/SEW.jpg"
    FILE_PATH_CARD__SEWC_FRONT = "Resources/PathCards/SEWC.jpg"
    FILE_PATH_CARD__SE___FRONT = "Resources/PathCards/SE.jpg"
    FILE_PATH_CARD__SE_C_FRONT = "Resources/PathCards/SEC.jpg"
    FILE_PATH_CARD__S_W__FRONT = "Resources/PathCards/SW.jpg"
    FILE_PATH_CARD__S_WC_FRONT = "Resources/PathCards/SWC.jpg"
    FILE_PATH_CARD__S____FRONT = "Resources/PathCards/S.jpg"
    FILE_PATH_CARD__S__C_FRONT = "Resources/PathCards/SC.jpg"
    FILE_PATH_CARD___EW__FRONT = "Resources/PathCards/EW.jpg"
    FILE_PATH_CARD___EWC_FRONT = "Resources/PathCards/EWC.jpg"
    FILE_PATH_CARD___E___FRONT = "Resources/PathCards/E.jpg"
    FILE_PATH_CARD___E_C_FRONT = "Resources/PathCards/EC.jpg"
    FILE_PATH_CARD____W__FRONT = "Resources/PathCards/W.jpg"
    FILE_PATH_CARD____WC_FRONT = "Resources/PathCards/WC.jpg"

    FILE_DEMOLISH_CARD_FRONT = "Resources/SpecialCards/Demolish.jpg"
    FILE_SPY_CARD_FRONT = "Resources/SpecialCards/Spy.jpg"

    FILE_BLOCK_PICK_CARD_FRONT = "Resources/SpecialCards/BlockPick.jpg"
    FILE_UNBLOCK_PICK_CARD_FRONT = "Resources/SpecialCards/UnblockPick.jpg"

    FILE_BLOCK_LAMP_CARD_FRONT = "Resources/SpecialCards/BlockLamp.jpg"
    FILE_UNBLOCK_LAMP_CARD_FRONT = "Resources/SpecialCards/UnblockLamp.jpg"

    FILE_BLOCK_CART_CARD_FRONT = "Resources/SpecialCards/BlockCart.jpg"
    FILE_UNBLOCK_CART_CARD_FRONT = "Resources/SpecialCards/UnblockCart.jpg"

    FILE_GOLD_DIGGER_FRONT = "Resources/SpecialCards/GoldDigger.jpg"
    FILE_SABOTEUR_FRONT = "Resources/SpecialCards/Saboteur.jpg"

    FILE_START_FRONT = "Resources/SpecialCards/StartCard.jpg"
    FILE_GOLD_CARD_FRONT = "Resources/SpecialCards/Gold.jpg"
    FILE_COAL_CARD_FRONT = "Resources/SpecialCards/Coal.jpg"
    FILE_GOAL_CARD_BACK = "Resources/SpecialCards/GoalBack.jpg"

    # </editor-fold>

    def __init__(self, player, board, names_list):
        """

        :param player:
        :type player: sm.Player
        :param board:
        :type board: sm.Board
        """

        self.player = player
        self.names_list = names_list

        # Set window to full screen and get screen info
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        assert isinstance(self.screen, pygame.Surface)
        self.screen_size = self.screen.get_size()

        # Game clock rename (used to set up frames per second)
        self.clock = pygame.time.Clock()

        # Set window title
        pygame.display.set_caption("Saboteur")

        # Set window area sizes based on screen size
        # Card Area
        self.hand_area_percentage = array((0.15, 0.7))
        self.hand_area_size = (self.screen_size * self.hand_area_percentage).astype(int)
        self.hand_area_position = 0, 0
        self.hand_area_rect = Rect(self.hand_area_position, self.hand_area_size)
        self.hand = HandView(player.hand,
                             self.hand_area_size,
                             self.screen.subsurface(self.hand_area_rect))

        # Player List Area
        self.names_area_percentage = array((0.15, 0.7))
        self.names_area_size = (self.screen_size * self.names_area_percentage).astype(int)
        self.names_area_position = (self.screen_size[0] - self.names_area_size[0] - 1, 0)
        self.names_area_rect = Rect(self.names_area_position, self.names_area_size)
        self.names = NamesView(self.names_list, self.names_area_size, self.screen.subsurface(self.names_area_rect))

        # Board Area
        self.board_area_percentage = array((0.7, 1))
        self.board_area_size = (self.screen_size * self.board_area_percentage).astype(int)
        self.board_area_position = (self.hand_area_size[0], 0)
        self.board_area_rect = Rect(self.board_area_position, self.board_area_size)
        self.board = BoardView(board, self.board_area_size, self.screen.subsurface(self.board_area_rect))

        # Deck information area
        self.deck_info_area_percentage = array((self.hand_area_percentage[0], 1 - self.hand_area_percentage[1]))
        self.deck_info_area_size = (self.screen_size * self.deck_info_area_percentage).astype(int)
        self.deck_info_area_position = (self.hand_area_position[0], self.hand_area_position[1] + self.hand_area_size[1])
        self.deck_info_area_background_image = pygame.image.load(ViewController.FILE_DECK_INFO_BACKGROUND)
        self.deck_info_area_background = pygame.transform.smoothscale(self.deck_info_area_background_image,
                                                                      self.deck_info_area_size).convert()

        self.deck_info_area_rect = Rect(self.deck_info_area_position, self.deck_info_area_size)
        self.screen.blit(self.deck_info_area_background, self.deck_info_area_position)

        # Type information area
        self.type_area_percentage = array((self.names_area_percentage[0], 1 - self.names_area_percentage[1]))
        self.type_area_size = (self.screen_size * self.type_area_percentage).astype(int)
        self.type_area_position = (self.names_area_position[0], self.names_area_position[1] + self.names_area_size[1])
        self.type_area_rect = Rect(self.type_area_position, self.type_area_size)
        self.type_area_card = CardView(player.role_card,
                                       self.type_area_size,
                                       self.screen.subsurface(self.type_area_rect))

        pygame.display.update()
        self.selected_card = None
        """:type selected_card: CardView | None"""
        self.active_player = True  # todo set to false
        self.pressed_element = None
        self.prepare_rotate = False

    def view_game_loop(self):
        while True:
            event = pygame.event.wait()
            if self.active_player:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicks = pygame.mouse.get_pressed()

                    if clicks[0]:
                        location = pygame.mouse.get_pos()
                        self.pressed_element, _ = self.get_element_at(location)
                        if self.pressed_element is None:
                            self.deselect()

                    if clicks[2]:
                        self.prepare_rotate = True

                if event.type == pygame.MOUSEBUTTONUP:
                    clicks = pygame.mouse.get_pressed()

                    if not clicks[0]:
                        location = pygame.mouse.get_pos()
                        released_element, region = self.get_element_at(location)

                        if released_element is not None and self.pressed_element == released_element:

                            # full click on one element

                            if self.selected_card is None:
                                if region == self.hand_area_rect:
                                    self.select(self.pressed_element)
                            else:
                                if region == self.deck_info_area_rect:  # discard card
                                    end = make_discard_request(self.selected_card)  # todo
                                    if end is not None:
                                        self.end_screen(end)

                                if region == self.board_area_rect:
                                    end = make_play_path_request(self.selected_card, self.pressed_element)  # todo
                                    if end:
                                        self.end_screen(end)
                                self.deselect()
                        self.pressed_element = None

                    if not clicks[2]:
                        if self.prepare_rotate:
                            if self.selected_card:
                                make_rotate_request(self.selected_card)
                                self.select(self.selected_card)
                            self.prepare_rotate = False

                    # todo remove this
                if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    self.end_view()
                pygame.display.update()

    def end_screen(self, winner):

        # Winner type
        font = pygame.font.SysFont("comicsansms", 60)
        if winner == sm.Model.SABOTEUR_WIN:
            winner_color = NamesView.RED
            winner_message = font.render("SABOTEURS WIN", True, winner_color, NamesView.BLACK)
        else:
            winner_color = NamesView.GREEN
            winner_message = font.render("GOLD DIGGERS WIN", True, winner_color, NamesView.BLACK)
        message_rect = winner_message.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 14))
        self.screen.blit(winner_message, message_rect)

        # actual Winners
        font = pygame.font.SysFont("comicsansms", 40)
        winner_list = request_winner_list()
        for index in range(len(winner_list)):
            player_name = winner_list[index]
            name_rendered = font.render(player_name, True, winner_color, NamesView.BLACK)
            name_rect = name_rendered.get_rect(center=(self.screen_size[0] // 2,
                                                       (self.screen_size[1] // 14) * (index + 3)))
            self.screen.blit(name_rendered, name_rect)

    def select(self, element):
        """

        :param element:
        :type element:
        :return:
        """
        self.selected_card = element
        self.selected_card.shade()
        return

    def deselect(self):
        if self.selected_card is None:
            return
        self.selected_card.redraw()
        self.selected_card = None

    def get_element_at(self, location):
        """

        :param location:
        :return:
        :rtype : CardView, Rect
        """
        x, y = location
        if self.deck_info_area_rect.collidepoint(x, y):
            return False, self.deck_info_area_rect  # False aka no card

        elif self.hand_area_rect.collidepoint(x, y):
            return self.hand.get_element_at(location), self.hand_area_rect

        elif self.board_area_rect.collidepoint(x, y):
            return self.board.get_element_at(location), self.board_area_rect

        elif self.names_area_rect.collidepoint(x, y):
            return None, None  # todo make names great again

        return None, None

    def update_hand(self, card_viewed):
        self.hand.update(card_viewed)
        # pygame.display.update()  # todo update only a rect, but it`s too bothersome (considering time left)
        pass

    def update_board(self, locations=None):
        self.board.update(locations)

    @staticmethod
    def end_view():
        pygame.quit()
        exit()


# # Function to convert tuples into integer tuples
# def convert_to_int_tuple(x):
#     res = ()
#     for element in x:
#         res += (int(element),)
#     return res
#
#
# def divide_tuples(dividend, divisor):
#     res = ()
#     for i in range(min(len(dividend), len(divisor))):
#         res += (dividend[i] // divisor[i],)
#     return res
#

def wait():
    while 1:
        event = pygame.event.wait()
        ''' Pause Until Input is Given '''
        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
            break


########################################################################################################################
#                                               NamesView Class                                                        #
########################################################################################################################
class NamesView:
    SPACING = 55
    FONT_SIZE = 35

    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)

    def __init__(self, names, area_size, subsurface):
        self.area_size = area_size
        self.center_x = self.area_size[0] // 2
        self.names = names
        self.nr_names = len(self.names)
        self.surface = subsurface
        assert isinstance(self.surface, pygame.Surface)

        self.background_image = pygame.image.load(ViewController.FILE_PLAYER_LIST_AREA_BACKGROUND)
        self.background = pygame.transform.smoothscale(self.background_image, self.area_size).convert()
        self.surface.blit(self.background, (0, 0))

        self.names_rendered = []
        self.font = pygame.font.SysFont("comicsansms", NamesView.FONT_SIZE)
        for index in range(self.nr_names):
            # todo name background rep if it is your turn or not (red = not, green = that players turn)
            # todo name color = blocked by symbol and we will assign colors for symbols
            name_rendered = self.font.render(self.names[index], True, NamesView.BLACK, NamesView.RED)
            self.names_rendered.append(name_rendered)
            name_rect = name_rendered.get_rect(center=(self.center_x, (index + 2) * NamesView.SPACING))
            self.surface.blit(name_rendered, name_rect)


########################################################################################################################
#                                               CardView Class                                                         #
########################################################################################################################
class CardView:
    CARD_DICTIONARY = {
        "DEMOLISH": (ViewController.FILE_DEMOLISH_CARD_FRONT, ViewController.FILE_CARD_BACK),
        "SPY": (ViewController.FILE_SPY_CARD_FRONT, ViewController.FILE_CARD_BACK),

        "BLOCK_PICK": (ViewController.FILE_BLOCK_PICK_CARD_FRONT, ViewController.FILE_CARD_BACK),
        "UNBLOCK_PICK": (ViewController.FILE_UNBLOCK_PICK_CARD_FRONT, ViewController.FILE_CARD_BACK),

        "BLOCK_LAMP": (ViewController.FILE_BLOCK_LAMP_CARD_FRONT, ViewController.FILE_CARD_BACK),
        "UNBLOCK_LAMP": (ViewController.FILE_UNBLOCK_LAMP_CARD_FRONT, ViewController.FILE_CARD_BACK),

        "BLOCK_CART": (ViewController.FILE_BLOCK_CART_CARD_FRONT, ViewController.FILE_CARD_BACK),
        "UNBLOCK_CART": (ViewController.FILE_UNBLOCK_CART_CARD_FRONT, ViewController.FILE_CARD_BACK),

        "NSEW_": (ViewController.FILE_PATH_CARD_NSEW__FRONT, ViewController.FILE_CARD_BACK),
        "NSEWC": (ViewController.FILE_PATH_CARD_NSEWC_FRONT, ViewController.FILE_CARD_BACK),
        "NSE__": (ViewController.FILE_PATH_CARD_NSE___FRONT, ViewController.FILE_CARD_BACK),
        "NSE_C": (ViewController.FILE_PATH_CARD_NSE_C_FRONT, ViewController.FILE_CARD_BACK),
        "NS_W_": (ViewController.FILE_PATH_CARD_NS_W__FRONT, ViewController.FILE_CARD_BACK),
        "NS_WC": (ViewController.FILE_PATH_CARD_NS_WC_FRONT, ViewController.FILE_CARD_BACK),
        "NS___": (ViewController.FILE_PATH_CARD_NS____FRONT, ViewController.FILE_CARD_BACK),
        "NS__C": (ViewController.FILE_PATH_CARD_NS__C_FRONT, ViewController.FILE_CARD_BACK),
        "N_EW_": (ViewController.FILE_PATH_CARD_N_EW__FRONT, ViewController.FILE_CARD_BACK),
        "N_EWC": (ViewController.FILE_PATH_CARD_N_EWC_FRONT, ViewController.FILE_CARD_BACK),
        "N_E__": (ViewController.FILE_PATH_CARD_N_E___FRONT, ViewController.FILE_CARD_BACK),
        "N_E_C": (ViewController.FILE_PATH_CARD_N_E_C_FRONT, ViewController.FILE_CARD_BACK),
        "N__W_": (ViewController.FILE_PATH_CARD_N__W__FRONT, ViewController.FILE_CARD_BACK),
        "N__WC": (ViewController.FILE_PATH_CARD_N__WC_FRONT, ViewController.FILE_CARD_BACK),
        "N____": (ViewController.FILE_PATH_CARD_N_____FRONT, ViewController.FILE_CARD_BACK),
        "N___C": (ViewController.FILE_PATH_CARD_N___C_FRONT, ViewController.FILE_CARD_BACK),
        "_SEW_": (ViewController.FILE_PATH_CARD__SEW__FRONT, ViewController.FILE_CARD_BACK),
        "_SEWC": (ViewController.FILE_PATH_CARD__SEWC_FRONT, ViewController.FILE_CARD_BACK),
        "_SE__": (ViewController.FILE_PATH_CARD__SE___FRONT, ViewController.FILE_CARD_BACK),
        "_SE_C": (ViewController.FILE_PATH_CARD__SE_C_FRONT, ViewController.FILE_CARD_BACK),
        "_S_W_": (ViewController.FILE_PATH_CARD__S_W__FRONT, ViewController.FILE_CARD_BACK),
        "_S_WC": (ViewController.FILE_PATH_CARD__S_WC_FRONT, ViewController.FILE_CARD_BACK),
        "_S___": (ViewController.FILE_PATH_CARD__S____FRONT, ViewController.FILE_CARD_BACK),
        "_S__C": (ViewController.FILE_PATH_CARD__S__C_FRONT, ViewController.FILE_CARD_BACK),
        "__EW_": (ViewController.FILE_PATH_CARD___EW__FRONT, ViewController.FILE_CARD_BACK),
        "__EWC": (ViewController.FILE_PATH_CARD___EWC_FRONT, ViewController.FILE_CARD_BACK),
        "__E__": (ViewController.FILE_PATH_CARD___E___FRONT, ViewController.FILE_CARD_BACK),
        "__E_C": (ViewController.FILE_PATH_CARD___E_C_FRONT, ViewController.FILE_CARD_BACK),
        "___W_": (ViewController.FILE_PATH_CARD____W__FRONT, ViewController.FILE_CARD_BACK),
        "___WC": (ViewController.FILE_PATH_CARD____WC_FRONT, ViewController.FILE_CARD_BACK),
        "____C": (ViewController.FILE_CARD_BACK, ViewController.FILE_CARD_BACK),
        "_____": (ViewController.FILE_CARD_BACK, ViewController.FILE_CARD_BACK),

        "START": (ViewController.FILE_START_FRONT, ViewController.FILE_START_FRONT),
        "GOLD": (ViewController.FILE_GOLD_CARD_FRONT, ViewController.FILE_GOAL_CARD_BACK),
        "COAL": (ViewController.FILE_COAL_CARD_FRONT, ViewController.FILE_GOAL_CARD_BACK),

        "GNOME": (ViewController.FILE_SABOTEUR_FRONT, ViewController.FILE_GOLD_DIGGER_FRONT)
    }
    SHADE_FACTOR = 0.8

    def __init__(self, card, card_size, subsurface):
        """

        :param card:
        :param card_size:
        :type card: sm.Card
        :type card_size: ndarray of int
        """
        self.card = card
        self.card_size = card_size
        self.surface = subsurface
        assert isinstance(self.surface, pygame.Surface)
        self.front_face = None
        self.back_face = None
        self.active = True
        self.change_card(card)

    def get_face(self):
        if self.card.revealed:
            return self.front_face
        else:
            return self.back_face

    def change_card(self, card):
        self.card = card
        front_file, back_file = CardView.CARD_DICTIONARY.get(card.get_name())

        front_image = pygame.image.load(front_file)
        self.front_face = pygame.transform.smoothscale(front_image, self.card_size)

        back_image = pygame.image.load(back_file)
        self.back_face = pygame.transform.smoothscale(back_image, self.card_size)
        self.redraw()

    def redraw(self):
        if self.active:
            self.surface.blit(self.get_face(), (0, 0))

    def shade(self):
        if self.active:
            rgb_array = surfarray.pixels3d(self.get_face())
            surfarray.blit_array(self.surface, rgb_array * CardView.SHADE_FACTOR)


########################################################################################################################
#                                               BoardView Class                                                        #
########################################################################################################################
class BoardView:

    # noinspection PyArgumentList
    def __init__(self, board, area_size, subsurface):
        """

        :param board:
        :param area_size:
        :type board: sm.Board
        :type area_size: ndarray of int
        :type subsurface: pygame.Surface
        """
        self.board = board
        self.area_size = area_size
        self.board_card_size = area_size // array(self.board.cell_nr_width_height)

        self.grid_view = [[None
                           for _ in range(len(self.board.grid[i]))]
                          for i in range(len(self.board.grid))]
        """:type gridView: list[list[CardView]]"""

        assert isinstance(subsurface, pygame.Surface)
        self.surface = subsurface

        for i in range(len(self.grid_view)):
            for j in range(len(self.grid_view[i])):
                card_subsurface = self.surface.subsurface(Rect(self.get_card_location(i, j), self.board_card_size))
                self.grid_view[i][j] = CardView(self.board.grid[i][j], self.board_card_size, card_subsurface)

    def get_card_position(self, card):
        for i in range(len(self.grid_view)):
            for j in range(len(self.grid_view[i])):
                if self.grid_view[i][j] == card:
                    return i, j

    def get_card_location(self, i, j):
        return i * self.board_card_size[0], j * self.board_card_size[1]

    def get_element_at(self, location):
        adjusted_location = array(location) - array(self.surface.get_abs_offset())
        i, j = adjusted_location // array(self.board_card_size)
        return i, j

    def update(self, positions=None):
        """

        :param positions:
        :return:
        :type positions: list[tuple of int]
        """

        if positions is None:
            for x in range(len(self.grid_view)):
                for y in range(len(self.grid_view[x])):
                    self.grid_view[x][y].change_card(self.board.grid[x][y])
        else:
            for x, y in positions:
                self.grid_view[x][y].change_card(self.board.grid[x][y])


class HandView:
    SPACING = 10

    def __init__(self, cards, area_size, subsurface):
        self.cards_viewed = []
        """ :type cards_viewed:list[CardView]"""

        self.surface = subsurface
        assert isinstance(self.surface, pygame.Surface)

        self.cards = cards
        self.area_size = area_size
        self.background_image = pygame.image.load(ViewController.FILE_HAND_AREA_BACKGROUND)
        self.background = pygame.transform.smoothscale(self.background_image, self.area_size)
        self.surface.blit(self.background, (0, 0))

        self.nr_cards = len(self.cards)
        # 75% witdh wise, 1 card extra space + x pixels between them heightwise
        self.card_size = array((self.area_size[0] * 0.75,
                                self.area_size[1] // (self.nr_cards + 1) - HandView.SPACING
                                )).astype(int)
        self.cards_location_start = ((self.area_size[0] - self.card_size[0]) // 2,
                                     self.card_size[1] // 2)
        for index in range(self.nr_cards):
            card_surface = self.surface.subsurface(Rect(self.get_index_location(index), self.card_size))
            self.cards_viewed.append(CardView(self.cards[index], self.card_size, card_surface))

    def get_index_location(self, index):
        return self.cards_location_start[0], \
               self.cards_location_start[1] + index * (self.card_size[1] + HandView.SPACING)

    def get_element_at(self, location):
        x, y = array(location) - array(self.surface.get_abs_offset())
        if not (self.cards_location_start[0] <= x <= self.cards_location_start[0] + self.card_size[0]):
            return None
        else:
            for index in range(self.nr_cards):
                _, top = self.get_index_location(index)
                if y >= top:
                    if y <= top + self.card_size[1]:
                        return self.cards_viewed[index]
                else:
                    return None
        return None

    def update(self, card_viewed):
        index = self.cards_viewed.index(card_viewed)
        if len(self.cards) == self.nr_cards:
            self.cards_viewed[index].change_card(self.cards[index])
            return
        else:
            card_viewed.active = False
            self.surface.blit(self.background, (0, 0))
            self.nr_cards = len(self.cards)
            for index in range(self.nr_cards):
                if self.cards[index] == self.cards_viewed[index].card:
                    self.cards_viewed[index].redraw()
                else:
                    card_surface = self.surface.subsurface(Rect(self.get_index_location(index), self.card_size))
                    self.cards_viewed[index] = (CardView(self.cards[index], self.card_size, card_surface))
            self.cards_viewed.pop()
            # pygame.display.update()


########################################################################################################################
#                                                      END CODE                                                        #
########################################################################################################################
########################################################################################################################
#                                               playing/testing funcions                                               #
########################################################################################################################


model = sm.Model(["Ana", "Baciu", "Claudiu", "Dani", "Elena", "Fabian", "Gheorghe", "Horea", "Iulia", "Julieta"])
#model = sm.Model(["Ana", "Baciu", "Claudiu"])
for player in model.players:
    player.hand = []

model.players[0].fill_hand(model.deck)

view = ViewController(model.get_active_player(), model.board, model.player_names)


def make_discard_request(card_viewed):
    """

    :param card_viewed:
    :type card_viewed: CardView
    :return:
    """

    # todo delete
    #  force same turn
    model.turn_index = 0

    print("got to request discard")
    card = card_viewed.card
    end = model.play_turn(card, model.LOCATION_DISCARD)
    print(end)

    view.update_hand(card_viewed)
    return end


def make_play_path_request(card_viewed, location):
    """

    :param location:
    :type location: tuple of int
    :param card_viewed:
    :type card_viewed: CardView
    :return:
    """

    # force same turn
    model.turn_index = 0

    print("got to request play path, glod @", model.gold_index)

    card = card_viewed.card
    print(location)
    res, win = model.play_turn(card, location)
    print(res)
    model.board.print_board_with_coords()
    model.board.print_board_with_ends()
    if res != model.ERROR_INVALID_LOCATION:
        positions = [location]
        view.update_board(positions + res)
    if win is not None:
        if win == model.SABOTEUR_WIN:
            print("SABOTEURS WIN")
        else:
            print("GD WIN")
    view.update_hand(card_viewed)

    return win


def make_rotate_request(card_viewed):
    """

    :param card_viewed:
    :type card_viewed: CardView
    :return:
    """

    print("Got to rotate request")

    card = card_viewed.card
    model.rotate_card(card)
    view.update_hand(card_viewed)


def request_winner_list():
    if model.game_ended == model.SABOTEUR_WIN:
        winners = True
    elif model.game_ended == model.GOLD_DIGGER_WIN:
        winners = False
    else:
        return

    winner_list = []
    for player in model.players:
        if player.saboteur == winners:
            winner_list.append(player.name)
    return winner_list


view.view_game_loop()

wait()
