from random import sample 
import random

# Rule Based AI
class ruleAI:
    def __init__(self, name):
        self.hand = []
        self.game_state = []
        self.split_suit = None
        self.score = 0
        self.name = name
        self.status = 'alive'
        
    def updateGameState(self, new_game_state):
        self.game_state = new_game_state
        
        if len(new_game_state) != 0:
            self.split_suit = new_game_state[0].suit
        
    def setHand(self, new_hand):
        self.hand = new_hand
        
    def updateHand(self, card_to_remove):
        self.hand.remove(card_to_remove)
        
    def solveSplit(self):
        playable_cards = self.getCardsOfSuit()
        
        if len(self.game_state) == 0 or len(playable_cards) == 0:
            return self.getLowest()
    
        elif len(playable_cards) == 1:
            return playable_cards[0]
        
        highest_playable = self.getHighestPlayable()
        split_highest = self.getSplitHighest()
        
        if highest_playable.value > split_highest.value:
            return highest_playable
        
        else:
            return self.getLowestPlayable()
    
    def getCardsOfSuit(self):
        to_return = []
        for idx, card in enumerate(self.hand):
            if card.suit == self.split_suit:
                to_return.append(card)
                
        return to_return
    
    def getLowest(self):
        lowest_card = self.hand[0]
        lowest_value = lowest_card.value
        for idx, card in enumerate(self.hand[1:]):
            if card.value < lowest_value:
                lowest_card = card
        
        return lowest_card
    
    # Return highest cart following the split suit
    def getHighestPlayable(self):
        highest_card = self.hand[0]
        highest_value = highest_card.value
        for idx, card in enumerate(self.hand[1:]):
            if card.value > highest_value and card.suit == self.split_suit:
                highest_card = card
        
        return highest_card
    
    def getLowestPlayable(self):
        lowest_card = self.hand[0]
        lowest_value = lowest_card.value
        for idx, card in enumerate(self.hand[1:]):
            if card.value < lowest_value and card.suit == self.split_suit:
                lowest_card = card
        
        return lowest_card
    
    # Return the highest cards in the split with the correct suit
    def getSplitHighest(self):
        highest_card = self.game_state[0]
        highest_value = highest_card.value
        for idx, card in enumerate(self.game_state[1:]):
            if card.value > highest_value and card.suit == self.split_suit:
                highest_card = card
        
        return highest_card
    
    def increaseScore(self, round_value):
        self.score = self.score + round_value
        
        if self.score >= 15:
            self.status = 'dead'
            print(f'{self.name} lost')
        
    def getName(self):
        return self.name
    
    def printPlayer(self):
        print(f'-{self.name}, score: {self.score}')
        