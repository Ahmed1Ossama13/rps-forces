import RPS_utils
import matplotlib.pyplot as plt


class Game:
    def __init__(self, player1, player2):
        self.seq1 = ""
        self.seq2 = ""
        self.player1 = player1
        self.player2 = player2
        self.rounds = 0

    def play(self, choice1, choice2):
        self.seq1 += choice1
        self.seq2 += choice2
        self.rounds += 1

    def p1_win_rate(self):
        w = 0
        for i in range(self.rounds):
            if RPS_utils.outcome(self.seq1[i], self.seq2[i]) == 'W':
                w += 1
        return round(w * 100.0 / self.rounds, 2)

    def p2_win_rate(self):
        w = 0
        for i in range(self.rounds):
            if RPS_utils.outcome(self.seq2[i], self.seq1[i]) == 'W':
                w += 1
        return round(w * 100.0 / self.rounds, 2)

    def draw_rate(self):
        w = 0
        for i in range(self.rounds):
            if RPS_utils.outcome(self.seq2[i], self.seq1[i]) == 'D':
                w += 1
        return round(w * 100.0 / self.rounds, 2)

    def plot_result(self):
        X = []
        Y1 = []
        Y2 = []
        Y3 = []
        w, l, d = 0, 0, 0
        for i in range(self.rounds):
            X.append(i + 1)
            res = RPS_utils.outcome(self.seq1[i], self.seq2[i])
            if res == 'W': w += 1
            elif res == 'L': l += 1
            else: d += 1
            Y1.append(round(w * 100.0 / (i + 1), 2))
            Y2.append(round(l * 100.0 / (i + 1), 2))
            Y3.append(round(d * 100.0 / (i + 1), 2))
        plt.plot(X, Y1, 'blue', label='P1 - ' + self.player1.name)
        plt.plot(X, Y2, 'red', label='P2 - ' + self.player2.name)
        plt.plot(X, Y3, 'black', label='Draw')
        plt.legend()
        plt.show()
