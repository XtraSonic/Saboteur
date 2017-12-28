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
import copy

NUMBER_OF_GOALS = 3


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


class PathCard(Card):
    PATH = 6

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
        self.end_reached[index] = True

    def reset_end(self):
        for index in range(len(self.end_reached)):
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

    def get_cardinals_string(self):
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

    def reset_end(self):
        for index in range(len(self.end_reached)):
            self.end_reached[index] = False
        self.end_reached[self.index] = True


class StartCard(PathCard):
    START = 8

    def __init__(self):
        super().__init__(True, True, True, True, True, True)
        self.card_type = StartCard.START


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
            self.board_cell_nr_width_height = Board.DEFAULT_BOARD_SIZE
        else:
            self.board_cell_nr_width_height = board_cell_nr_width_height
        #                      North  South  Est    West   Center Revealed
        self.grid = [[PathCard()
                      for _ in range(max(self.board_cell_nr_width_height[1], Board.MINIMUM_BOARD_SIZE[1]))]
                     for _ in range(max(self.board_cell_nr_width_height[0], Board.MINIMUM_BOARD_SIZE[0]))]

        start_position_width = (self.board_cell_nr_width_height[0] - 1) // 2
        start_position_height = (self.board_cell_nr_width_height[1] - 9) // 2

        self.grid[start_position_width][start_position_height] = StartCard()
        self.placed_cards_locations_list = [(start_position_width, start_position_height)]

        left_goal_position_width = start_position_width - NUMBER_OF_GOALS + 1
        left_goal_position_height = start_position_height + 8
        for i in range(NUMBER_OF_GOALS):
            self.grid[left_goal_position_width + i * 2][left_goal_position_height] = GoalCard(i, False)

    def print_board(self):
        for j in range(self.board_cell_nr_width_height[1]):  # width
            for i in range(self.board_cell_nr_width_height[0]):  # height
                if self.grid[i][j].card_type == PathCard.PATH:
                    print(self.grid[i][j].get_cardinals_string(), end=" ")
                elif self.grid[i][j].card_type == GoalCard.GOAL:
                    print("_GOAL", end=" ")
                elif self.grid[i][j].card_type == StartCard.START:
                    print("START", end=" ")
                else:
                    print("_____", end=" ")
            print()

    def print_board_with_coords(self):
        for j in range(self.board_cell_nr_width_height[1]):  # width
            for i in range(self.board_cell_nr_width_height[0]):  # height
                if self.grid[i][j].card_type == PathCard.PATH:
                    if self.grid[i][j].is_initialized():
                        print(self.grid[i][j].get_cardinals_string(), end=" ")
                    else:
                        print("({0},{1})".format(i, j), end=" ")
                elif self.grid[i][j].card_type == GoalCard.GOAL:
                    print("_GOAL", end=" ")
                elif self.grid[i][j].card_type == StartCard.START:
                    print("START", end=" ")
                else:
                    print("_____", end=" ")
            print()

    def print_board_with_ends(self):
        for j in range(self.board_cell_nr_width_height[1]):  # width
            for i in range(self.board_cell_nr_width_height[0]):  # height
                if self.grid[i][j].is_initialized() and (self.grid[i][j].card_type == PathCard.PATH or
                                                         self.grid[i][j].card_type == GoalCard.GOAL):
                    if self.grid[i][j].is_initialized():
                        for k in range(len(self.grid[i][j].end_reached)):
                            if self.grid[i][j].end_reached[k]:
                                print(k, end=" ")
                            else:
                                print("_", end=" ")
                    else:
                        print("({0},{1})".format(i, j), end=" ")
                elif self.grid[i][j].card_type == StartCard.START:
                    print("START", end=" ")
                else:
                    print("_____", end=" ")
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
                """if ((i == 0 and card.north != self.grid[pos_x][pos_y].south) or  # test if it can fit (north neighbour)
                        (i == 1 and card.south != self.grid[pos_x][pos_y].north) or  # (south neighbour)
                        (i == 2 and card.est != self.grid[pos_x][pos_y].west) or  # (est neighbour)
                        (i == 3 and card.west != self.grid[pos_x][pos_y].est)):  # (west neighbour)
                    return False
                else:
                   """

        return connected_to_road

    def is_inside(self, location):
        """"
        Parameters
        ----------
        location:int tuple
            location[0] = the position on the printed X axis (width related)
            location[1] = the position on the printed Y axis (height related)
        """
        return 0 <= location[0] < self.board_cell_nr_width_height[0] and 0 <= location[1] < \
               self.board_cell_nr_width_height[1]

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

        return True

    def spread_mark(self, location, index):
        if not self.is_inside(location):
            return

        spread_card = self.grid[location[0]][location[1]]
        if not spread_card.is_initialized() or spread_card.end_reached[index]:
            return

        spread_card.mark_end(index)
        for offset in Board.NEIGHBOURS:
            neighbour = add_tuples(location, offset)
            self.spread_mark(neighbour, index)

        if spread_card.card_type == GoalCard.GOAL:
            for offset in Board.NEIGHBOURS:
                neighbour = add_tuples(location, offset)
                self.spread_mark(neighbour, spread_card.index)

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

        if reset_card.card_type == GoalCard.GOAL:
            for offset in Board.NEIGHBOURS:
                neighbour = add_tuples(location, offset)
                self.spread_mark(neighbour, reset_card.index)

    def place_card(self, card, location):
        if not card.is_initialized():
            return -2

        if not self.fits(card, location):
            return -1

        self.grid[location[0]][location[1]] = card
        self.placed_cards_locations_list.append(location)

        for offset in Board.NEIGHBOURS:
            neighbour = add_tuples(location, offset)
            if self.is_inside(neighbour) and self.grid[neighbour[0]][neighbour[1]].is_initialized():
                for index in range(len(self.grid[neighbour[0]][neighbour[1]].end_reached)):
                    if not card.end_reached[index] and self.grid[neighbour[0]][neighbour[1]].end_reached[index]:
                        self.spread_mark(location, index)
                    if card.end_reached[index] and not self.grid[neighbour[0]][neighbour[1]].end_reached[index]:
                        self.spread_mark(neighbour, index)

        # TODO
        # self.check_end()

b = Board()

# this for the extra path beneath start N S E W, if you want more cards, add them to placed_bla bla as well

# b.grid[4][2] = PathCard(True, False, True, False, True)
# b.placed_cards_locations_list.append((4, 2))

# b.remove_path((4, 2))


p = [[None for _ in range(50)] for _ in range(5)]
p[1][1] = PathCard(True, True, True, True, False)
p[2][1] = PathCard(True, False, True, True, False)
p[3][1] = PathCard(False, True, True, True, False)
p[4][1] = PathCard(False, False, True, True, False)

p[1][2] = PathCard(True, True, True, False, False)
p[2][2] = PathCard(True, False, True, False, False)
p[3][2] = PathCard(False, True, True, False, False)
p[4][2] = PathCard(False, False, True, False, False)

p[1][3] = PathCard(True, True, False, True, False)
p[2][3] = PathCard(True, False, False, True, False)
p[3][3] = PathCard(False, True, False, True, False)
p[4][3] = PathCard(False, False, False, True, False)

p[1][4] = PathCard(True, True, False, False, False)
p[2][4] = PathCard(True, False, False, False, False)
p[3][4] = PathCard(False, True, False, False, False)
p[4][4] = PathCard(False, False, False, False, False)

# for i_ in range(5):
#     for j_ in range(5):
#         if i_ != 0 and j_ != 0:
#             print(b.get_all_valid_moves(p[i_][j_]), p[i_][j_].get_cardinals_string())
NSEW = p[1][1]
b.place_card(copy.deepcopy(NSEW), (4, 2))
b.place_card(copy.deepcopy(NSEW), (4, 3))
b.place_card(copy.deepcopy(NSEW), (4, 4))
b.place_card(copy.deepcopy(NSEW), (4, 5))
b.place_card(copy.deepcopy(NSEW), (4, 6))
b.place_card(copy.deepcopy(NSEW), (4, 7))
b.place_card(copy.deepcopy(NSEW), (4, 8))
b.place_card(copy.deepcopy(NSEW), (5, 8))
b.place_card(copy.deepcopy(NSEW), (6, 8))
b.remove_path((4, 8))
b.place_card(copy.deepcopy(NSEW), (4, 8))
print()
b.print_board_with_coords()
b.print_board_with_ends()
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
