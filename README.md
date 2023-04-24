# Prompt
Design a class deck of cards that can be used for different card game applications.

What is the deck of cards: A "standard" deck of playing cards consists of 52 cards in each of the 4 suites of Spades, Hearts, Diamonds, and Clubs. Each suit contains 13 cards: Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King.

# A few assumptions
I'm going to assume the following for simplicity:
- an 'Ace' has a numerical value of 1.
- a 'Jack' has a numerical value of 11.
- a 'Queen' has a numerical value of 12.
- a 'King' has a numerical value of 13.

I am not a card player, but, a quick inspection of some [rules](https://en.wikipedia.org/wiki/High_card_by_suit) for comparing cards looks like it depends on the game or could even be arbitrary. This influenced my design in how I compare cards. 

# Designing a Card
Before we can build a deck of cards, we need to decide how we'd like to represent a card in our deck. Each card in a deck can be modeled by something that has a suit and a value. At it's simplest form, you could probably use a list of tuples:

```python
deck = [('Hearts', 1), ('Hearts', 2),..,('Diamonds', 13)]
```

where the first item in the tuple is the suit and the second is the card value. However, we want to abstract this a bit so that we can:

- write some modular components to represent a card as well as a deck of cards.
- have a standard way of comparing cards, i.e., is a 'Queen of Hearts' as valuable as a 'Queen of Diamonds'?

We can start with a Card class to represent the current suit and value of a given card, as well as provide some operations we might find useful when playing cards. Let's start with state.  We need:

- suit: indicates whether the card is a 'Hearts', 'Diamonds', 'Clubs' or 'Spades'
- value: indicates the card value, i.e. a numerical value from 1 - 13 (inclusive).

We can use class/member variables for these two pieces of data, however, as I thought through this, it seemed like perhaps we'd want to build some immutability into our cards.  That is, if we have a card that is say a 'Queen of Hearts', we probably shouldn't be able to mutate this card into a '10 of Spades'.  For this, we can use Python propertes, for example:

```python
@property
def value(self):
    return self.__value
```

but, leave the setter decorator out.  Attemping to change the value after initialization will result in an error being raised.  However, since nothing is really private in Python, a programmer could access our class member, '__value', but, there's intent with using a property.  

In order to build on the idea of a card being immutable once constructed, we can also implement the 'dunder' method, \__hash\__ so that we could throw our cards into a hash like structure such as a set or map if need be.  In order to do this, we can just think of a card as a tuple, as suggested above:

```python
def __hash__(self) -> int:
    return hash((self.suite, self.value))
```

In Python we can use 'dunder' methods to determine if two cards are:
 - equal (have same card value)
 - not equal (have different card values)
 - less than (card 1 has a value less than card 2)
 - less than or equal to (card 1 has a value less than or equal to card 2)
 - greater than (card 1 has a value greater than card 2)
 - greater than or equal to (card 1 has a value greater than card 2)

At first, since I'm fairly inexperienced at playing cards, I thought that the Ace card always outranked all other cards.  However, after looking up some [rules](https://en.wikipedia.org/wiki/High_card_by_suit), I found that is not the case; it depends on the game we're playing. So, I tried to think of a way that we could use the Card class itself to introduce an ordering or comparison logic, but, leave the actual comparison to a higher level component, such as a 'Deck' or a 'Game' class.  I took inspiration from utilizing sorting functions that allow you to pass in a comparator (see [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort) for JavaScript, and [here](https://docs.python.org/3/howto/sorting.html#comparison-functions) for Python):

- the comparator function should return a negative integer if card 1 is less than card 2.
- the comparator functon should return 0 if card 1 is equal to card 2.
- the comparator function should return a positive integer if card 1 is greater than card 2.

For simplicity, I assumed that a default way to compare cards could be:
- Ace's are the highest value card
- the suit of the card doesn't matter. That is, a 'Queen of Hearts' is equal to a 'Queen of Diamonds'. 

Then I can instantiate my Card objects with a default comparator:

```python
def __init__(self, suit:Suit, value:int, comparator:Callable[[Card, Card], int]=DEFAULT_COMPARATOR) -> None:
    # initialization code goes here...
```

We can now implement the Python magic methods for comparison of cards, and we can just delegate that logic to our comparator function.  Here's an example of implementing the 'less than' operator, '<':

```python
def __lt__(self, __o:Card) -> bool:
    return self._comparator(self, __o) < 0
```

At this point, we can implement the rest of the comparison magic methods so that we can compare cards to each other.  Now that we have a way to represent cards, we can put them into a deck.  So let's move on to that.

# Designing a Deck
Our deck needs to contain a collection of 52 cards, namely 13 cards of each suite (52 in total). So, we need a way to store the cards. We also might need to support some operations that model people playing cards, namely:
- we should be able to shuffle the deck to put the cards in a randomized order.
- most games require drawing from a deck, for example, when dealing out cards to players. 
- different card games might have different rules about ranking cards, so, we probably need a way to deal with this a well.

Let's start with instantiating a deck with the \__init\__ method. How should we store our cards? Well, I guess it would depend on the requirements we need to satisfy.  In the bullet points above, I defined a few things we'd want to do, mainly, shuffling cards, and dealing them off the top of the deck. For that, a simple list/stack structure would be satisfactory:

```python
def __init__(self, comparator:Callable[[Card, Card], int]=DEFAULT_COMPARATOR) -> None:
    self._deck = []
    # for each suit of card
    for suit in Suit:
        # we need to create 13 cards
        for card_value in range(1, FaceCard.King.value + 1):
            self._deck.append(Card(suit=suit, value=card_value, comparator=comparator))
```

Note that we can pass in a comparator function for cards so that they know how to compare themselves.  

Shuffling the deck is fairly straight forward: we can simply use the shuffle() method in the random module. 

Another requirement our Deck needs to satisfy is we'd like to deal cards off the top of the deck. After a deck is shuffled by a dealer, they generally draw _n_ number of cards off the top of the deck and either round robbin them out one at a time to each player, or you could hand each player n cards each. Once a card is drawn from the deck, it's not longer in it. For satisfying this, we can implement a _draw()_ function:

```python
def draw(self, take:int) -> List[Card]:
    """
    Draws the specified number of cards from the top of the deck.
    """
    pass
```

and a convenience method to just pop one card off the deck:

```python
def pop_card(self) -> Card:
    """
    Pops a card from the top of the deck, if available. 
    """
    pass
```

Note that since the Cards themselves are hashable/immutable, we can also store our Cards in a hash like structure such as a set or map, and even an OrderedDictionary class to provide look ups as well as preserve ordering of cards.  However, I elected to keep things simple for now with a list/stack in Python; we might need to utilize the Cards and Deck in an actual Game to see if we need more sophisticated operations on the Deck itself.

# Exercising the Code
There's a suite of tests for the Card as well as Deck. You'll need Python3 to execute them.

From the top level directory:

```shell
cd src
python3 -m unittest discover .  -v
```
Test output will follow:

```shell
test_aces_high_by_default (tests.test_card.TestCard) ... ok
test_cannot_be_initialized_with_bad_suite (tests.test_card.TestCard) ... ok
test_cannot_be_initialized_with_invalid_card_value (tests.test_card.TestCard) ... ok
test_custom_comparator (tests.test_card.TestCard) ... ok
test_equals (tests.test_card.TestCard) ... ok
test_greater_than (tests.test_card.TestCard) ... ok
test_greater_than_or_equal_to (tests.test_card.TestCard) ... ok
test_is_face_card (tests.test_card.TestCard) ... ok
test_less_than (tests.test_card.TestCard) ... ok
test_less_than_or_equal_to (tests.test_card.TestCard) ... ok
test_not_equals (tests.test_card.TestCard) ... ok
test_different_comparator (tests.test_deck.TestDesk) ... ok
test_draw (tests.test_deck.TestDesk) ... ok
test_draw_will_not_overdraw (tests.test_deck.TestDesk) ... ok
test_intializes_deck (tests.test_deck.TestDesk) ... ok
test_shuffle (tests.test_deck.TestDesk) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.008s

OK
```

Additionally, there's also a mini game with the following rules:
- players are dealt 3 cards each
- the player with the top card in their hand wins. Or they can tie.
- uses the default card comparator: Ace is highest card.

To run it from the top level directory:

```shell 
python3 mini_game.py
```

It should produce output similar to the following (but with different cards and result each time):

```shell
Player One's Cards:
	9 of Spades
	Queen of Clubs
	7 of Diamonds

Player One's Top Card: Queen of Clubs

Player Two's Cards:
	5 of Hearts
	3 of Hearts
	9 of Hearts

Player Two's Top Card: 9 of Hearts

Player One Wins!
```
