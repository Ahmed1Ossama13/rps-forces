from __future__ import division
import random
import itertools
from Players import Player


class MarkovChainPlayer(Player.Player):
    beat = {'R': 'P', 'P': 'S', 'S': 'R'}


    class MarkovChain():

        def __init__(self, type, beat, level, memory, score=0, score_mem=0.9):
            self.type = type
            self.matrix = self.create_matrix(beat, level, memory)
            self.memory = memory
            self.level = level
            self.beat = beat
            self.score = score
            self.score_mem = score_mem
            self.prediction = ''
            self.name = 'level: {}, memory: {}'.format(self.level, self.memory)
            self.last_updated_key = ''

        def create_matrix(self, beat, level, memory):
            def create_keys(beat, level):
                keys = list(beat)
                if level > 1:
                    for i in range(level - 1):
                        key_len = len(keys)
                        for i in itertools.product(keys, ''.join(beat)):
                            keys.append(''.join(i))
                        keys = keys[key_len:]

                return keys

            keys = create_keys(beat, level)

            matrix = {}
            for key in keys:
                matrix[key] = {'R': 1 / (1 - memory) / 3,
                               'P': 1 / (1 - memory) / 3,
                               'S': 1 / (1 - memory) / 3}

            return matrix

        def update_matrix(self, key_lagged, response):

            for key in self.matrix[key_lagged]:
                self.matrix[key_lagged][key] = self.memory * self.matrix[key_lagged][key]

            self.matrix[key_lagged][response] += 1
            self.last_updated_key = key_lagged

        def update_score(self, inp, out):

            if self.beat[out] == inp:
                self.score = self.score * self.score_mem - 1
            elif out == inp:
                self.score = self.score * self.score_mem
            else:
                self.score = self.score * self.score_mem + 1

        def predict(self, key_current):

            probs = self.matrix[key_current]

            if max(probs.values()) == min(probs.values()):
                self.prediction = random.choice(list(self.beat.keys()))
            else:
                self.prediction = max([(i[1], i[0]) for i in probs.items()])[1]

            if self.type == 'input_oriented':
                return self.prediction
            elif self.type == 'output_oriented':
                return self.beat[self.prediction]

    class Ensembler():
        def __init__(self, type, beat, min_score=-10, score=0, score_mem=0.9):
            self.type = type
            self.matrix = {i: 0 for i in beat}
            self.beat = beat
            self.min_score = min_score
            self.score = score
            self.score_mem = score_mem
            self.prediction = ''

        def update_score(self, inp, out):

            if self.beat[out] == inp:
                self.score = self.score * self.score_mem - 1
            elif out == inp:
                self.score = self.score * self.score_mem
            else:
                self.score = self.score * self.score_mem + 1

        def update_matrix(self, pred_dict, pred_score):
            norm_dict = {key: pred_dict[key] / sum(pred_dict.values()) for key in pred_dict}
            for key in self.matrix:
                if pred_score >= self.min_score:
                    self.matrix[key] = self.matrix[key] + pred_score * norm_dict[key]

        def predict(self):

            if max(self.matrix.values()) == min(self.matrix.values()):
                self.prediction = random.choice(list(self.beat.keys()))
            else:
                self.prediction = max([(i[1], i[0]) for i in self.matrix.items()])[1]

            return self.prediction

    class HistoryColl():
        def __init__(self):
            self.history = ''

        def hist_collector(self, inp, out):
            self.history = self.history + inp
            self.history = self.history + out
            if len(self.history) > 10:
                self.history = self.history[-10:]

        def create_keys(self, level):
            return self.history[-level:]

        def create_keys_hist(self, level):
            key_hist = self.history[-level - 2:-2]
            inp_latest = self.history[-2]
            out_latest = self.history[-1]
            return key_hist, inp_latest, out_latest

    def solve(self, input):
        print(input, self.beat)
        if input == '':
            self.output = random.choice(list(self.beat.keys()))
            self.history = self.HistoryColl()

            self.memory = [0.5, 0.6, 0.7, 0.8, 0.9, 0.93, 0.95, 0.97, 0.99]
            self.level = [1, 2, 3, 4]
            self.ensemble_min_score = [5]

            self.models_inp = [self.MarkovChain('input_oriented', self.beat, i[0], i[1]) for i in itertools.product(self.level, self.memory)]
            self.models_out = [self.MarkovChain('output_oriented', self.beat, i[0], i[1]) for i in itertools.product(self.level, self.memory)]
            self.models_ens = [self.Ensembler('ensemble', self.beat, i) for i in self.ensemble_min_score]

            self.models = self.models_inp + self.models_out + self.models_ens

        elif len(self.history.history) == 10:

            self.history.hist_collector(input, self.output)

            max_score = 0

            for model in self.models:

                if model.type in ('input_oriented', 'output_oriented'):
                    key_hist, inp_latest, out_latest = self.history.create_keys_hist(model.level)
                    key_curr = self.history.create_keys(model.level)

                if model.prediction != '':
                    model.update_score(input, self.beat[model.prediction])

                if model.type == 'input_oriented':
                    model.update_matrix(key_hist, inp_latest)

                elif model.type == 'output_oriented':
                    model.update_matrix(key_hist, out_latest)

                elif model.type == 'ensemble':
                    for mod in self.models:
                        if mod.type in ('input_oriented', 'output_oriented'):
                            model.update_matrix(mod.matrix[mod.last_updated_key], model.score)

                if model.type in ('input_oriented', 'output_oriented'):
                    predicted_input = model.predict(key_curr)
                elif model.type == 'ensemble':
                    predicted_input = model.predict()

                if model.score > max_score:
                    max_score = model.score
                    self.output = self.beat[predicted_input]

            if max_score < 1:
                self.output = random.choice(list(self.beat.keys()))

        else:
            self.history.hist_collector(input, self.output)
            self.output = random.choice(list(self.beat.keys()))
        return self.output

    def play(self, your_seq, opp_seq):
        return self.solve(opp_seq[-1 : ])