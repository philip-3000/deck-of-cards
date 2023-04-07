from app.Card import Card, Suit, FaceCard, DEFAULT_COMPARATOR
import unittest

class TestCard(unittest.TestCase):
    def test_cannot_be_initialized_with_bad_suite(self):
        with self.assertRaises(ValueError):
            _ = Card(suit="bad suite", value=3)

    def test_cannot_be_initialized_with_invalid_card_value(self):
        with self.assertRaises(ValueError):
            _ = Card(suit=Suit.Hearts, value=0)

        with self.assertRaises(ValueError):
            _ = Card(suit=Suit.Hearts, value=42)

    def can_hash(self):
        m = {}
        card = Card(suit=Suit.Clubs, value=3)
        m[card] = 1     
        self.assertTrue(card in m)   

    def test_less_than(self):
        threeOfHearts = Card(suit=Suit.Hearts, value=3)
        fourOfHearts = Card(suit=Suit.Spades, value=4)
        self.assertLess(threeOfHearts, fourOfHearts)

    def test_less_than_or_equal_to(self):
        card1 = Card(suit=Suit.Hearts, value=4)
        card2 = Card(suit=Suit.Clubs, value=4)
        self.assertLessEqual(card1, card2)

        card1 = Card(suit=Suit.Hearts, value=3)
        self.assertLessEqual(card1, card2)

    def test_greater_than(self):
        threeOfHearts = Card(suit=Suit.Hearts, value=3)
        fourOfHearts = Card(suit=Suit.Diamonds, value=4)
        self.assertGreater(fourOfHearts, threeOfHearts)

    def test_greater_than_or_equal_to(self):
        card1 = Card(suit=Suit.Hearts, value=4)
        card2 = Card(suit=Suit.Clubs, value=4)
        self.assertGreaterEqual(card1, card2)

        card1 = Card(suit=Suit.Hearts, value=5)
        self.assertGreaterEqual(card1, card2)

    def test_equals(self):
        card1 = Card(suit=Suit.Hearts, value=4)
        card2 = Card(suit=Suit.Spades, value=4)
        self.assertEqual(card1, card2)

    def test_not_equals(self):
        card1 = Card(suit=Suit.Hearts, value=5)
        card2 = Card(suit=Suit.Clubs, value=4)
        self.assertNotEqual(card1, card2)

    def test_aces_high_by_default(self):
        # by default, the cards should have aces 'high' in that they are the greatest ranked card.
        kingOfHearts = Card(suit=Suit.Hearts, value=FaceCard.King.value)
        aceOfDiamonds = Card(suit=Suit.Diamonds, value=1)
        self.assertGreater(aceOfDiamonds, kingOfHearts)

    def test_custom_comparator(self):
        # tests that two cards can be compared via custom logic.
        # in this comparison function, we'll make 2's the highest card.
        # and then just use the default ordering function when 
        # the cards aren't a 2.
        def custom_comparator(card1:Card, card2:Card) -> int:
            if card1.value == 2 and card2.value != 2:
                return 1
            
            if card2.value == 2 and card1.value != 2:
                return -1

            return DEFAULT_COMPARATOR(card1=card1, card2=card2)

        twoOfDiamonds = Card(suit=Suit.Diamonds, value=2, comparator=custom_comparator)
        aceOfSpades = Card(suit=Suit.Spades, value=1, comparator=custom_comparator)
        kingOfHearts = Card(suit=Suit.Hearts, value=FaceCard.King.value, comparator=custom_comparator)
        self.assertLess(aceOfSpades, twoOfDiamonds)
        self.assertGreater(twoOfDiamonds, aceOfSpades)
        self.assertGreater(aceOfSpades, kingOfHearts)


    def test_is_face_card(self):
        card1 = Card(suit=Suit.Hearts, value=5)
        self.assertFalse(card1.isFaceCard())

        card1 = Card(suit=Suit.Hearts, value=FaceCard.Jack.value)
        self.assertTrue(card1.isFaceCard())

