import requests, random, RPS_utils
from Players import MarkovChainPlayer, RandomPlayer, PatternPlayer
from Players import IO2LegacyPlayer, RepetitionPredictorPlayer
from Players import AfinitiEndpointPlayer, BeatMostCommonMovePlayer
from Players import HumanPlayer
from Game import Game

iterations = 300
player1 = RandomPlayer.RandomPlayer('Random Player')
player2 = HumanPlayer.HumanPlayer('Human Player')
game = Game(player1, player2)

for itr in range(iterations):
    choice_player1 = player1.play(game.seq1, game.seq2)
    choice_player2 = player2.play(game.seq2, game.seq1)
    print("Round", itr + 1, ":", choice_player1, "-", choice_player2)
    game.play(choice_player1, choice_player2)

print("Done")
print("Player#1 win rate: ", str(game.p1_win_rate()) + '%')
print("Player#2 win rate: ", str(game.p2_win_rate()) + '%')
print("DRAW rate: ", str(game.draw_rate()) + '%')
game.plot_result()




