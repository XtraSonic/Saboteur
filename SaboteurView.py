import pygame
from pygame.locals import *
from numpy import *
import SaboteurModel as sm

# Initialize pygame
pygame.init()


class ViewController:
    # <editor-fold desc="View constants -> file paths">
    FILE_CARD_AREA_BACKGROUND = "Resources/CardAreaBackground.png"
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

    def __init__(self, player, board):
        """

        :param player:
        :type player: sm.Player
        :param board:
        :type board: sm.Board
        """

        self.player = player

        # Set window to full screen and get screen info
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
        self.hand = HandView(player.hand, self.hand_area_size)
        self.hand_area_rect = Rect(self.hand_area_position, self.hand_area_size)

        # Player List Area
        self.names_area_percentage = array((0.15, 0.7))
        self.names_area_size = (self.screen_size * self.names_area_percentage).astype(int)
        self.names_area_position = (self.screen_size[0] - self.names_area_size[0] - 1, 0)
        self.names_area_background_image = pygame.image.load(ViewController.FILE_PLAYER_LIST_AREA_BACKGROUND)
        self.names_area_background = pygame.transform.smoothscale(self.names_area_background_image,
                                                                  self.names_area_size).convert()
        self.names_area_rect = Rect(self.names_area_position, self.names_area_size)

        # Board Area
        self.board_area_percentage = array((0.7, 1))
        self.board_area_size = (self.screen_size * self.board_area_percentage).astype(int)
        self.board_area_position = (self.hand_area_size[0], 0)
        self.board = BoardView(board, self.board_area_size)
        self.board_area_rect = Rect(self.board_area_position, self.board_area_size)

        # Deck information area
        self.deck_info_area_percentage = array((self.hand_area_percentage[0], 1 - self.hand_area_percentage[1]))
        self.deck_info_area_size = (self.screen_size * self.deck_info_area_percentage).astype(int)
        self.deck_info_area_position = (self.hand_area_position[0], self.hand_area_position[1] + self.hand_area_size[1])
        self.deck_info_area_background_image = pygame.image.load(ViewController.FILE_DECK_INFO_BACKGROUND)
        self.deck_info_area_background = pygame.transform.smoothscale(self.deck_info_area_background_image,
                                                                      self.deck_info_area_size).convert()
        self.deck_info_area_rect = Rect(self.deck_info_area_position, self.deck_info_area_size)

        # Type information area
        self.type_area_percentage = array((self.names_area_percentage[0], 1 - self.names_area_percentage[1]))
        self.type_area_size = (self.screen_size * self.type_area_percentage).astype(int)
        self.type_area_position = (self.names_area_position[0], self.names_area_position[1] + self.names_area_size[1])
        self.type_area_image_raw = CardView(player.role_card, self.type_area_size).get_face()
        self.type_area_image = pygame.transform.smoothscale(self.type_area_image_raw, self.type_area_size).convert()

        # Set up screen
        self.screen.blit(self.hand.get_surface(), self.hand_area_position)
        self.screen.blit(self.names_area_background, self.names_area_position)
        self.screen.blit(self.board.get_surface(), self.board_area_position)
        self.screen.blit(self.deck_info_area_background, self.deck_info_area_position)
        self.screen.blit(self.type_area_image, self.type_area_position)  # one time only

        pygame.display.update()
        self.selected_card = None
        """:type selected_card: CardView | None"""
        self.active_player = True  # todo set to false
        self.pressed_element = None

    def view_game_loop(self):
        while True:
            event = pygame.event.wait()
            if self.active_player:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicks = pygame.mouse.get_pressed()
                    if clicks[0]:
                        location = pygame.mouse.get_pos()
                        self.pressed_element, _ = self.get_element_at(location)
                # todo other clicks + continue with logic afetr button is released
                if event.type == pygame.MOUSEBUTTONUP:
                    clicks = pygame.mouse.get_pressed()
                    if not clicks[0]:
                        location = pygame.mouse.get_pos()
                        stub, target = self.get_element_at(location)
                        if self.pressed_element == stub:
                            # full click on one element

                            if self.selected_card is not None:
                                if target == self.deck_info_area_rect:
                                    make_discard_request(self.selected_card)  # todo
                                self.selected_card = None
                            else:
                                if target == self.hand_area_rect:
                                    self.selected_card = self.pressed_element

                        self.pressed_element = None

                    # todo remove this
                if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    self.end_view()

    def get_element_at(self, location):
        # ~spaghetti code, but i alreday put waaay too much time into this
        x, y = location
        if self.deck_info_area_rect.collidepoint(x, y):
            return False, self.deck_info_area_rect
        elif self.hand_area_rect.collidepoint(x, y):
            return self.hand.get_element_at(location), self.hand_area_rect
        elif self.board_area_rect.collidepoint(x, y):
            pass
            # todo return self.board.get_element_at(location)
        elif self.names_area_rect.collidepoint(x, y):
            return False  # todo make names great again
        return None, None

    def update_hand(self, card_viewed):
        image, location = self.hand.update(card_viewed)
        location_adjusted = (location[0] + self.hand_area_position[0],
                             location[1] + self.hand_area_position[1])

        self.screen.blit(image, location_adjusted)
        pygame.display.update()
        pass

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


def divide_tuples(dividend, divisor):
    res = ()
    for i in range(min(len(dividend), len(divisor))):
        res += (dividend[i] // divisor[i],)
    return res


#
# def wait():
#     while 1:
#         ''' Pause Until Input is Given '''
#         if event.type == pygame.KEYDOWN and event.key == K_SPACE:
#             break


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

    def __init__(self, card, card_size):
        """

        :param card:
        :param card_size:
        :type card: sm.Card
        :type card_size: ndarray of int
        """
        self.card = card
        self.card_size = card_size
        front_file, back_file = CardView.CARD_DICTIONARY.get(card.get_name())

        front_image = pygame.image.load(front_file)
        self.front_face = pygame.transform.smoothscale(front_image, self.card_size)

        back_image = pygame.image.load(back_file)
        self.back_face = pygame.transform.smoothscale(back_image, self.card_size)

    def get_face(self):
        if self.card.revealed:
            return self.front_face
        else:
            return self.back_face


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
        self.surface = pygame.Surface(self.board_card_size * self.board.cell_nr_width_height).convert()

        for x in range(len(self.gridView)):
            for y in range(len(self.gridView[x])):
                screen_location = (x * self.board_card_size[0], y * self.board_card_size[1])
                if self.board.grid[x][y].revealed:
                    self.surface.blit(self.gridView[x][y].front_face,
                                      screen_location,
                                      self.gridView[x][y].front_face.get_rect())
                else:
                    self.surface.blit(self.gridView[x][y].back_face,
                                      screen_location,
                                      self.gridView[x][y].back_face.get_rect())

    def get_surface(self):
        return pygame.transform.smoothscale(self.surface, self.area_size).convert()

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
                        self.surface.blit(self.gridView[x][y].front_face,
                                          screen_location,
                                          self.gridView[x][y].front_face.get_rect())
                    else:
                        self.surface.blit(self.gridView[x][y].back_face,
                                          screen_location,
                                          self.gridView[x][y].back_face.get_rect())
        else:
            x, y = location
            screen_location = (x * self.board_card_size[0], y * self.board_card_size[1])
            self.gridView[x][y] = CardView(self.board.grid[x][y], self.board_card_size)
            if self.board.grid[x][y].revealed:
                self.surface.blit(self.gridView[x][y].front_face,
                                  screen_location,
                                  self.gridView[x][y].front_face.get_rect())
            else:
                self.surface.blit(self.gridView[x][y].back_face,
                                  screen_location,
                                  self.gridView[x][y].back_face.get_rect())

            # todo this should not be neccessary
            # check goals
            y = self.board.left_goal_location[1]
            for x in range(sm.NUMBER_OF_GOALS):
                x = self.board.left_goal_location[0] + 2 * x
                screen_location = (x * self.board_card_size[0], y * self.board_card_size[1])
                if self.board.grid[x][y].revealed:
                    self.surface.blit(self.gridView[x][y].front_face,
                                      screen_location,
                                      self.gridView[x][y].front_face.get_rect())
                else:
                    self.surface.blit(self.gridView[x][y].back_face,
                                      screen_location,
                                      self.gridView[x][y].back_face.get_rect())


class HandView:
    SPACING = 10

    def __init__(self, cards, area_size):
        self.cards_viewed = []
        """ :type :list[CardView]"""
        self.cards = cards
        self.area_size = area_size
        self.background = pygame.image.load(ViewController.FILE_CARD_AREA_BACKGROUND)
        self.surface = pygame.transform.smoothscale(self.background, self.area_size).convert()

        self.nr_cards = len(self.cards)
        # 75% witdh wise, 1 card extra space + x pixels between them heightwise
        self.card_size = array((self.area_size[0] * 0.75,
                                self.area_size[1] // (self.nr_cards + 1) - HandView.SPACING
                                )).astype(int)
        self.cards_position_start = ((self.area_size[0] - self.card_size[0]) // 2,
                                     self.card_size[1] // 2)
        for index in range(self.nr_cards):
            self.cards_viewed.append(CardView(self.cards[index], self.card_size))
            card_image = pygame.transform.smoothscale(self.cards_viewed[index].get_face(), self.card_size)
            position = self.get_index_position(index)
            self.surface.blit(card_image, position)

    def get_index_position(self, index):
        return self.cards_position_start[0], \
               self.cards_position_start[1] + index * (self.card_size[1] + HandView.SPACING)

    def get_surface(self):
        return self.surface.convert()

    def get_element_at(self, location):
        x, y = location
        if not (self.cards_position_start[0] <= x <= self.cards_position_start[0] + self.card_size[0]):
            return False
        else:
            for index in range(self.nr_cards):
                _, top = self.get_index_position(index)
                if top <= y:
                    if y <= top + self.card_size[1]:
                        return self.cards_viewed[index]
                else:
                    return False
        return False

    def update(self, card_viewed):
        index = self.cards_viewed.index(card_viewed)
        if len(self.cards) == self.nr_cards:
            self.cards_viewed[index] = CardView(self.cards[index], self.card_size)
            location = self.get_index_position(index)
            image = self.cards_viewed[index].get_face()
            self.surface.blit(image, location)
            return image, location
        else:
            pass
            # todo reduce the nr of cards shown


########################################################################################################################
#                                                      END CODE                                                        #
########################################################################################################################
########################################################################################################################
#                                               playing/testing funcions                                               #
########################################################################################################################
#
# def play_test():
#     black = (0, 0, 0)
#     pink = (255, 132, 188)
#     blue = (0, 0, 255)
#     smb = sm.Board()
#     b = BoardView(smb, board_area_size)
#
#     screen.blit(card_area_background, hand_area_position)
#     screen.blit(names_area_background, names_area_position)
#
#     board_area = pygame.transform.smoothscale(b.surface, board_area_size)
#     screen.blit(board_area, board_area_position)
#     pygame.display.update()
#     b.board.print_board_with_coords()
#     wait()
#
#     # smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 2))
#     # smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 3))
#     # smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 4))
#     # smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 5))
#     # smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 6))
#     # smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 7))
#     # b.update((4,2))
#     # b.update((4,3))
#     # b.update((4,4))
#     # b.update((4,5))
#     # b.update((4,6))
#     # b.update((4,7))
#     # board_area = pygame.transform.smoothscale(b.surface, board_area_size)
#     # screen.blit(board_area, board_area_position)
#     # pygame.display.update()
#     # b.board.print_board_with_coords()
#     #
#     # wait()
#     # smb.place_card(sm.PathCard(True, True, True, True, True, True), (4, 8))
#     # b.update((4,8))
#     # board_area = pygame.transform.smoothscale(b.surface, board_area_size)
#     # screen.blit(board_area, board_area_position)
#     # pygame.display.update()
#     # b.board.print_board_with_coords()
#     # wait()
#
#     for i_ in range(2, 9):
#         smb.place_card(sm.PathCard(True, True, True, True, True), (4, i_))
#         b.update((4, i_))
#         board_area = pygame.transform.smoothscale(b.surface, board_area_size)
#         screen.blit(board_area, board_area_position)
#         pygame.display.update()
#         wait()
#
#     b.board.print_board_with_coords()
#
#     smb.place_card(sm.PathCard(True, True, True, True, True), (5, 9))
#     b.update((5, 9))
#     board_area = pygame.transform.smoothscale(b.surface, board_area_size)
#     screen.blit(board_area, board_area_position)
#     pygame.display.update()
#     wait()
#
#     b.board.print_board_with_coords()
#
#     smb.place_card(sm.PathCard(True, True, True, True, True), (3, 9))
#     b.update((3, 9))
#     board_area = pygame.transform.smoothscale(b.surface, board_area_size)
#     screen.blit(board_area, board_area_position)
#     pygame.display.update()
#     wait()
#
#     b.board.print_board_with_coords()

model = sm.Model(["a", "b", "c"])
view = ViewController(model.get_active_player(), model.board)


def make_discard_request(card_viewed):
    """

    :param card_viewed:
    :type card_viewed: CardView | None
    :return:
    """
    pass
    # force same turn
    model.turn_index = 0

    print("got to request")
    card = card_viewed.card
    print(model.play_turn(card, model.LOCATION_DISCARD))

    view.update_hand(card_viewed)


view.view_game_loop()
