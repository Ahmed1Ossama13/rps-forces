from Players.Player import Player
import random

class RandomPlayer(Player):
    def play(self, your_seq, opp_seq):
        return random.choice("RPS")
