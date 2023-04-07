from __future__ import annotations
from enum import Enum
import math
from typing import Callable


def DEFAULT_COMPARATOR(card1:Card, card2:Card)->int:
    """
    Assumes Ace's are highest card, suit does not matter.
    """
    if card1.value == card2.value:
        return 0

    # translate an ace up to a higher number to make this easier.
    val1 = card1.value if card1.value > 1 else math.inf
    val2 = card2.value if card2.value > 1 else math.inf

    if val1 < val2:
        return -1
    else:
        return 1

class FaceCard(Enum):
    """
    Represents a face card value (i.e. jacks, etc).
    """
    Jack  = 11
    Queen = 12
    King  = 13

class Suit(Enum):
    """
    Represents a 'suit' in a standard deck of playing cards. Contains the four standard
    suits.
    """
    Spades   = "Spades"
    Hearts   = "Hearts"
    Diamonds = "Diamonds"
    Clubs    = "Clubs"


class Card:
    """
    Represents a card in a standard deck. A card has two important properties:
     - a value or rank
     - a suit
    Provides facilities for comparing cards as well. The default comparison assumes that an Ace is the 
    highest card, and that the suit does not matter.
    """
    valid_face_card_values = {member.value:member.name for member in FaceCard}
    def __init__(self, suit:Suit, value:int, comparator:Callable[[Card, Card], int]=DEFAULT_COMPARATOR) -> None:
        # prevent unwanted/invalid sets like suit=56.
        if type(suit) != Suit:
            raise ValueError(f"Unexpected type '{type(suit)}' for suit.")
        self.__suit = suit
        
        if value < 1 or value > FaceCard.King.value:
            raise ValueError(f"Card value '{value}' is out of range") 
        self.__value = value

        # need way to compare/rank cards. this kind of depends on the rules of the game, so, rather
        # than make assumptions about how to do it, we can have a higher level component tell us
        # how to do it.
        self._comparator = comparator

    @property
    def value(self):
        """
        Returns the numerical value of the card.
        """
        return self.__value

    @property
    def suit(self):
        """
        Returns the suit of the card.
        """
        return self.__suit

    def __hash__(self) -> int:
        """
        Returns the hash value of this card.
        """
        return hash((self.suit, self.value))

    def __eq__(self, __o:Card) -> bool:
        """
        Determines if this card is equal to another card.
        """
        return self._comparator(self, __o) == 0

    def __ne__(self, __o:Card) -> bool:
        """
        Determines if this card is not equal to another card. 
        """
        return self._comparator(self, __o) != 0

    def __lt__(self, __o:Card) -> bool:
        """
        Determines if this card is strictly less than another card.
        """
        return self._comparator(self, __o) < 0

    def __le__(self, __o:Card) -> bool:
        """
        Determines if this card is less than or equal to another card.
        """
        return self._comparator(self, __o) <= 0

    def __gt__(self, __o:Card) -> bool:
        """
        Determines if this card is strictly greater than another card.
        """
        return self._comparator(self, __o) > 0

    def __ge__(self, __o:Card) -> bool:
        """
        Determines if this card is greater than or equal to another card.
        """
        return self._comparator(self, __o) >= 0

    def __str__(self) -> str:
        """
        A string representation of a card.
        """
        # if a face card, print out something like
        # "Queen of Hearts"
        if self.isFaceCard():
            return f"{Card.valid_face_card_values[self.value]} of {self.suit.value}"
        elif self.value == 1:
            # handle case for Aces
            return f"Ace of {self.suit.value}"
        else:
            # everything else just use the number.
            return f"{self.value} of {self.suit.value}"
        
    def isFaceCard(self)->bool:
        """
        Returns true if the card is a face card, otherwise false.
        """
        return self.value in Card.valid_face_card_values




