import requests, random, RPS_utils
from Players import MarkovChainPlayer, RandomPlayer, PatternPlayer
from Players import IO2LegacyPlayer, RepetitionPredictorPlayer
from Players import AfinitiEndpointPlayer, BeatMostCommonMovePlayer
from Players import HumanPlayer
from Game import Game

def pattern_player(your_seq, opp_seq):
    return ['R', 'P', 'S'][len(your_seq) % 3]


def random_player(your_seq, opp_seq):
    return ['R', 'P', 'S'][random.randint(0, 2)]


def opp_will_change_player(your_seq, opp_seq):
    if len(opp_seq) < 15:
        return ['R', 'P', 'S'][len(your_seq) % 3]
    reps = 0
    score = 0
    for i in range(-1, -11, -1):
        reps += 1 if (opp_seq[i] == opp_seq[i - 1]) else 0
        score += 1 if (RPS_utils.outcome(opp_seq[i], your_seq[i])) else 0
    if score > 3:
        return RPS_utils.pick_if_eliminated(opp_seq[-1]) if reps < 5 else RPS_utils.pick_beater(opp_seq[-1])
    else:
        return RPS_utils.pick_if_eliminated(opp_seq[-1]) if reps >= 5 else RPS_utils.pick_beater(opp_seq[-1])


def pattern_recognition_player_RPS(your_seq, opp_seq):
    n = len(your_seq)
    if n < 20:
        return random_player(your_seq, opp_seq)
    mem = {}
    len = 10
    for i in range(0, n - len + 1):
        s = ""
        for j in range(i, i + len):
            res = opp_seq[j]
            s += res
        if i + len >= n: break
        if s not in mem: mem[s] = {'R': 0, 'P': 0, 'S': 0}
        mem[s][opp_seq[i + len]] += 1

    if s in mem:
        return RPS_utils.pick_beater(RPS_utils.pick_most_common_move(mem[s]))
    else:
        return RPS_utils.pick_if_eliminated(opp_seq[-1])


def beat_common_move_player(your_seq, opp_seq):
    L = {'R': 0, 'P': 0, 'S': 0}
    for item in opp_seq:
        L[item] += 1
    M = []
    for item in L:
        M.append((L[item], item))
    M.sort()
    return RPS_utils.pick_beater(M[-1][-1])


def inverse_intuition_player(your_seq, opp_seq):
    n = len(your_seq)
    if n < 10:
        return random_player(your_seq, opp_seq)
    mem = {}
    for i in range(0, n - 4):
        s = ""
        for j in range(i, i + 5):
            res = RPS_utils.outcome(your_seq[j], opp_seq[j])
            if res == 'WIN': s += 'W'
            elif res == 'DRAW': s += 'D'
            else: s += 'L'
        if i + 5 >= n: break
        mem[s] = True if (your_seq[i + 5] == your_seq[i + 4]) else False
    if s in mem:
        return RPS_utils.pick_beater(RPS_utils.pick_beater(your_seq[-1]) if (mem[s]) else RPS_utils.pick_if_eliminated(your_seq[-1]))
    else:
        return RPS_utils.pick_beater(RPS_utils.pick_if_eliminated(your_seq[-1]))


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




