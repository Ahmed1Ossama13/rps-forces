from Players.Player import Player
import random
import RPS_utils


class PatternPlayer(Player):
    def play(self, your_seq, opp_seq):
        if len(your_seq) == 0: return random.choice("RPS")
        return RPS_utils.beater(your_seq[-1])
