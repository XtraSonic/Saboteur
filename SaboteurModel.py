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

NUMBER_OF_GOALS = 3
KEY_WORDS = ["PLACEHOLDER",  # 0
             "DEMOLISH",  # 1
             "SPY",  # 2
             "TYPE",  # 3
             "BLOCK",  # 4
             "UNBLOCK",  # 5
             "PICK",  # 6
             "LAMP",  # 7
             "CART",  # 8
             "PATH",  # 9
             "GOAL",  # 10
             "START"  # 11
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
    TYPE = KEY_WORDS.index("TYPE")
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

    def spy(self, player, goal):
        # TODO
        pass

    def demolish(self, board, location):
        # TODO
        pass

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

    def get_name(self):
        return KEY_WORDS[self.card_type] + "_" + KEY_WORDS[self.card_subtype]


class PathCard(Card):
    PATH = KEY_WORDS.index("PATH")

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
    MINIMUM_BOARD_SIZE = (5, 9)
    DEFAULT_BOARD_SIZE = (9, 11)
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

        start_position_width = (self.cell_nr_width_height[0] - 1) // 2
        start_position_height = (self.cell_nr_width_height[1] - 9) // 2
        self.start_location = (start_position_width, start_position_height)

        self.grid[start_position_width][start_position_height] = StartCard()
        self.placed_cards_locations_list = [(start_position_width, start_position_height)]

        left_goal_position_width = start_position_width - NUMBER_OF_GOALS + 1
        left_goal_position_height = start_position_height + 8
        self.left_goal_location = (left_goal_position_width, left_goal_position_height)
        for i in range(NUMBER_OF_GOALS):
            self.grid[left_goal_position_width + i * 2][left_goal_position_height] = GoalCard(i, False, False)

        random.seed()
        index = random.randrange(NUMBER_OF_GOALS)
        (self.grid[left_goal_position_width + index * 2][left_goal_position_height]).gold = True

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
                    if self.grid[i][j].is_initialized():
                        for k in range(NUMBER_OF_GOALS):
                            if self.grid[i][j].end_reached[k]:
                                print(k, end=" ")
                            else:
                                print("_", end=" ")
                    else:
                        print("({0},{1})".format(i, j), end=" ")
                else:
                    print("_____", end=" ")
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
                removed_card.card_type == GoalCard.GOAL:
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
            return -2, False

        if not self.fits(card, location):
            return -1, False

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

        return self.check_end()

    def check_end(self):
        """

        :return: first element is a int tuple containing the indexes of the goal cards that were revealed
                 second element is a boolean signaling if the gold was found
        :rtype: tuple of int, bool
        """
        start = self.grid[self.start_location[0]][self.start_location[1]]
        result = ()
        finish = False
        for index in range(NUMBER_OF_GOALS):
            if start.end_reached[index]:
                goal, location = self.get_goal(index)
                if not goal.revealed:
                    goal.revealed = True
                    self.placed_cards_locations_list.append(location)
                    result += (index,)
                    if goal.gold:
                        finish = True
        return result, finish

    def get_goal(self, index):
        """
        Gets the goal on the index position

        :param index: index of the goal card, counting them from left to right starting from 0
        :type index: int
        :return: the gold card on position referred by the index and the location on the board
        :rtype: GoalCard, tuple of int
        """
        return (self.grid[self.left_goal_location[0] + 2 * index][self.left_goal_location[1]],
                (self.left_goal_location[0] + 2 * index, self.left_goal_location[1]))


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

    def draw(self):
        if not self.is_empty():
            return self.deck_list.pop()
        return None


########################################################################################################################
#                                               Player Class                                                           #
########################################################################################################################
class Player:

    def __init__(self, name, type):
        # TODO
        self.name = name
        self.type = type


########################################################################################################################
#                                               Model Class                                                            #
########################################################################################################################

class Model:

    def __init__(self):
        # TODO
        pass


def play_test():
    b = Board()
    """
    NSEW_ = PathCard(True,True,True,True,False)
    NSEWC = PathCard(True,True,True,True,True)
    NSE__ = PathCard(True,True,True,False,False)
    NSE_C = PathCard(True,True,True,False,True)
    NS_W_ = PathCard(True,True,False,True,False)
    NS_WC = PathCard(True,True,False,True,True)
    NS___ = PathCard(True,True,False,False,False)
    NS__C = PathCard(True,True,False,False,True)
    N_EW_ = PathCard(True,False,True,True,False)
    N_EWC = PathCard(True,False,True,True,True)
    N_E__ = PathCard(True,False,True,False,False)
    N_E_C = PathCard(True,False,True,False,True)
    N__W_ = PathCard(True,False,False,True,False)
    N__WC = PathCard(True,False,False,True,True)
    N____ = PathCard(True,False,False,False,False)
    N___C = PathCard(True,False,False,False,True)
    _SEW_ = PathCard(False,True,True,True,False)
    _SEWC = PathCard(False,True,True,True,True)
    _SE__ = PathCard(False,True,True,False,False)
    _SE_C = PathCard(False,True,True,False,True)
    _S_W_ = PathCard(False,True,False,True,False)
    _S_WC = PathCard(False,True,False,True,True)
    _S___ = PathCard(False,True,False,False,False)
    _S__C = PathCard(False,True,False,False,True)
    __EW_ = PathCard(False,False,True,True,False)
    __EWC = PathCard(False,False,True,True,True)
    __E__ = PathCard(False,False,True,False,False)
    __E_C = PathCard(False,False,True,False,True)
    ___W_ = PathCard(False,False,False,True,False)
    ___WC = PathCard(False,False,False,True,True)
    _____ = PathCard(False,False,False,False,False)
    ____C = PathCard(False,False,False,False,True)
    # for i_ in range(5):
    #     for j_ in range(5):
    #         if i_ != 0 and j_ != 0:
    #             print(b.get_all_valid_moves(p[i_][j_]), p[i_][j_].get_name())
    
    b.place_card(copy.deepcopy(NSEWC), (4, 2))
    b.place_card(copy.deepcopy(NSEWC), (4, 3))
    b.place_card(copy.deepcopy(NSEWC), (4, 4))
    b.place_card(copy.deepcopy(NSEWC), (4, 5))
    b.place_card(copy.deepcopy(NSEWC), (4, 6))
    b.place_card(copy.deepcopy(NSEWC), (4, 7))
    b.place_card(copy.deepcopy(NSEWC), (4, 8))
    b.place_card(copy.deepcopy(NSEWC), (5, 8))
    b.place_card(copy.deepcopy(NSEWC), (6, 8))
    b.remove_path((4, 8))
    #b.place_card(copy.deepcopy(NSEW_), (4, 8))
    b.place_card(copy.deepcopy(NSEWC), (5, 7))
    print()
    b.print_board_with_coords()
    b.print_board_with_ends()
    """

    path_dic = {
        "NSEW_": lambda: PathCard(True, True, True, True, False),
        "NSEW": lambda: PathCard(True, True, True, True, False),

        "NSEWC": lambda: PathCard(True, True, True, True, True),

        "NSE__": lambda: PathCard(True, True, True, False, False),
        "NSE": lambda: PathCard(True, True, True, False, False),

        "NSE_C": lambda: PathCard(True, True, True, False, True),
        "NSEC": lambda: PathCard(True, True, True, False, True),

        "NS_W_": lambda: PathCard(True, True, False, True, False),
        "NSW": lambda: PathCard(True, True, False, True, False),

        "NS_WC": lambda: PathCard(True, True, False, True, True),
        "NSWC": lambda: PathCard(True, True, False, True, True),

        "NS___": lambda: PathCard(True, True, False, False, False),
        "NS": lambda: PathCard(True, True, False, False, False),

        "NS__C": lambda: PathCard(True, True, False, False, True),
        "NSC": lambda: PathCard(True, True, False, False, True),

        "N_EW_": lambda: PathCard(True, False, True, True, False),
        "NEW": lambda: PathCard(True, False, True, True, False),

        "N_EWC": lambda: PathCard(True, False, True, True, True),
        "NEWC": lambda: PathCard(True, False, True, True, True),

        "N_E__": lambda: PathCard(True, False, True, False, False),
        "NE": lambda: PathCard(True, False, True, False, False),

        "N_E_C": lambda: PathCard(True, False, True, False, True),
        "NEC": lambda: PathCard(True, False, True, False, True),

        "N__W_": lambda: PathCard(True, False, False, True, False),
        "NW": lambda: PathCard(True, False, False, True, False),

        "N__WC": lambda: PathCard(True, False, False, True, True),
        "NWC": lambda: PathCard(True, False, False, True, True),

        "N____": lambda: PathCard(True, False, False, False, False),
        "N": lambda: PathCard(True, False, False, False, False),

        "N___C": lambda: PathCard(True, False, False, False, True),
        "NC": lambda: PathCard(True, False, False, False, True),

        "_SEW_": lambda: PathCard(False, True, True, True, False),
        "SEW": lambda: PathCard(False, True, True, True, False),

        "_SEWC": lambda: PathCard(False, True, True, True, True),
        "SEWC": lambda: PathCard(False, True, True, True, True),

        "_SE__": lambda: PathCard(False, True, True, False, False),
        "SE": lambda: PathCard(False, True, True, False, False),

        "_SE_C": lambda: PathCard(False, True, True, False, True),
        "SEC": lambda: PathCard(False, True, True, False, True),

        "_S_W_": lambda: PathCard(False, True, False, True, False),
        "SW": lambda: PathCard(False, True, False, True, False),

        "_S_WC": lambda: PathCard(False, True, False, True, True),
        "SWC": lambda: PathCard(False, True, False, True, True),

        "_S___": lambda: PathCard(False, True, False, False, False),
        "S": lambda: PathCard(False, True, False, False, False),

        "_S__C": lambda: PathCard(False, True, False, False, True),
        "SC": lambda: PathCard(False, True, False, False, True),

        "__EW_": lambda: PathCard(False, False, True, True, False),
        "EW": lambda: PathCard(False, False, True, True, False),

        "__EWC": lambda: PathCard(False, False, True, True, True),
        "EWC": lambda: PathCard(False, False, True, True, True),

        "__E__": lambda: PathCard(False, False, True, False, False),
        "E": lambda: PathCard(False, False, True, False, False),

        "__E_C": lambda: PathCard(False, False, True, False, True),
        "EC": lambda: PathCard(False, False, True, False, True),

        "___W_": lambda: PathCard(False, False, False, True, False),
        "W": lambda: PathCard(False, False, False, True, False),

        "___WC": lambda: PathCard(False, False, False, True, True),
        "WC": lambda: PathCard(False, False, False, True, True),

        "_____": lambda: PathCard(False, False, False, False, False),
        "": lambda: PathCard(False, False, False, False, False),

        "____C": lambda: PathCard(False, False, False, False, True),
        "C": lambda: PathCard(False, False, False, False, True)
    }

    b.place_card(path_dic.get("NSEWC", None)(), (4, 2))
    b.place_card(path_dic.get("NSEWC", None)(), (4, 3))
    b.place_card(path_dic.get("NSEWC", None)(), (4, 4))
    b.place_card(path_dic.get("NSEWC", None)(), (4, 5))
    b.place_card(path_dic.get("NSEWC", None)(), (4, 6))
    b.place_card(path_dic.get("NSEWC", None)(), (4, 7))
    while True:
        b.print_board_with_coords()
        print()
        b.print_board_with_ends()
        print()
        print("command: ")
        command = input().lower()
        if command == "exit":
            break
        elif command == "p" or command == "place":
            print("Place -> Card:")
            card_ = path_dic.get(input(), None)
            if card_ is None:
                print("Invalid card")
            else:
                card_ = card_()
                print("location (x + enter + y)")
                location_ = int(input()), int(input())
                print(b.place_card(card_, location_))
        elif command == "g" or command == "get_valid":
            print("Get -> Card:")
            card_ = path_dic.get(input(), None)
            if card_ is None:
                print("Invalid card")
            else:
                card_ = card_()
                print(b.get_valid_moves(card_))
        elif command == "r" or command == "remove":
            print("location (x + enter + y)")
            location_ = int(input()), int(input())
            b.remove_path(location_)
        else:
            print("Invalid command")
