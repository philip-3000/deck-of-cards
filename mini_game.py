from src.app.Card import Card
from src.app.Deck import Deck


if __name__ == "__main__":
    # We'll just play a simple game with the deck. Each player is 
    # dealt 3 cards. The player with the top (i.e. highest ranked card)
    # card in their hand wins.

    # create a deck of cards and shuffle them.
    deck_of_cards = Deck()
    deck_of_cards.shuffle()

    # hand out 7 to each player.
    player_one_hand = deck_of_cards.draw(3)
    player_two_hand = deck_of_cards.draw(3)

    # print the hand out so we can see it.
    print("Player One's Cards:")
    for c in player_one_hand:
        print(f"\t{c}")

    max_player_one_card = max(player_one_hand)
    print(f"\nPlayer One's Top Card: {max_player_one_card}\n")

    print("Player Two's Cards:")
    for c in player_two_hand:
        print(f"\t{c}")

    max_player_two_card = max(player_two_hand)
    print(f"\nPlayer Two's Top Card: {max_player_two_card}\n")

    if max_player_one_card > max_player_two_card:
        print("Player One Wins!")
    elif max_player_one_card < max_player_two_card:
        print("Player Two Wins!")
    else:
        print("It's a Draw!")
    
    
    