from typing import Callable, List
from .Card import Card, Suit, FaceCard, DEFAULT_COMPARATOR
from random import shuffle

class Deck:
    """
    Class to represent a standard deck of cards, which consists of four suits
    of 13 cards each, 52 in total. Provides operations to draw/deal cards out
    plus shuffle. 

    When instantiating a deck of cards, the caller may also indicate how to compare cards to each
    other utilizing a comparator function.  If not specified, a default comparator is used and
    the following is assumed:
        - an Ace outranks all other cards
        - the suit of the card doesn't matter. That is, a 'Queen of Hearts' is equal 
        to a 'Queen of Spades'
    """
    def __init__(self, comparator:Callable[[Card, Card], int]=DEFAULT_COMPARATOR) -> None:
        self._deck:List[Card] = []
        # for each suit of card
        for suit in Suit:
            # we need to create 13 cards
            for card_value in range(1, FaceCard.King.value + 1):
                self._deck.append(Card(suit=suit, value=card_value, comparator=comparator))

    def __len__(self) -> int:
        """
        Returns the current number of cards in the deck.
        """
        return len(self._deck)

    def shuffle(self) -> None:
        """
        Shuffles the deck by randomizing the order of the cards.
        """
        shuffle(self._deck)

    def draw(self, take:int) -> List[Card]:
        """
        Draws the specified number of cards from the top of the deck.
        """
        if take > len(self._deck):
            raise ValueError(f"Cannot draw {take} cards from deck since it only contains {len(self._deck)} cards")
        
        drawed_cards = []
        while len(drawed_cards) < take:
            drawed_cards.append(self._deck.pop())

        return drawed_cards

    def pop_card(self) -> Card:
        """
        Pops a card from the top of the deck, if available. 
        """
        return self.draw(1)[0]

    def __iter__(self)-> List[Card]:
        """
        Dunder method to yield cards from a deck.
        """
        for card in self._deck:
            yield card

