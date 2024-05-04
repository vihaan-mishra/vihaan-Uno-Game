#!/usr/bin/env python
# coding: utf-8

# In[26]:


'''class UnoDeck:
    def __init__(self):
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0, color))  # one 0 of each color
            for i in range(2):
                for n in range(1, 10):  # two of each of 1-9 of each color
                    self.deck.append(UnoCard(n, color))
            for d in range(2):  # Add two of each action card
                self.deck.append(UnoCard('Skip', color))
                self.deck.append(UnoCard('Reverse', color))
                self.deck.append(UnoCard('Draw Two', color))
        random.shuffle(self.deck)
'''

# if card is:
#    Skip: next players turn is skipped
#    Draw Two: next player turn draws 2 cards and is skipped
#    Reverse: goes back to previous player turn, 
# Same matching is used for each card: If skip played, latter person can play blue or another skip

import random

class UnoCard:
    '''represents an Uno card
    attributes:
      rank: int from 0 to 9
      color: string'''

    def __init__(self, rank, color):
        '''UnoCard(rank, color) -> UnoCard
        creates an Uno card with the given rank and color'''
        self.rank = rank
        self.color = color

    def __str__(self):
        '''str(Unocard) -> str'''
        return(str(self.color) + ' ' + str(self.rank))

    def is_match(self, other):
        '''UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in rank or color, False if not'''
        return (self.color == other.color) or (self.rank == other.rank)

class UnoDeck:
    '''represents a deck of Uno cards
    attribute:
      deck: list of UnoCards'''

    def __init__(self):
        '''UnoDeck() -> UnoDeck
        creates a new full Uno deck'''
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0, color))  # one 0 of each color
            for i in range(2):
                for n in range(1, 10):  # two of each of 1-9 of each color
                    self.deck.append(UnoCard(n, color))
                
                self.deck.append(UnoCard('Skip', color))
                self.deck.append(UnoCard('Reverse', color))
                self.deck.append(UnoCard('Draw Two', color)) 
                
        random.shuffle(self.deck)  # shuffle the deck

    def __str__(self):
        '''str(Unodeck) -> str'''
        return 'An Uno deck with '+str(len(self.deck)) + ' cards remaining.'

    def is_empty(self):
        '''UnoDeck.is_empty() -> boolean
        returns True if the deck is empty, False otherwise'''
        return len(self.deck) == 0

    def deal_card(self):
        '''UnoDeck.deal_card() -> UnoCard
        deals a card from the deck and returns it
        (the dealt card is removed from the deck)'''
        return self.deck.pop()

    def reset_deck(self, pile):
        '''UnoDeck.reset_deck(pile) -> None
        resets the deck from the pile'''
        if len(self.deck) != 0:
            return
        self.deck = pile.reset_pile() # get cards from the pile
        random.shuffle(self.deck)  # shuffle the deck

class UnoPile:
    '''represents the discard pile in Uno
    attribute:
      pile: list of UnoCards'''

    def __init__(self, deck):
        '''UnoPile(deck) -> UnoPile
        creates a new pile by drawing a card from the deck'''
        card = deck.deal_card()
        self.pile = [card]  # all the cards in the pile

    def __str__(self):
        '''str(UnoPile) -> str'''
        return 'The pile has ' + str(self.pile[-1]) + ' on top.'

    def top_card(self):
        '''UnoPile.top_card() -> UnoCard
        returns the top card in the pile'''
        return self.pile[-1]

    def add_card(self, card):
        '''UnoPile.add_card(card) -> None
        adds the card to the top of the pile'''
        self.pile.append(card)

    def reset_pile(self):
        '''UnoPile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of UnoCards'''
        newdeck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return newdeck

class UnoPlayer:
    '''represents a player of Uno
    attributes:
      name: a string with the player's name
      hand: a list of UnoCards'''

    def __init__(self, name, deck):
        '''UnoPlayer(name, deck) -> UnoPlayer
        creates a new player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.deal_card() for i in range(7)]

    def __str__(self):
        '''str(UnoPlayer) -> UnoPlayer'''
        return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'

    def get_name(self):
        '''UnoPlayer.get_name() -> str
        returns the player's name'''
        return self.name

    def get_hand(self):
        '''get_hand(self) -> str
        returns a string representation of the hand, one card per line'''
        output = ''
        for card in self.hand:
            output += str(card) + '\n'
        return output

    def has_won(self):
        '''UnoPlayer.has_won() -> boolean
        returns True if the player's hand is empty (player has won)'''
        return len(self.hand) == 0

    def draw_card(self, deck):
        '''UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn'''
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)   # add this card to the hand
        return card

    def play_card(self, card, pile):
        '''UnoPlayer.play_card(card, pile) -> None
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!'''
        self.hand.remove(card)
        pile.add_card(card)

    def take_turn(self, deck, pile):
        '''UnoPlayer.take_turn(deck, pile) -> None
        takes the player's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''        
        # print player info
        print(self.name + ", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]            
        if len(matches) > 0:  # can play        
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index + 1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            choice = -1
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # play the chosen card from hand, add it to the pile
            chosenCard = matches[choice - 1]
            self.play_card(chosenCard, pile)
            # if chosenCard is a 'Action Card' carry out steps in play_uno function
            if chosenCard.rank == 'Draw Two':
                return 'Draw Two'
            elif chosenCard.rank == 'Reverse':
                return 'Reverse'
            elif chosenCard.rank == 'Skip':
                return 'Skip'
        else:  # can't play
            print("You can't play, so you have to draw.")
            input("Press enter to draw.")
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            if newcard.is_match(topcard): # can be played
                print("Good -- you can play that!")
                self.play_card(newcard,pile)
                chosenCard = matches[choice - 1]
                self.play_card(chosenCard, pile)
                if chosenCard.rank == 'Draw Two':
                    return 'Draw Two'
                elif chosenCard.rank == 'Reverse':
                    return 'Reverse'
                elif chosenCard.rank == 'Skip':
                    return 'Skip'
            else:   # still can't play
                print("Sorry, you still can't play.")
                if pile.top_card().rank == 'Draw Two':
                    return 'Draw Two'
                elif pile.top_card().rank == 'Reverse':  
                    return 'Reverse'
                elif pile.top_card().rank == 'Skip':
                    return 'Skip'
            input("Press enter to continue.")
        return None 

def play_uno(numPlayers):
    '''play_uno(numPlayers) -> None
    plays a game of Uno with numPlayers'''
    # set up full deck and initial discard pile
    deck = UnoDeck()
    pile = UnoPile(deck)
    # set up the players
    playerList = []
    for n in range(numPlayers):
        # get each player's name, then create an UnoPlayer
        name = input('Player #' + str(n + 1) + ', enter your name: ')
        playerList.append(UnoPlayer(name,deck))
    # randomly assign who goes first
    currentPlayerNum = random.randrange(numPlayers)
    # set up order of players
    direction = True
    # play the game
    while True:
        # print the game status
        print('-------')
        for player in playerList:
            print(player)
        print('-------')
        # take a turn
        card_val = playerList[currentPlayerNum].take_turn(deck, pile)
        # check for a winner
        if playerList[currentPlayerNum].has_won():
            print(playerList[currentPlayerNum].get_name() + " wins!")
            print("Thanks for playing!")
            break
        # checks if card played is 'Draw Two', skips player by moving two places and gives skipped player two cards
        if card_val == 'Draw Two':
            if direction:
                currentPlayerNum = (currentPlayerNum + 2) % numPlayers
            else:
                currentPlayerNum = (currentPlayerNum - 2) % numPlayers
            print('Sorry, ' + str(playerList[currentPlayerNum - 1].name) + ' you have to draw 2 cards AND your turn is skipped!')
            for i in range(2):
                newcard = playerList[currentPlayerNum].draw_card(deck)
                print("You drew: "+str(newcard))
            input("Press enter to continue.")
        # checks if card played is 'Reverse', then changes variable direction to change order    
        elif card_val == 'Reverse':
            direction = not direction
            if direction:
                currentPlayerNum = (currentPlayerNum + 1) % numPlayers
            else:
                currentPlayerNum = (currentPlayerNum - 1) % numPlayers
            print('The turns are reversed!')
            print("The current player is: ", playerList[currentPlayerNum].name)
        # checks if card played is 'Skip' and then moves two places  
        elif card_val == 'Skip':
            if direction:
                currentPlayerNum = (currentPlayerNum + 2) % numPlayers
            else:
                currentPlayerNum = (currentPlayerNum - 2) % numPlayers
            print('Sorry, ' + str(playerList[currentPlayerNum - 1].name) + 'your turn is skipped!')
            print("Current player: ", playerList[currentPlayerNum].name)  
        # if card played is normal, go to next player
        else:
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers
        
play_uno(3)


# In[ ]:




