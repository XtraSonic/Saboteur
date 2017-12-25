"""
This file includes the building blocks of the game required for the back end
Classes included:
    Card + all it`s subclasses  -> represents the real life cards
    Board                       -> contains a matrix of all the cards that would be on a real board
    Deck                        -> contains a list of cards which represents the real life deck
    Player                      -> represents the information about a real life player
    Model                       -> brings all the elements together
"""

import numpy


#####################################################################################################
#                                               Cards + extensions                                  #
#####################################################################################################


class Card:
    VALID_TYPES = [None, "block", "unblock", "demolish", "type", "spy", "path", "goal"]
    VALID_SUBTYPES = [None, "pick", "lamp", "cart"]

    def __init__(self, revealed=None, card_type=None, card_subtype=None):

        try:
            self.card_type = self.VALID_TYPES.index(card_type)
        except ValueError as e:
            self.card_subtype = None
            print("ERROR: Invalid card type ! Value will be set to \"None\" \nMessage:", e)

        try:
            self.card_subtype = self.VALID_SUBTYPES.index(card_subtype)
        except ValueError as e:
            self.card_subtype = None
            print("ERROR: Invalid card subtype ! Value will be set to \"None\" \nMessage:", e)

        if revealed is None:
            self.revealed = True
        else:
            self.revealed = revealed

    def flip(self):
        self.revealed = not self.revealed

    def block(self, player):
        # TODO
        pass

    def unblock(self, player):
        # TODO
        pass

    def spy(self, player, goal):
        # TODO
        pass

    def demolish(self, board, location):
        # TODO
        pass


#####################################################################################################
#                                               Board Class                                         #
#####################################################################################################


class Board:

    def __init__(self, board_cell_nr_width_height=None):
        # Board size, number of cells: Width/Height, Width >= 5, Height >= 9
        self.MINIMUM_BOARD_SIZE = numpy.array(5, 9)
        self.DEFAULT_BOARD_SIZE = numpy.array((9, 11))
        if board_cell_nr_width_height is None:
            self.board_cell_nr_width_height = self.DEFAULT_BOARD_SIZE
        else:
            self.board_cell_nr_width_height = board_cell_nr_width_height
        # TODO change the cards to path cards
        self.grid = [[Card()
                      for x in range(max(self.board_cell_nr_width_height[0], 9))]
                     for y in range(max(self.board_cell_nr_width_height[1], 5))]


#####################################################################################################
#                                               Deck Class                                          #
#####################################################################################################

class Deck:

    def __init__(self):
        # TODO
        pass


#####################################################################################################
#                                               Player Class                                        #
#####################################################################################################

class Player:

    def __init__(self):
        # TODO
        pass


#####################################################################################################
#                                               Model Class                                         #
#####################################################################################################

class Model:

    def __init__(self):
        # TODO
        pass
