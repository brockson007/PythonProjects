# A simple BlackJack game
# Created by Brock Hayes

import random
import time
import locale

# Global Values
SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
          'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
PLAYING = True
playerName = ""

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += VALUES[card.rank]
        if card.rank == "Ace":
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand: ", *player.cards, sep='\n')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep='\n')
    print("Player's Hand = ", player.value)


def push():
    print("Dealer and Player tie! It's a push.")


class Player:
    def __init__(self, name):
        self.name = name
        self.amount = 1000
        self.bet = 0

    def take_bet(self, money):
        while True:
            try:
                self.bet = int(input("How much money would you like to bet? "))
            except ValueError:
                print('Sorry, a bet must be an integer!')
            else:
                if self.bet > money:
                    print("Sorry, your bet can't exceed", money)
                else:
                    break

    def win_bet(self):
        self.amount += self.bet

    def lose_bet(self):
        self.amount -= self.bet

    def hit_or_stand(self, deck, hand):
        # Controls upcoming while loop
        global PLAYING
        while True:
            x = input("\nWould you like to Hit or Stand? Enter 'h' or 's' ")
            try:
                x[0].lower()
            except IndexError:
                continue
            if x[0].lower() == 'h':
                hit(deck, hand)
            elif x[0].lower() == 's':
                print("Player stands. Dealer is playing. ")
                PLAYING = False
            else:
                print("Please enter either 'h' or 's' ")
                continue
            break

    def player_busts(self):
        print("Player busts!")
        self.lose_bet()

    def player_wins(self):
        print("Player wins!")
        self.win_bet()

    def dealer_busts(self):
        print("Dealer busts!")
        self.win_bet()

    def dealer_wins(self):
        print("Dealer wins!")
        self.lose_bet()


print('''
    
 _______   __                      __                                    __       
/       \ /  |                    /  |                                  /  |      
$$$$$$$  |$$ |  ______    _______ $$ |   __      __   ______    _______ $$ |   __ 
$$ |__$$ |$$ | /      \  /       |$$ |  /  |    /  | /      \  /       |$$ |  /  |
$$    $$< $$ | $$$$$$  |/$$$$$$$/ $$ |_/$$/     $$/  $$$$$$  |/$$$$$$$/ $$ |_/$$/ 
$$$$$$$  |$$ | /    $$ |$$ |      $$   $$<      /  | /    $$ |$$ |      $$   $$<  
$$ |__$$ |$$ |/$$$$$$$ |$$ \_____ $$$$$$  \     $$ |/$$$$$$$ |$$ \_____ $$$$$$  \ 
$$    $$/ $$ |$$    $$ |$$       |$$ | $$  |    $$ |$$    $$ |$$       |$$ | $$  |
$$$$$$$/  $$/  $$$$$$$/  $$$$$$$/ $$/   $$/__   $$ | $$$$$$$/  $$$$$$$/ $$/   $$/ 
                                          /  \__$$ |                              
                                          $$    $$/                               
                                           $$$$$$/
''')
# Opening statement
print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
       Dealer hits until they reach 17. Aces count as 1 or 11.\n')
time.sleep(1)
while playerName == "":
    playerName = input("What is your name stranger? ")
playerOne = Player(playerName)
print("Welcome " + playerOne.name.capitalize() + "!")
time.sleep(2)
print("Your starting amount is", locale.format_string('$%.0f', playerOne.amount))
time.sleep(1)

while True:

    # Creates and shuffles the deck, deals two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Prompt the Player for their bet
    playerOne.take_bet(playerOne.amount)

    # Show cards (keeps one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while PLAYING:

        # Prompt Player to Hit or Stand
        playerOne.hit_or_stand(deck, player_hand)

        # Show cards (keeps one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            playerOne.player_busts()
            break
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            playerOne.dealer_busts()
        elif dealer_hand.value > player_hand.value:
            playerOne.dealer_wins()
        elif dealer_hand.value < player_hand.value:
            playerOne.player_wins()
        else:
            push()

    # Inform player of their money total
    print("\nPlayer's winnings stand at", playerOne.amount)

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

    if new_game[0].lower() == 'y':
        PLAYING = True
    else:
        print("Thanks for playing!")
        break
