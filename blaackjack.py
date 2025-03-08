import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"

class Deck:
    def __init__(self):
        self.build()
        self.shuffle()

    def build(self):
        suits = ["spades", "clubs", "hearts", "diamonds"]
        ranks = [
            {"rank": "A", "value": 11},
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            {"rank": "4", "value": 4},
            {"rank": "5", "value": 5},
            {"rank": "6", "value": 6},
            {"rank": "7", "value": 7},
            {"rank": "8", "value": 8},
            {"rank": "9", "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "J", "value": 10},
            {"rank": "Q", "value": 10},
            {"rank": "K", "value": 10},
        ]
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, number):
        return [self.cards.pop() for _ in range(min(number, len(self.cards)))]

class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate_value(self):
        value = sum(card.rank["value"] for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank["rank"] == "A")
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    def get_value(self):
        return self.calculate_value()

    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_value() == 21

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank["rank"] == self.cards[1].rank["rank"]

    def display(self, show_all_dealer_cards=False):
        print(f"{'Dealer' if self.dealer else 'Your'} hand:")
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards:
                print("hidden")
            else:
                print(card)
        if not self.dealer:
            print("Value:", self.get_value())
        print()

class Game:
    def play(self):
        currency = self.get_currency()
        deck = Deck()

        while currency > 0:
            print("\n" + "*" * 30)
            print(f"New Game! You have {currency} chips left!")
            print("*" * 30)

            bet = self.get_bet(currency)
            bets = [bet]  # Listă de pariuri per mână

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            player_hand.add_card(deck.deal(2))
            dealer_hand.add_card(deck.deal(2))

            dealer_hand.display()
            player_hand.display()
            
            hands_to_play = [player_hand]
            
            if player_hand.can_split() and bet * 2 <= currency:
                choice = self.get_split_choice()
                if choice == "yes":
                    hand1 = Hand()
                    hand2 = Hand()
                    hand1.add_card([player_hand.cards[0], deck.deal(1)[0]])
                    hand2.add_card([player_hand.cards[1], deck.deal(1)[0]])
                    hands_to_play = [hand1, hand2]
                    bets = [bet, bet]

            for i, hand in enumerate(hands_to_play):
                print(f"\nPlaying hand {i + 1}:")
                hand.display()
                can_double = 1 
                if bets[i] * 2 > currency:
                     can_double = 0
                while hand.get_value() < 21:
                    choice = self.get_player_choice()
                    if choice in ["double", "d"]: 
                        if can_double == 1:
                            hand.add_card(deck.deal(1))
                            hand.display()
                            bets[i] *= 2
                            break
                        else :
                            print("You don't have enough chips to use double or you already used hit")
                            continue
                    if choice in ["hit", "h"]:
                        hand.add_card(deck.deal(1))
                        hand.display()
                        can_double = 0
                    else:
                        break

            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal(1))
            dealer_hand.display(show_all_dealer_cards=True)

            print("Final Results")
            for i, hand in enumerate(hands_to_play):
                print(f"Your hand {i + 1}: {hand.get_value()}")
                print(f"Dealer's hand: {dealer_hand.get_value()}")
                if hand.get_value() > 21:
                    currency -= bets[i]
                elif dealer_hand.get_value() > 21:
                    currency += bets[i]
                elif dealer_hand.is_blackjack() and hand.is_blackjack():
                    pass  # Push
                elif hand.is_blackjack():
                    currency += bets[i] + bets[i] // 3
                elif dealer_hand.is_blackjack():
                    currency -= bets[i]
                else:
                    if hand.get_value() > dealer_hand.get_value():
                        currency += bets[i]
                    elif hand.get_value() < dealer_hand.get_value():
                        currency -= bets[i]
            
            deck = Deck()
        print("\nThanks for playing!")

    def get_currency(self):
        while True:
            try:
                currency = int(input("How many chips do you want? "))
                if 1 <= currency <= 10000:
                    return currency
                print("Please enter a number between 1 and 10000.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def get_bet(self, currency):
        while True:
            try:
                bet = int(input("How much do you want to bet? "))
                if 1 <= bet <= currency:
                    return bet
                print(f"Enter a number between 1 and {currency}!")
            except ValueError:
                print("Invalid input. Enter a number.")

    def get_player_choice(self):
        return input("Please choose 'Hit' or 'Stand' or 'Double' (H/S/D): ").lower()

    def get_split_choice(self):
        return input("You have a pair! Do you want to split? (yes/no): ").lower()

g = Game()
g.play()
