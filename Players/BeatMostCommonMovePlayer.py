from Players.Player import Player
import RPS_utils

class BeatMostCommonMovePlayer(Player):
    def play(self, your_seq, opp_seq):
        return RPS_utils.beater(RPS_utils.pick_most_common_move(opp_seq))
