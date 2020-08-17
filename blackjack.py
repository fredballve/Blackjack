import random
import os

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        if rank == 'Ace':
            self.ace = True
        else:
            self.ace = False
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.deck = []
        
        for rank in ranks:
            for suit in suits:
                self.deck.append(Card(suit,rank))
                
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '/n' + card.__str__()
        return deck_comp
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        
class Chips:
    def __init__(self,total=100):
        self.total = total
        self.bet = 0
    def win_bet(self,blackjack):
        if blackjack:
            self.total += self.bet*1.5
        else:
            self.total += self.bet
    def lose_bet(self):
        self.total -= self.bet
        
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_cards(self,card):
        self.cards.append(card)
        self.value+=values[card.rank]
        if card.rank == "Ace":
            self.aces+=1
            self.adjust_for_ace()
            
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
            
    
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except:
            print("Invalid Input, please input an integer")
        else:
            if chips.bet > chips.total and chips.bet>0:
                print(f"Sorry, you don`t have enought chips! You only have {chips.total}")
            else:
                break
    
def hit_or_stand(deck,hand):
    global playing
    while True:
        aux = input("Would you like to Hit or Stand? (h/s) ")
        if aux[0].lower() == 'h':
            hit(deck,hand)
            break
        elif aux[0].lower() == 's':
            playing = False
            break
        else:
            print("Invalid Input")
        
    
def hit(deck,hand):
    hand.add_cards(deck.deal())
    hand.adjust_for_ace()

def player_busts(chips):
    clear_terminal()
    show_all(player_hand,dealer_hand)
    print(f"Player Busted! You Lost {chips.bet}")
    chips.lose_bet()

def player_wins_blackjack(chips):
    clear_terminal()
    show_all(player_hand,dealer_hand)
    print(f"BLACKJACK! You won {chips.bet*1.5}")
    chips.win_bet(True)
    
def player_wins_normal(chips):
    clear_terminal()
    show_all(player_hand,dealer_hand)
    print(f"Player wins! You won {chips.bet}")
    chips.win_bet(False)

def dealer_busts(chips):
    print(f"Dealer busts! You won {chips.bet}")
    chips.win_bet(False)
    
def dealer_wins(chips):
    print(f"Dealer wins! You lost {chips.bet}")
    chips.lose_bet()
    
def push():
    print(f"Dealer and Player tie! It's a push")

def show_some(player,dealer):
    print("Dealers Hand:")
    print(f" | <Hidden card> | {dealer.cards[1]}")
    print('')
    
    print("Your Hand:")
    print("", *player.cards, sep=' | ')
    print(f'Total value: {player_hand.value}\n')
    
def show_all(player,dealer):
    print("Dealer Hand:")
    print("", *dealer.cards, sep=' | ')
    print(f'Total value: {dealer_hand.value}\n')
    
    print("Your Hand:")
    print("", *player.cards, sep=' | ')
    print(f'Total value: {player_hand.value}\n')


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
played_times = 0
game_on = True    
while game_on:
    clear_terminal()
    if played_times == 0:
        print("Welcome to BlackJack! Get as close to 21 as you can without going over!\nDealer hits until 17. Aces count as 1 or 11\nBlackjack pays 3 to 2")
        player_chips = Chips()
        print(f"\nYou have {player_chips.total} coins\n")
        
    if played_times == 0:
        new_deck = Deck()
        new_deck.shuffle()
        
    if played_times > 5:
        del(new_deck)
        new_deck = Deck()
        new_deck.shuffle()
    
    
    player_hand = Hand()
    player_hand.add_cards(new_deck.deal())
    player_hand.add_cards(new_deck.deal())
            
    dealer_hand = Hand()
    dealer_hand.add_cards(new_deck.deal())
    dealer_hand.add_cards(new_deck.deal())
    take_bet(player_chips)
                
    playing = True
    while playing:
        clear_terminal()
        show_some(player_hand,dealer_hand)
        
        if player_hand.value >21:
            player_busts(player_chips)
            break
        elif player_hand.value == 21:
            break
        else:
            hit_or_stand(new_deck,player_hand)

    if player_hand.value < 21:
        clear_terminal()
        while dealer_hand.value < 17:
            hit(new_deck,dealer_hand)
            
        show_all(player_hand,dealer_hand)
    
        if dealer_hand.value>21 :
            dealer_busts(player_chips)
        elif dealer_hand.value == 21:
            dealer_wins(player_chips)
        elif dealer_hand.value == player_hand.value:
            push()
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins_normal(player_chips)
    
    if player_hand.value == 21:
        if dealer_hand.value == 21:
            print("dealer player and dealer get Blackjack!")
            push()
        else:
            player_wins_blackjack(player_chips)
    
    print(f"You have {player_chips.total} coins")
    if player_chips.total ==0:
        print("Sorry, you don't have coins to play again")
        break
    
    while True:
        play_again = input("Do you want to play again? (y/n) ")
        if play_again[0].lower() == "y":
            played_times += 1
            break
        elif play_again[0].lower() == "n":
            print("Thanks for playing!")
            game_on = False
            break
        else:
            print("Invalid Input")