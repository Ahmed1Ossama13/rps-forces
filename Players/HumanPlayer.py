from Players.Player import Player
import RPS_utils, random

class HumanPlayer(Player):
    def play(self, your_seq, opp_seq):
        return 'R'
        # if len(your_seq) == 0: return random.choice('RPS')
        # last_outcome = RPS_utils.outcome(your_seq[-1], opp_seq[-1])
        # if last_outcome == 'W':
        #     return your_seq[-1]
        # elif last_outcome == 'L':
        #     return RPS_utils.beater(opp_seq[-1])
        # else:
        #     return random.choice('RPS')
