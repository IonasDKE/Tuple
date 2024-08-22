from RuleBasedAI import ruleAI
from GameEngine import GameEngine, Card
from MonteCarloTreeSearch import MCTS

def game():
        player_1 = ruleAI('player 1')
        player_2 = ruleAI('player 2')
        player_3 = ruleAI('player 3')

        players = [player_1, player_2, player_3]
        game_engine = GameEngine(players)

        #i=1
        #while i < 5:
        #    i = i +1
        while len(game_engine.getPlayers()) != 1:
            #test = test +1
            """Deal cards"""
            hands = game_engine.deal()
            for idx, hand in enumerate(hands):
                players[idx].setHand(hand)


            #while game_engine.split_number <= 4:
            while len(game_engine.getPlayers()[0].hand) != 0:
                print(f'Split number: {game_engine.split_number}')
                game_state = []
                
                """Every player plays 1 card"""
                for player in game_engine.getPlayers():
                    player.updateGameState(game_state)
                    card_played = player.solveSplit()
                    game_state.append(card_played)
                    player.updateHand(card_played)
                    game_engine.updateGameState(game_state)
                
                game_engine.printGameState()   
                print()
                game_engine.defineSplitWinner()
                
            game_engine.resetSplitNumber()    
            game_engine.printPlayers()
            print('- - - - - ')

def test():
    player_1 = ruleAI('player 1')
    player_2 = MCTS('player 2')

    players = [player_1, player_2]
    game_engine = GameEngine(players)

    while len(game_engine.getPlayers()) != 1:
        #test = test +1
        """Deal cards"""
        hands = game_engine.deal()
        for idx, hand in enumerate(hands):
            players[idx].setHand(hand)


        #while game_engine.split_number <= 4:
        while len(game_engine.getPlayers()[0].hand) != 0:
            print(f'Split number: {game_engine.split_number}')
            game_state = []
            
            """Every player plays 1 card"""
            for player in game_engine.getPlayers():
                player.updateGameState(game_state)
                card_played = player.solveSplit()
                game_state.append(card_played)
                player.updateHand(card_played)
                game_engine.updateGameState(game_state)
            
            game_engine.printGameState()   
            print()
            game_engine.defineSplitWinner()
            
        game_engine.resetSplitNumber()    
        game_engine.printPlayers()
        print('- - - - - ')

if __name__ == '__main__':

    test()
