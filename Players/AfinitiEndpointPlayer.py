from Players.Player import Player
import requests


class AfinitiEndpointPlayer(Player):
    def play(self, your_seq, opp_seq):
        response = requests.get('https://smartplay.afiniti.com/v1/play/' + str(opp_seq))
        return response.json()['nextBestMove']
