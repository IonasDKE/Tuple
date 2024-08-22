from random import sample 
import random

from RuleBasedAI import ruleAI

"""- - - Cards - - -"""
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit 
        
    def getValue(self):
        return self.value
    
    def getSuit(self):
        return self.suit
    
    def printCard(self):
        return (f'{self.value}, {self.suit}')

"""- - - Games Engine - - -"""
class GameEngine():
    def __init__(self, players):
        self.players = players
        self.players_split_order = players
        self.number_players = len(players)
        self.game_state = []
        self.cards = []
        self.split_number = 1
        
        self.generateCards()
        
    def generateCards(self):
        suits = ['Heart','Diamonds', 'Spades', 'Clubs']
        values = [10, 9, 8, 7, 6, 5, 4, 3]
        
        for value in values:
            for suit in suits:
                self.cards.append(Card(value,suit))
        
    def deal(self):
        hands = []
        cards_copy = self.cards.copy()
        
        for _ in range(self.number_players):
            hand = sample(cards_copy, 4)
            hands.append(hand)

            # Remove the sampled cards from the pool of possible outcomes
            for card in hand:
                cards_copy.remove(card)
            
        return hands
        
    def defineSplitWinner(self):
        split_suit = self.game_state[0].suit
        current_best_card = self.game_state[0].value
        self.split_winner = self.players[0]
        
        # Define winner
        for idx, card in enumerate(self.game_state):
                if card.suit == split_suit and card.value > current_best_card:
                    self.split_winner = self.players_split_order[idx]
                    current_best_card = card.value
        
        # Last split of the round
        if self.split_number == 4:
            self.updateScores(self.split_winner, current_best_card)
            self.updatePlayerOrder()
            self.split_number = self.split_number + 1
            return
        
        # Intermediate split
        else:
            self.split_number = self.split_number + 1
            # Re-order the players so that the winner starts the next split
            for idx, player in enumerate(self.players_split_order):
                if player == self.split_winner:
                    self.players_split_order = self.players_split_order[idx:] + self.players_split_order[:idx]
                    return
                
    def updateScores(self, split_winner, winning_card):        
        round_value = 1
        if winning_card == 3:
            round_value = 2
            print(f'Round winner: {split_winner.name} with a jack')
        
        else:
            print(f'Round winner: {split_winner.name}')
            
        for player in self.players:
            if player != split_winner:
                player.increaseScore(round_value)
    
    def updatePlayerOrder(self):
        self.players = self.players[1:] + self.players[:1]
        to_remove = []
        for player in self.players:
            if player.status == 'dead':
                to_remove.append(player)
        
        for player in to_remove:
            self.players.remove(player)
                
        self.players_split_order = self.players.copy()
        
    def updateGameState(self, new_game_state):
        self.game_state = new_game_state
        
    def printGameState(self):
        to_return = []
        for idx, card in enumerate(self.game_state):
            print(f'- {self.players_split_order[idx].name}: {card.printCard()}')
            
    def getPlayers(self):
        return self.players_split_order
    
    def printPlayers(self):
        for p in self.players:
            p.printPlayer()
            
    def resetSplitNumber(self):
        self.split_number = 1
        
    def setCards(self, new_cards):
        self.cards = new_cards
        
    def setPlayerSplitOrder(self, new_order):
        self.player_split_order = new_order

    def getLastSplitWinner(self):
        return self.split_winner
        
    def getCopyGameEngine(self):
        dummy_players = [ruleAI(str(x)) for x in range(len(self.players))]
        game_engine_copy = GameEngine(dummy_players)
        game_engine_copy.setPlayerSplitOrder(self.players_split_order)
        game_engine_copy.split_number = self.split_number
        
        return game_engine_copy