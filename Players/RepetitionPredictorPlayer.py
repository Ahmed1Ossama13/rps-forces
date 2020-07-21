from Players.Player import Player
import random
import RPS_utils

class RepetitionPredictorPlayer(Player):
    mem = {}
    segment_length = 3
    def play(self, your_seq, opp_seq):
        n = len(your_seq)
        if n < self.segment_length + 1:
            return random.choice('RPS')
        s = ""
        for i in range(n - self.segment_length - 1, n):
            res = RPS_utils.outcome(opp_seq[i], your_seq[i])
            s += res
            if s not in self.mem:
                self.mem[s] = [0, 0]
            did_repeat = 1 if (opp_seq[n - 2] == opp_seq[n - 1]) else 0
            self.mem[s][did_repeat] += 1
        s = s[1 : ] + RPS_utils.outcome(opp_seq[n - 1], your_seq[n - 1])
        if s in self.mem:
            will_repeat = self.mem[s][1] * 1.0 / (self.mem[s][0] + self.mem[s][1])
            if will_repeat > 0.8:
                return RPS_utils.beater(opp_seq[-1])
            else:
                return RPS_utils.pick_if_eliminated(opp_seq[-1])
        else:
            return RPS_utils.pick_if_eliminated(opp_seq[-1])
