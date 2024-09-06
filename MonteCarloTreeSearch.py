from random import sample 
import random
from GameEngine import Card, GameEngine

class MCTS:
    def __init__(self, name):
        self.hand = []
        self.cards_not_played = [] # List of cards potentially in other players hand or in pile
        self.setMemory()
        
        self.game_state = []
        self.split_suit = None
        self.score = 0
        self.name = name
        self.status = 'alive'
        self.tree = None
        
    def setMemory(self):
        suits = ['Heart','Diamonds','Spades','Clubs']
        values = [10, 9, 8, 7, 6, 5, 4, 3]
        
        for v in values:
            for s in suits:
                self.cards_not_played.append(Card(v,s))
                
    def updateMemory(self, cards_played):
        for card in cards_played:
            if card in self.cards_not_played:
                self.cards_not_played.remove(card)

    def setGameEngine(self, copy_game_engine):
        self.game_engine_copy = copy_game_engine
        self.nb_opponents = len(self.game_engine_copy.getPlayers())
        
    def updateGameState(self, new_game_state):
        self.game_state = new_game_state
        self.updateMemory(new_game_state)
        
        if len(new_game_state) != 0:
            self.split_suit = new_game_state[0].suit
    
    def setHand(self, new_hand):
        self.hand = new_hand
        self.updateMemory(new_hand)
        # self.Tree.extendTree(new_hand)
        
    def updateHand(self, card_to_remove):
        self.hand.remove(card_to_remove)
        
    def increaseScore(self, round_value):
        self.score = self.score + round_value
        
        if self.score == 15:
            self.status = 'dead'
            print(f'{self.name} lost')
        
    def getName(self):
        return self.name
    
    def printPlayer(self):
        print(f'-{self.name}, score: {self.score}')
        
    def deal_to_opponent(self):
        hands = []
        cards_copy = self.cards_not_played.copy()
        
        number_of_cards = 4 - (self.game_engine_copy.split_number -1) # If split number 2 we wanna deal 3 cards that's why -1
        
        for i in range(self.nb_opponents):
            hand = sample(cards_copy, number_of_cards)
            hands.append(hand)
            for e in hand:
                cards_copy.remove(e)
            
        return hands
    
    # return the cards of the split suit
    def getPlayableCards(self, nodes):
        split_suit = self.game_state[0].suit
        playable_cards = []

        for node in nodes:
            if node.getCard().suit == split_suit:
                playable_cards.append(node)

        if playable_cards:
            return playable_cards
        
        else:
            return nodes
        
    def solveSplit(self):
        nodes = self.root.getChildren()
        
        if len(self.game_state) != 0:
            playable_nodes = self.getPlayableCards(nodes)

        for _ in range(100):
            selected_node = random.sample(playable_nodes, 1)[0]
            self.updateNode(selected_node)
        
        largest_score = 0
        best_node = nodes[0]
        for node in nodes:
            if node.getScore() > largest_score:
                best_node = node 
                        
        return best_node.card

    def updateNode(self, selected_node):
        game_state_copy = self.game_state.copy()
        dummy_players = self.game_engine_copy.getPlayers()

        self.updateMemory(game_state_copy)

        hands = self.deal_to_opponent()
        for idx, hand in enumerate(hands):
            dummy_players[idx].setHand(hand)

        split_winner = self.play(dummy_players, game_state_copy)
        outcome = self.getSplitOutcome(split_winner, game_state_copy)
        selected_node.updateScore(outcome)

    def play(self, dummy_players, game_state_copy):

        while len(dummy_players[0].hand) != 0:

            if len(game_state_copy) != 0:
                players = self.game_engine_copy.getPlayers()
                
            else:
                players = self.game_engine_copy.players_split_order[len(game_state):]

            """Every players plays 1 card"""
            for player in players:
                player.updateGameState(game_state_copy)
                card_played = player.solveSplit()
                game_state_copy.append(card_played)
                player.updateHand(card_played)
                self.game_engine_copy.updateGameState(game_state_copy)

            self.game_engine_copy.defineSplitWinner()

        return self.game_engine_copy.getLastSplitWinner()
    
    # Return 1 if the winner is MCTS, 0 otherwise
    def getSplitOutcome(self, split_winner):
        return int(split_winner == self)
    

class Tree():
    def __init__(self):
        self.root = Node(None, None)
        
    def getRoot(self):
        return self.root
    
    def setRoot(self, new_root):
        self.root = new_root
        
    def extendTree(self, parent, hand):   
        if len(hand) > 0:
            for card in self.hand:
                new_node = Node(parent, card)
                parent.addChild(new_node)       
                self.extendNode(new_node, hand.remove(card))
                
        else:
            return
        
    def extendNode(new_node, hand):

        return 
        
class Node():
    def __init__(self, parent, card):
        self.parent = parent
        self.children = []
        
        self.score = 0
        self.times_visited = 0
        self.win_counter = 0
        self.card = card
        
    def addChild(self, new_child):
        self.children.append(new_child)
    
    # Succes is either 1 or 0 
    def updateScore(self, succes):
        self.win_counter = self.win_counter + succes
        self.times_visited = self.times_visited + 1
        
        self.score = self.win_counter/self.times_visited
        
    def getScore(self):
        return self.score
    
    def setCard(self, card):
        self.card = card
        
    def getCard(self):
        return self.card
        
    def getChildren(self):
        return self.children
        