from collections import Counter
from app.Card import Card, Suit, FaceCard, DEFAULT_COMPARATOR
from app.Deck import Deck
import unittest

class TestDesk(unittest.TestCase):
    def test_intializes_deck(self):
        # standard deck should contain 52 cards
        d = Deck()
        self.assertEqual(len(d), 52)

        # there should be 13 cards of each squite
        suiteCounter = Counter()
        for card in d:
            suiteCounter[card.suit] += 1

        self.assertEqual(suiteCounter[Suit.Hearts], 13)
        self.assertEqual(suiteCounter[Suit.Diamonds], 13)
        self.assertEqual(suiteCounter[Suit.Spades], 13)
        self.assertEqual(suiteCounter[Suit.Clubs], 13)

    def test_draw(self):
        d = Deck()

        original_length = len(d)

        # let's grab the last 7 
        drawed = d.draw(7)
        self.assertEqual(len(drawed), 7)
        self.assertEqual(len(d), original_length - 7)
        
        # the cards in our hand should not be in our deck.
        remaining_deck = set([(card.suit, card.value) for card in d])
        hand = set([(card.suit, card.value) for card in drawed])
        self.assertTrue(len(remaining_deck.intersection(hand))==0)

    def test_draw_will_not_overdraw(self):
        d = Deck()

        original_length = len(d)
        drawed = d.draw(original_length)
        self.assertEqual(len(drawed), original_length)
        self.assertEqual(len(d), 0)

        # should be no more! 
        with self.assertRaises(ValueError):
            d.draw(1)

    def test_different_comparator(self):
        # tests that a deck can be instantiated with a different comparison ordering
        # in order to accomodate different rules for different games. For this test,
        # we'll make a rule that the '2 of clubs' is the highest card in the deck - it 
        # beats all others. Otherwise, use the standard default ordering that ace's beat other cards.
        def two_of_clubs_beats_all(card1:Card, card2:Card):
            
            # test to see if card1 is highest card. if so, card1 > card2
            if card1.value == 2 and card1.suit == Suit.Clubs:
                return 1
            
            # test to see if card2 is highest card, if so, card2 > card1
            if card2.value == 2 and card2.suit == Suit.Clubs:
                return -1

            # for all else, just call the default
            return DEFAULT_COMPARATOR(card1=card1, card2=card2)

        d = Deck(comparator=two_of_clubs_beats_all)

        # pull out all the cards into a 'hand', except the 2 of clubs
        my_hand = []
        twoOfClubs:Card = None
        while len(d) > 0:
            card = d.pop_card()
            if card.value == 2 and card.suit == Suit.Clubs:
                twoOfClubs = card
            else:
                my_hand.append(card)
                
        # now, each card in my hand should be less than a 2 of clubs
        for card in my_hand:
            self.assertLess(card, twoOfClubs)


    def test_shuffle(self):
        d = Deck()
        cloned = [Card(card.suit, card.value) for card in d]

        d.shuffle()

        # when you shuffle the deck, it should still contain the same cards.
        c1 = Counter()
        for c in cloned:
            c1[(c.suit,c.value)] += 1

        c2 = Counter()    
        for c in d:
            c2[(c.suit,c.value)] += 1

        self.assertEqual(c1,c2)

        # but the ordering should be different.
        cloned_tuples = [(card.suit, card.value) for card in cloned]
        shuffled_tuples = [(card.suit, card.value) for card in d]

        # testing that the lists are equal should fail.
        with self.assertRaises(AssertionError):
            self.assertListEqual(cloned_tuples, shuffled_tuples)