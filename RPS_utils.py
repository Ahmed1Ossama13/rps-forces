def beater(c):
    return {
        'R': 'P',
        'P': 'S',
        'S': 'R'
    }[c]


def loser(c):
    return beater(beater(c))


def outcome(p1, p2):
    if (p1 == p2):
        return 'D'
    if loser(p1) == p2: return 'W'
    return 'L'

def other(c):
    return beater(c) + loser(c)

def pick_if_eliminated(c):
    if c == 'R':
        return 'S'
    if c == 'P':
        return 'R'
    return 'P'

def pick_most_common_move(seq):
    h = {
        'R': 0,
        'P': 0,
        'S': 0
    }
    for item in seq:
        h[item] += 1
    M = []
    for item in h:
        M.append((h[item], item))
    M.sort()
    return M[-1][-1]

