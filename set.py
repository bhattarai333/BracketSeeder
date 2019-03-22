class Set:
    winner = ""
    loser = ""
    score = ""

    def __init__(self, winner, loser, score):
        self.winner = winner
        self.loser = loser
        self.score = score

    def get_winner(self):
        return self.winner
    def get_loser(self):
        return self.loser
    def get_score(self):
        return self.score