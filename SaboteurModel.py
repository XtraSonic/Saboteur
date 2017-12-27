"""
This file includes the building blocks of the game required for the back end
Classes included:
    Card + all it`s subclasses  -> represent the real life cards
    Board                       -> contains a matrix of all the cards that would be on a real board
    Deck                        -> contains a list of cards which represents the real life deck
    Player                      -> represents the information about a real life player
    Model                       -> brings all the elements together
"""

# defaults set for possible future updates
NUMBER_OF_GOALS = 3


########################################################################################################################
#                                               Card + extensions                                                      #
########################################################################################################################


class Card:
    PLACEHOLDER = 0
    DEMOLISH = 1
    SPY = 2
    TYPE = 3
    VALID_TYPES = [PLACEHOLDER, DEMOLISH, SPY, TYPE, None]
    """
        Attributes
        ----------
        card_type:int
            is a number representing the type
        revealed:bool
            true if the card is visible
        """

    def __init__(self, card_type=None, revealed=None):
        """"
                Parameters
                ----------
                card_type:int
                    is a number representing the type, default is None
                revealed:bool
                    true if the card is visible, default is True
                """

        try:
            self.VALID_TYPES.index(card_type)
            self.card_type = card_type
        except ValueError as e:
            self.card_type = None
            print("ERROR: Invalid card type ! Value will be set to \"None\" \nMessage:", e)

        if revealed is None:
            self.revealed = True
        else:
            self.revealed = revealed

    def flip(self):
        self.revealed = not self.revealed

    def spy(self, player, goal):
        # TODO
        pass

    def demolish(self, board, location):
        # TODO
        pass


class BlockUnblockCard(Card):
    BLOCK = 4
    UNBLOCK = 5
    PICK = 10
    LAMP = 20
    CART = 30
    VALID_SUBTYPES = [None, PICK, LAMP, CART]

    def __init__(self, card_subtype, block=None, revealed=None):
        """"
                Parameters
                ----------
                card_subtype:int
                    a number representing the card subtype
                block:bool
                    true is the card is a block card, default is False => unblock card
                revealed:bool
                    true if the card is visible, default is True
                """

        super().__init__(Card.PLACEHOLDER, revealed)
        if block is None or block is False:
            self.card_type = BlockUnblockCard.UNBLOCK
        elif block:
            self.card_type = BlockUnblockCard.BLOCK
        else:
            print("ERROR: Invalid card type for Block/Unblock, type will be set to None")
            self.card_type = None

        try:
            self.card_subtype = self.VALID_SUBTYPES.index(card_subtype)
        except ValueError as e:
            self.card_subtype = None
            print("ERROR: Invalid card subtype ! Value will be set to \"None\" \nMessage:", e)

    def block(self, player):
        # TODO
        pass

    def unblock(self, player):
        # TODO
        pass


class PathCard(Card):
    PATH = 6

    def __init__(self, north, south, est, west, center, revealed=None):
        """"
                Parameters
                ----------
                north:bool or None
                    true if card has path to north, None if card is not set yet
                south:bool or None
                    true if card has path to south, None if card is not set yet
                est:bool or None
                    true if card has path to est, None if card is not set yet
                west:bool or None
                    true if card has path to west, None if card is not set yet
                center:bool or None
                    true if card is a connected road, False if it is a dead end, None if card is not set yet
                revealed:bool
                    true if the card is visible, default is True
                """
        super().__init__(Card.PLACEHOLDER, revealed)
        self.card_type = PathCard.PATH

        self.north = north
        self.south = south
        self.est = est
        self.west = west
        self.center = center

        self.end_reached = [False for _ in range(NUMBER_OF_GOALS)]

    def mark_end(self, index):
        """"
        Parameters
        ----------
        index:int
            number representing which of the goal cards was reached
        """
        self.end_reached[index] = True

    def reset_end(self, index):
        self.end_reached[index] = False

    def rotate180(self):
        self.north ^= self.south
        self.south ^= self.north
        self.north ^= self.south

        self.est ^= self.west
        self.west ^= self.est
        self.est ^= self.west

    def is_symmetric(self):
        return (self.north == self.south) and (self.est == self.west)

    def get_cardinals(self):
        cardinals = list("_____")
        if self.north:
            cardinals[0] = "N"
        if self.south:
            cardinals[1] = "S"
        if self.est:
            cardinals[2] = "E"
        if self.west:
            cardinals[3] = "W"
        if self.center:
            cardinals[4] = "C"
        return "".join(cardinals)


class GoalCard(PathCard):
    GOAL = 7

    def __init__(self, index, revealed=None):
        super().__init__(True, True, True, True, True, revealed)
        self.card_type = GoalCard.GOAL
        self.index = index
        self.end_reached[self.index] = True

    def reset_end(self, index):
        if index != self.index:
            self.end_reached[index] = False


class StartCard(PathCard):
    START = 8

    def __init__(self):
        super().__init__(True, True, True, True, True, True)
        self.card_type = StartCard.START

    def mark_end(self, index):
        # TODO
        pass


########################################################################################################################
#                                               Board Class                                                            #
########################################################################################################################


class Board:
    # Board size, number of cells: Width/Height, Width >= 5, Height >= 9
    MINIMUM_BOARD_SIZE = (5, 9)
    DEFAULT_BOARD_SIZE = (9, 11)
    #              North   South    Est     West
    NEIGHBOURS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self, board_cell_nr_width_height=None):
        if board_cell_nr_width_height is None:
            self.board_cell_nr_width_height = Board.DEFAULT_BOARD_SIZE
        else:
            self.board_cell_nr_width_height = board_cell_nr_width_height
        #                      North  South  Est    West   Center Revealed
        self.grid = [[PathCard(None, None, None, None, None, False)
                      for _ in range(max(self.board_cell_nr_width_height[1], Board.MINIMUM_BOARD_SIZE[1]))]
                     for _ in range(max(self.board_cell_nr_width_height[0], Board.MINIMUM_BOARD_SIZE[0]))]

        start_position_width = (self.board_cell_nr_width_height[0] - 1) // 2
        start_position_height = (self.board_cell_nr_width_height[1] - 9) // 2

        self.grid[start_position_width][start_position_height] = StartCard()

        left_goal_position_width = start_position_width - NUMBER_OF_GOALS + 1
        left_goal_position_height = start_position_height + 8
        for i in range(NUMBER_OF_GOALS):
            self.grid[left_goal_position_width + i * 2][left_goal_position_height] = GoalCard(i, False)

    def print_board(self):
        for j in range(self.board_cell_nr_width_height[1]):  # width
            for i in range(self.board_cell_nr_width_height[0]):  # height
                if self.grid[i][j].card_type == PathCard.PATH:
                    print(self.grid[i][j].get_cardinals(), end=" ")
                elif self.grid[i][j].card_type == GoalCard.GOAL:
                    print("_GOAL", end=" ")
                elif self.grid[i][j].card_type == StartCard.START:
                    print("START", end=" ")
                else:
                    print("_____", end=" ")
            print()

    def get_valid_moves(self, card):
        """"
                Parameters
                ----------
                card:PathCard
                    the card for which to search the valid moves
                """

        symmetric = card.is_symmetric()
        result = None
        while True:
            for i in range(self.board_cell_nr_width_height[0]):
                for j in range(self.board_cell_nr_width_height[1]):
                    if self.fits(card, i, j):
                        result.append((i, j))

            if symmetric:
                symmetric = False
            else:
                break

    def fits(self, card, x, y):
        """"
                Parameters
                ----------
                card:PathCard
                    the card for which to search the valid moves
                x:int
                    the position on the printed X axis (width related)
                y:int
                    the position on the printed Y axis (height related)
                """

        # PROBLEM: if the card next to the one we compare is a goal, you HAVE to connect it to it
        # so you can`t place a N_EWC to the north of a goal card,
        # basically, if you place a card next to a goal, you HAVE to reveal it
        # since i don`t want to make x images (where x > 0) for each case, i`ll call this a FEATURE :)
        for i in range(len(Board.NEIGHBOURS)):
            t = Board.NEIGHBOURS[i]
            pos_x = x + t[0]
            pos_y = y + t[1]
            if self.valid_location(pos_x, pos_y):
                if i == 0 and (self.grid[pos_x][pos_y].south is None or card.north != self.grid[pos_x][pos_y].south):
                    return False
                elif i == 1 and (self.grid[pos_x][pos_y].north is None or card.south != self.grid[pos_x][pos_y].north):
                    return False
                elif i == 2 and (self.grid[pos_x][pos_y].west is None or card.est != self.grid[pos_x][pos_y].west):
                    return False
                elif i == 3 and (self.grid[pos_x][pos_y].est is None or card.west != self.grid[pos_x][pos_y].est):
                    return False

        return True

    def valid_location(self, x, y):
        """"
                Parameters
                ----------
                x:int
                    the position on the printed X axis (width related)
                y:int
                    the position on the printed Y axis (height related)
                """
        return 0 <= x < self.board_cell_nr_width_height[0] and 0 <= y < self.board_cell_nr_width_height[1]


########################################################################################################################
#                                               Deck Class                                                             #
########################################################################################################################


class Deck:

    def __init__(self, deck_list=None):
        if deck_list is not None:
            self.deck_list = deck_list

    def is_empty(self):
        if len(self.deck_list.length()) == 0:
            return True
        else:
            return False

    def make_saboteur_deck(self):
        pass
        # TODO


########################################################################################################################
#                                               Player Class                                                           #
########################################################################################################################

class Player:

    def __init__(self):
        # TODO
        pass


########################################################################################################################
#                                               Model Class                                                            #
########################################################################################################################

class Model:

    def __init__(self):
        # TODO
        pass
