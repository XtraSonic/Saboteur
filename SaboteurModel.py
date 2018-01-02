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
import random

random.seed()
NUMBER_OF_GOALS = 3
KEY_WORDS = ["PLACEHOLDER",
             "DEMOLISH",
             "SPY",
             "GNOME",
             "BLOCK",
             "UNBLOCK",
             "PICK",
             "LAMP",
             "CART",
             "PATH",
             "GOAL",
             "START"
             ]


# convenience function, but numpy might be better
def add_tuples(a, b):
    c = ()
    for i in range(min(len(a), len(b))):
        c += (a[i] + b[i],)
    return c


########################################################################################################################
#                                               Card + extensions                                                      #
########################################################################################################################
class Card:
    PLACEHOLDER = KEY_WORDS.index("PLACEHOLDER")
    DEMOLISH = KEY_WORDS.index("DEMOLISH")
    SPY = KEY_WORDS.index("SPY")
    GNOME = KEY_WORDS.index("GNOME")
    VALID_TYPES = [PLACEHOLDER, DEMOLISH, SPY, GNOME, None]
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
            true if the card is visible, default is False
        """

        try:
            self.VALID_TYPES.index(card_type)
            self.card_type = card_type
        except ValueError as e:
            self.card_type = None
            print("ERROR: Invalid card type ! Value will be set to \"None\" \nMessage:", e)

        if revealed is None:
            self.revealed = False
        else:
            self.revealed = revealed

    def get_name(self):
        return KEY_WORDS[self.card_type]


class BlockUnblockCard(Card):
    BLOCK = KEY_WORDS.index("BLOCK")
    UNBLOCK = KEY_WORDS.index("UNBLOCK")
    PICK = KEY_WORDS.index("PICK")
    LAMP = KEY_WORDS.index("LAMP")
    CART = KEY_WORDS.index("CART")
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
            true if the card is visible, default is False
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
            self.symbol = self.VALID_SUBTYPES.index(card_subtype)
        except ValueError as e:
            self.symbol = None
            print("ERROR: Invalid card subtype ! Value will be set to \"None\" \nMessage:", e)

    def get_name(self):
        return KEY_WORDS[self.card_type] + "_" + KEY_WORDS[self.symbol]


class PathCard(Card):
    PATH = KEY_WORDS.index("PATH")

    PATH_CONSTRUCTOR_DICTIONARY = {
        "NSEW_": lambda x: PathCard(True, True, True, True, False, x),
        "NSEW": lambda x: PathCard(True, True, True, True, False, x),

        "NSEWC": lambda x: PathCard(True, True, True, True, True, x),

        "NSE__": lambda x: PathCard(True, True, True, False, False, x),
        "NSE": lambda x: PathCard(True, True, True, False, False, x),

        "NSE_C": lambda x: PathCard(True, True, True, False, True, x),
        "NSEC": lambda x: PathCard(True, True, True, False, True, x),

        "NS_W_": lambda x: PathCard(True, True, False, True, False, x),
        "NSW": lambda x: PathCard(True, True, False, True, False, x),

        "NS_WC": lambda x: PathCard(True, True, False, True, True, x),
        "NSWC": lambda x: PathCard(True, True, False, True, True, x),

        "NS___": lambda x: PathCard(True, True, False, False, False, x),
        "NS": lambda x: PathCard(True, True, False, False, False, x),

        "NS__C": lambda x: PathCard(True, True, False, False, True, x),
        "NSC": lambda x: PathCard(True, True, False, False, True, x),

        "N_EW_": lambda x: PathCard(True, False, True, True, False, x),
        "NEW": lambda x: PathCard(True, False, True, True, False, x),

        "N_EWC": lambda x: PathCard(True, False, True, True, True, x),
        "NEWC": lambda x: PathCard(True, False, True, True, True, x),

        "N_E__": lambda x: PathCard(True, False, True, False, False, x),
        "NE": lambda x: PathCard(True, False, True, False, False, x),

        "N_E_C": lambda x: PathCard(True, False, True, False, True, x),
        "NEC": lambda x: PathCard(True, False, True, False, True, x),

        "N__W_": lambda x: PathCard(True, False, False, True, False, x),
        "NW": lambda x: PathCard(True, False, False, True, False, x),

        "N__WC": lambda x: PathCard(True, False, False, True, True, x),
        "NWC": lambda x: PathCard(True, False, False, True, True, x),

        "N____": lambda x: PathCard(True, False, False, False, False, x),
        "N": lambda x: PathCard(True, False, False, False, False, x),

        "N___C": lambda x: PathCard(True, False, False, False, True, x),
        "NC": lambda x: PathCard(True, False, False, False, True, x),

        "_SEW_": lambda x: PathCard(False, True, True, True, False, x),
        "SEW": lambda x: PathCard(False, True, True, True, False, x),

        "_SEWC": lambda x: PathCard(False, True, True, True, True, x),
        "SEWC": lambda x: PathCard(False, True, True, True, True, x),

        "_SE__": lambda x: PathCard(False, True, True, False, False, x),
        "SE": lambda x: PathCard(False, True, True, False, False, x),

        "_SE_C": lambda x: PathCard(False, True, True, False, True, x),
        "SEC": lambda x: PathCard(False, True, True, False, True, x),

        "_S_W_": lambda x: PathCard(False, True, False, True, False, x),
        "SW": lambda x: PathCard(False, True, False, True, False, x),

        "_S_WC": lambda x: PathCard(False, True, False, True, True, x),
        "SWC": lambda x: PathCard(False, True, False, True, True, x),

        "_S___": lambda x: PathCard(False, True, False, False, False, x),
        "S": lambda x: PathCard(False, True, False, False, False, x),

        "_S__C": lambda x: PathCard(False, True, False, False, True, x),
        "SC": lambda x: PathCard(False, True, False, False, True, x),

        "__EW_": lambda x: PathCard(False, False, True, True, False, x),
        "EW": lambda x: PathCard(False, False, True, True, False, x),

        "__EWC": lambda x: PathCard(False, False, True, True, True, x),
        "EWC": lambda x: PathCard(False, False, True, True, True, x),

        "__E__": lambda x: PathCard(False, False, True, False, False, x),
        "E": lambda x: PathCard(False, False, True, False, False, x),

        "__E_C": lambda x: PathCard(False, False, True, False, True, x),
        "EC": lambda x: PathCard(False, False, True, False, True, x),

        "___W_": lambda x: PathCard(False, False, False, True, False, x),
        "W": lambda x: PathCard(False, False, False, True, False, x),

        "___WC": lambda x: PathCard(False, False, False, True, True, x),
        "WC": lambda x: PathCard(False, False, False, True, True, x),

        "_____": lambda x: PathCard(False, False, False, False, False, x),
        "": lambda x: PathCard(False, False, False, False, False, x),

        "____C": lambda x: PathCard(False, False, False, False, True, x),
        "C": lambda x: PathCard(False, False, False, False, True, x)
    }

    def __init__(self, north=None, south=None, est=None, west=None, center=None, revealed=None):
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
            true if the card is visible, default is False
        """
        super().__init__(Card.PLACEHOLDER, revealed)
        self.card_type = PathCard.PATH

        self.north = north
        self.south = south
        self.est = est
        self.west = west
        self.center = center

        self.end_reached = [False for _ in range(NUMBER_OF_GOALS)]

    def is_initialized(self):
        if self.north is None or self.south is None or self.est is None or self.west is None or self.center is None:
            return False
        return True

    def mark_end(self, index):
        """"
        Parameters
        ----------
        index:int
            number representing which of the goal cards was reached
        """
        if self.center:
            self.end_reached[index] = True

    def reset_end(self):
        for index in range(NUMBER_OF_GOALS):
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
        return self.north, self.south, self.est, self.west, self.center

    def get_name(self):
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
    GOAL = KEY_WORDS.index("GOAL")

    def __init__(self, index, gold, revealed=None):
        super().__init__(True, True, True, True, True, revealed)
        self.card_type = GoalCard.GOAL
        self.index = index
        self.end_reached[self.index] = True
        self.gold = gold

    def reset_end(self):
        for index in range(NUMBER_OF_GOALS):
            self.end_reached[index] = False
        self.end_reached[self.index] = True

    def get_name(self):
        if self.gold:
            return "GOLD"
        else:
            return "COAL"


class StartCard(PathCard):
    START = KEY_WORDS.index("START")

    def __init__(self):
        super().__init__(True, True, True, True, True, True)
        self.card_type = StartCard.START

    def get_name(self):
        return KEY_WORDS[self.card_type]


########################################################################################################################
#                                               Board Class                                                            #
########################################################################################################################
class Board:
    # Board size, number of cells: Width/Height, Width >= 5, Height >= 9
    GOAL_START_SPACE = 7
    MINIMUM_BOARD_SIZE = (NUMBER_OF_GOALS * 2 - 1, GOAL_START_SPACE + 2)
    DEFAULT_BOARD_SIZE = (NUMBER_OF_GOALS * 2 + 3, GOAL_START_SPACE + 4)

    ERROR_UNINITIALIZED = -2
    ERROR_NOT_FIT = -1

    #              North   South    Est     West
    NEIGHBOURS = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    def __init__(self, board_cell_nr_width_height=None):
        if board_cell_nr_width_height is None:
            self.cell_nr_width_height = Board.DEFAULT_BOARD_SIZE
        else:
            self.cell_nr_width_height = board_cell_nr_width_height
        #                      North  South  Est    West   Center Revealed
        self.grid = [[PathCard()
                      for _ in range(max(self.cell_nr_width_height[1], Board.MINIMUM_BOARD_SIZE[1]))]
                     for _ in range(max(self.cell_nr_width_height[0], Board.MINIMUM_BOARD_SIZE[0]))]

        # middle of the board
        start_position_width = (self.cell_nr_width_height[0] - 1) // 2

        # middle of goal and start is in center
        start_position_height = (self.cell_nr_width_height[1] - Board.GOAL_START_SPACE - 2) // 2
        self.start_location = (start_position_width, start_position_height)

        self.grid[start_position_width][start_position_height] = StartCard()
        self.placed_cards_locations_list = [(start_position_width, start_position_height)]

        left_goal_position_width = start_position_width - NUMBER_OF_GOALS + 1
        left_goal_position_height = start_position_height + Board.GOAL_START_SPACE + 1
        self.left_goal_location = (left_goal_position_width, left_goal_position_height)
        for i in range(NUMBER_OF_GOALS):
            self.grid[left_goal_position_width + i * 2][left_goal_position_height] = GoalCard(i, False, False)

    def print_board(self):
        for j in range(self.cell_nr_width_height[1]):
            for i in range(self.cell_nr_width_height[0]):
                if self.grid[i][j].card_type == PathCard.PATH:
                    print(self.grid[i][j].get_name(), end=" ")
                elif self.grid[i][j].card_type == GoalCard.GOAL:
                    print("_GOAL", end=" ")
                elif self.grid[i][j].card_type == StartCard.START:
                    print("START", end=" ")
                else:
                    print("_____", end=" ")
            print()
        print()

    def print_board_with_coords(self):
        for j in range(self.cell_nr_width_height[1]):
            for i in range(self.cell_nr_width_height[0]):
                if self.grid[i][j].card_type == PathCard.PATH:
                    if self.grid[i][j].is_initialized():
                        print(self.grid[i][j].get_name(), end=" ")
                    else:
                        print("({0},{1})".format(i, j), end=" ")
                elif self.grid[i][j].card_type == GoalCard.GOAL:
                    if self.grid[i][j].revealed:
                        print("RGOAL", end=" ")
                    else:
                        print("_GOAL", end=" ")
                elif self.grid[i][j].card_type == StartCard.START:
                    print("START", end=" ")
                else:
                    print("_____", end=" ")
            print()
        print()

    def print_board_with_ends(self):
        for j in range(self.cell_nr_width_height[1]):
            for i in range(self.cell_nr_width_height[0]):
                if self.grid[i][j].is_initialized() and (self.grid[i][j].card_type == PathCard.PATH or
                                                         self.grid[i][j].card_type == GoalCard.GOAL or
                                                         self.grid[i][j].card_type == StartCard.START):
                    for k in range(NUMBER_OF_GOALS):
                        if self.grid[i][j].end_reached[k]:
                            print(k, end="")
                        else:
                            print("*", end="")
                    print(end=" ")
                else:
                    for _ in range(NUMBER_OF_GOALS):
                        print("_", end="")
                    print(end=" ")
            print()
        print()

    def get_all_valid_moves(self, card):
        """"
        Parameters
        ----------
        card:PathCard
            the card for which to search the valid moves
        """

        result = [[], []]
        result[0] = self.get_valid_moves(card)
        if not card.is_symmetric():
            card.rotate180()
            result[1] = self.get_valid_moves(card)
            card.rotate180()
        return result

    def get_valid_moves(self, card):
        """"
        Parameters
        ----------
        card:PathCard
            the card for which to search the valid moves
        """
        if not card.is_initialized():
            return []

        result = []
        for location in self.placed_cards_locations_list:
            for offset in Board.NEIGHBOURS:
                pos = add_tuples(location, offset)
                if pos not in result and self.fits(card, pos):
                    result.append(pos)

        return result

    def fits(self, card, location):
        """"
        Parameters
        ----------
        card:PathCard
            the card for which to search the valid moves
        location:int tuple
            location[0] = the position on the printed X axis (width related)
            location[1] = the position on the printed Y axis (height related)
        """

        if self.grid[location[0]][location[1]].is_initialized():
            return False  # an initialized card already exists in the location we want to place "card"

        connected_to_road = False

        card_cardinals = card.get_cardinals()

        #       compare index 0  1  2  3
        #                  of N  S  E  W
        compare_with_index = (1, 0, 3, 2)
        #               with  S  N  W  E

        # PROBLEM: if the card next to the one we compare is a goal, you HAVE to connect it to it
        # so you can`t place a N_EWC to the north of a goal card,
        # basically, if you place a card next to a goal, you HAVE to reveal it
        # since i don`t want to make x images (where x > 0) for each case, i`ll call this a FEATURE :)
        for i in range(len(Board.NEIGHBOURS)):
            offset = Board.NEIGHBOURS[i]
            pos_x, pos_y = add_tuples(location, offset)

            # if neighbour is inside the matrix and is initialized
            if self.is_inside((pos_x, pos_y)) and self.grid[pos_x][pos_y].is_initialized():
                if card_cardinals[i] != self.grid[pos_x][pos_y].get_cardinals()[compare_with_index[i]]:
                    return False
                else:
                    if card_cardinals[i]:
                        connected_to_road = True
        return connected_to_road

    def is_inside(self, location):
        """"
        Parameters
        ----------
        location:int tuple
            location[0] = the position on the printed X axis (width related)
            location[1] = the position on the printed Y axis (height related)
        """
        return (0 <= location[0] < self.cell_nr_width_height[0] and
                0 <= location[1] < self.cell_nr_width_height[1])

    def remove_path(self, location):
        removed_card = self.grid[location[0]][location[1]]
        if removed_card.card_type == StartCard.START or \
                removed_card.card_type == GoalCard.GOAL or \
                not removed_card.is_initialized():
            return False

        self.grid[location[0]][location[1]] = PathCard()

        self.placed_cards_locations_list.remove(location)
        for offset in Board.NEIGHBOURS:
            neighbour = add_tuples(location, offset)
            self.reset_spread(neighbour)

        goal_y = self.left_goal_location[1]
        for i in range(NUMBER_OF_GOALS):
            goal_x = self.left_goal_location[0] + 2 * i
            self.spread_to_neighbours((goal_x, goal_y), self.grid[goal_x][goal_y].index)

        return True

    def spread_to_neighbours(self, location, index):
        for offset in Board.NEIGHBOURS:
            neighbour = add_tuples(location, offset)
            self.spread_mark(neighbour, index)

    def spread_mark(self, location, index):
        if not self.is_inside(location):
            return

        spread_card = self.grid[location[0]][location[1]]
        if not spread_card.is_initialized() or spread_card.end_reached[index] or not spread_card.center:
            return

        spread_card.mark_end(index)
        self.spread_to_neighbours(location, index)

        if spread_card.card_type == GoalCard.GOAL:
            self.spread_to_neighbours(location, spread_card.index)

    def reset_spread(self, location):
        if not self.is_inside(location):
            return

        reset_card = self.grid[location[0]][location[1]]
        if not reset_card.is_initialized() or (not any(reset_card.end_reached) and
                                               reset_card.card_type == PathCard.PATH):
            return

        if reset_card.card_type == GoalCard.GOAL:
            done = True
            for i in range(len(reset_card.end_reached)):
                if reset_card.end_reached[i] and i != reset_card.index:
                    done = False
                    break
            if done:
                return

        reset_card.reset_end()
        for offset in Board.NEIGHBOURS:
            neighbour = add_tuples(location, offset)
            self.reset_spread(neighbour)

    def place_card(self, card, location):
        if not card.is_initialized():
            return Board.ERROR_UNINITIALIZED

        if not self.fits(card, location):
            return Board.ERROR_NOT_FIT

        card.revealed = True
        self.grid[location[0]][location[1]] = card
        self.placed_cards_locations_list.append(location)

        for offset in Board.NEIGHBOURS:
            neighbour = add_tuples(location, offset)
            if self.is_inside(neighbour) and self.grid[neighbour[0]][neighbour[1]].is_initialized():
                for index in range(NUMBER_OF_GOALS):
                    # card doesn't have a mark that the neighbour has
                    if not card.end_reached[index] and self.grid[neighbour[0]][neighbour[1]].end_reached[index]:
                        self.spread_mark(location, index)

    def get_goal_location(self, index):
        """
        Gets the goal on the index position

        :param index: index of the goal card, counting them from left to right starting from 0
        :type index: int
        :return: the goal card on position referred by the index and the location on the board
        :rtype: tuple of int
        """
        return self.left_goal_location[0] + 2 * index, self.left_goal_location[1]


########################################################################################################################
#                                               Deck Class                                                             #
########################################################################################################################
class Deck:

    def __init__(self, deck_list=None):
        self.deck_list = []
        """ :type : list[Card]"""
        if deck_list is not None:
            self.deck_list = deck_list

    def is_empty(self):
        if len(self.deck_list) == 0:
            return True
        else:
            return False

    def make_saboteur_deck(self):
        # todo special cards
        paths = PathCard.PATH_CONSTRUCTOR_DICTIONARY

        # NSEWC
        for _ in range(5):
            self.deck_list.append(paths.get("NSEWC")(False))
        # EWC
        for _ in range(5):
            self.deck_list.append(paths.get("__EWC")(False))
        # NEWC
        for _ in range(5):
            self.deck_list.append(paths.get("N_EWC")(False))
        # SWC
        for _ in range(5):
            self.deck_list.append(paths.get("_S_WC")(False))
        # NWC
        for _ in range(5):
            self.deck_list.append(paths.get("N__WC")(False))
        # NSC
        for _ in range(5):
            self.deck_list.append(paths.get("NS__C")(False))
        # NSWC
        for _ in range(5):
            self.deck_list.append(paths.get("NS_WC")(False))

        # NSEW
        for _ in range(2):
            self.deck_list.append(paths.get("NSEW_")(False))
        # SW
        self.deck_list.append(paths.get("_S_W_")(False))
        # NW
        self.deck_list.append(paths.get("N__W_")(False))
        # EW
        self.deck_list.append(paths.get("__EW_")(False))
        # S
        self.deck_list.append(paths.get("_S___")(False))
        # E
        self.deck_list.append(paths.get("__E__")(False))
        # SEW
        self.deck_list.append(paths.get("_SEW_")(False))
        # NS
        self.deck_list.append(paths.get("NS___")(False))
        # NSE
        self.deck_list.append(paths.get("NSE__")(False))

        self.shuffle()

    def draw_card(self):
        """

        :return:
        :rtype: Card
        """
        if not self.is_empty():
            return self.deck_list.pop()
        return None

    def shuffle(self):
        random.shuffle(self.deck_list)


########################################################################################################################
#                                               Player Class                                                           #
########################################################################################################################
class Player:
    ERROR_WRONG_CARD_TYPE = -1
    ERROR_ALREADY_BLOCKED_BY_SYMBOL = -2
    ERROR_NOT_BLOCKED_BY_SYMBOL = -3
    ERROR_HAND_IS_FULL = -4
    ERROR_DECK_IS_EMPTY = -5
    ERROR_PLAYER_BLOCKED = -6
    ERROR_NOT_FIT = -7

    def __init__(self, name, saboteur, max_hand_size):
        """

        :param name:
        :param saboteur:
        :param max_hand_size:
        :type name: str
        :type saboteur: bool
        \:type max_hand_size: int
        """
        self.max_hand_size = max_hand_size

        self.name = name
        self.saboteur = saboteur
        self.hand = []
        self.blocked_by = []
        self.knows_goals = [False for _ in range(NUMBER_OF_GOALS)]
        self.role_card = Card(Card.GNOME, saboteur)

    def is_blocked(self):
        if len(self.blocked_by):
            return True
        else:
            return False

    def block(self, block_card):
        """

        :param block_card:
        :return:
        :type block_card: BlockUnblockCard
        """
        if block_card.card_type != BlockUnblockCard.BLOCK:
            return Player.ERROR_WRONG_CARD_TYPE

        if block_card.symbol in self.blocked_by:
            return Player.ERROR_ALREADY_BLOCKED_BY_SYMBOL

        self.blocked_by.append(block_card.symbol)

    def unblock(self, block_card):
        if block_card.card_type != BlockUnblockCard.UNBLOCK:
            return Player.ERROR_WRONG_CARD_TYPE

        if block_card.symbol not in self.blocked_by:
            return Player.ERROR_NOT_BLOCKED_BY_SYMBOL

        self.blocked_by.remove(block_card)

    def add_card(self, deck):
        if len(self.hand) >= self.max_hand_size:
            return Player.ERROR_HAND_IS_FULL

        card = deck.draw_card()

        if card:
            card.revealed = True
            self.hand.append(card)
        else:
            return Player.ERROR_DECK_IS_EMPTY

    def fill_hand(self, deck):
        while len(self.hand) < self.max_hand_size:
            if self.add_card(deck) == Player.ERROR_DECK_IS_EMPTY:
                return Player.ERROR_DECK_IS_EMPTY

    def replace_card(self, index, deck):
        new_card = deck.draw_card()
        if new_card:
            new_card.revealed = 1
            self.hand[index] = new_card
        else:
            self.hand.pop(index)
            return Player.ERROR_DECK_IS_EMPTY

    def is_empty_hand(self):
        if len(self.hand):
            return True
        else:
            return False


########################################################################################################################
#                                               Model Class                                                            #
########################################################################################################################
class Model:
    MIN_PLAYERS = 3
    MAX_PLAYERS = 10

    SABOTEUR_WIN = 1
    GOLD_DIGGER_WIN = 2
    LOCATION_DISCARD = "DISCARD"
    ERROR_INVALID_LOCATION = -1

    NR_PLAYERS_DICTIONARY = {
        3: ((1, 3), 6),
        4: ((1, 4), 6),
        5: ((2, 4), 6),

        6: ((2, 5), 5),
        7: ((3, 5), 5),

        8: ((3, 6), 4),
        9: ((3, 7), 4),
        10: ((4, 7), 4)
    }

    def __init__(self, player_names):

        # deck
        self.deck = Deck()
        self.deck.make_saboteur_deck()

        # players
        self.player_names = player_names
        self.nr_of_players = len(player_names)
        if not (Model.MIN_PLAYERS <= self.nr_of_players <= Model.MAX_PLAYERS):
            raise Exception("Can not create a model with " + str(self.nr_of_players) + " players")
        (self.nr_saboteurs, self.nr_gold_diggers), max_hand_size = Model.NR_PLAYERS_DICTIONARY.get(self.nr_of_players)
        player_roles = [False for _ in range(self.nr_of_players + 1)]
        for i in range(self.nr_saboteurs):
            player_roles[i] = True
        random.shuffle(player_roles)
        self.players = [Player(element[0], element[1], max_hand_size) for element in zip(player_names, player_roles)]
        for player in self.players:
            if player.fill_hand(self.deck) == Player.ERROR_DECK_IS_EMPTY:
                raise Exception("Could not fill the hands of the playeyers with the default deck")

        # board
        self.board = Board()
        self.gold_index = random.randrange(NUMBER_OF_GOALS)

        self.turn_index = 0

    def check_end_gold(self):
        start = self.board.grid[self.board.start_location[0]][self.board.start_location[1]]
        result = []
        for index in range(NUMBER_OF_GOALS):
            if start.end_reached[index]:
                location = self.board.get_goal_location(index)
                goal = self.board.grid[location[0]][location[1]]
                if not goal.revealed:
                    goal.revealed = True
                    self.board.placed_cards_locations_list.append(location)
                    result.append(index)

        if self.gold_index in result:
            return result, True
        else:
            return result, False

    def check_end_cards(self):
        if self.deck.is_empty():
            for player in self.players:
                if not player.is_empty_hand():
                    return False
            return True
        return False

    def play_turn(self, card, location):
        player = self.players[self.turn_index]
        # card = player.hand[index_hand]
        # """:type : Card | PathCard | BlockUnblockCard"""
        index_hand = player.hand.index(card)

        if location == Model.LOCATION_DISCARD:
            self.end_turn(player, index_hand)
            return

        if card.card_type == PathCard.PATH:
            place_result = self.board.place_card(card, location)
            if place_result == Board.ERROR_UNINITIALIZED:
                raise Exception("Something went terribly wrong...\n"
                                " A card in " + player.name + "s hand was uninitialized")
            elif place_result == Board.ERROR_NOT_FIT:
                return Model.ERROR_INVALID_LOCATION

            reveals, gold_digger_win = self.check_end_gold()
            if not gold_digger_win:
                if self.check_end_cards():
                    return Model.SABOTEUR_WIN
                self.end_turn(player, index_hand)
                return reveals
            gold_location = self.board.get_goal_location(self.gold_index)
            gold_goal = self.board.grid[gold_location[0]][gold_location[1]]
            gold_goal.gold = True
            return Model.GOLD_DIGGER_WIN

        elif card.card_type == Card.SPY:
            if not self.board.grid[location[0]][location[1]].card_type == KEY_WORDS.index("SPY"):
                return Model.ERROR_INVALID_LOCATION
            # todo decide how to handle spy: popup or perma reveal
            self.end_turn(player, index_hand)
            return

        elif card.card_type == KEY_WORDS.index("DEMOLISH"):
            if not self.board.remove_path(location):
                return Model.ERROR_INVALID_LOCATION
            self.end_turn(player, index_hand)
            return

        elif card.card_type == BlockUnblockCard.BLOCK:
            if location == self.turn_index or \
                    not (0 <= location < len(self.players)):
                return Model.ERROR_INVALID_LOCATION

            block_result = self.players[location].block(card)
            if block_result == Player.ERROR_WRONG_CARD_TYPE:
                raise Exception("Something went terribly wrong...\n"
                                "Block card is not of Block type ?")
            elif block_result == Player.ERROR_ALREADY_BLOCKED_BY_SYMBOL:
                return Model.ERROR_INVALID_LOCATION

            self.end_turn(player, index_hand)
            return

        elif card.card_type == BlockUnblockCard.UNBLOCK:
            if location == self.turn_index or \
                    not (0 <= location < len(self.players)):
                return Model.ERROR_INVALID_LOCATION

            block_result = self.players[location].unblock(card)
            if block_result == Player.ERROR_WRONG_CARD_TYPE:
                raise Exception("Something went terribly wrong...\n"
                                "Unlock card is not of Unlock type ?")
            elif block_result == Player.ERROR_NOT_BLOCKED_BY_SYMBOL:
                return Model.ERROR_INVALID_LOCATION

            self.end_turn(player, index_hand)
            return

        else:
            raise Exception("Something went terribly wrong...\n"
                            "WUT CARD IZ DIZ ???\n" + card.get_name())

    def end_turn(self, player, index_hand):
        player.replace_card(index_hand, self.deck)
        self.turn_index += 1
        if self.turn_index == self.nr_of_players:
            self.turn_index = 0

    def get_active_player(self):
        return self.players[self.turn_index]


########################################################################################################################
#                                                      END CODE                                                        #
########################################################################################################################
########################################################################################################################
#                                               playing/testing funcions                                               #
########################################################################################################################


def play_test():
    b = Board()
    path_dic = PathCard.PATH_CONSTRUCTOR_DICTIONARY
    while True:
        b.print_board_with_coords()
        b.print_board_with_ends()
        print("command: ")
        command = input().lower()
        if command == "e" or command == "exit":
            break
        elif command == "p" or command == "place":
            print("Place -> Card:")
            card_ = path_dic.get(input(), None)
            if card_ is None:
                print("Invalid card")
            else:
                card_ = card_(True)
                print("location (x + enter + y)")
                location_ = int(input()), int(input())
                print(b.place_card(card_, location_))
        elif command == "g" or command == "get_valid":
            print("Get -> Card:")
            card_ = path_dic.get(input(), None)
            if card_ is None:
                print("Invalid card")
            else:
                card_ = card_(True)
                print(b.get_valid_moves(card_))
        elif command == "r" or command == "remove":
            print("location (x + enter + y)")
            location_ = int(input()), int(input())
            b.remove_path(location_)
        elif command == "d" or command == "deck_play":
            deck = Deck()
            deck.make_saboteur_deck()
            for el in deck.deck_list:
                print(el.get_name(), end=" ")
            print()
            while not deck.is_empty():
                card_ = deck.draw_card()
                print(card_.get_name())
                print("location (x + enter + y)")
                location_ = int(input()), int(input())
                print(b.place_card(card_, location_))
                b.print_board_with_coords()
                b.print_board_with_ends()

        else:
            print("Invalid command")

# play_test()
