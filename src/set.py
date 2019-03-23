class Set:
    winner = ""
    loser = ""
    score = ""

    def __init__(self, winner, loser, score):
        self.winner = winner
        self.loser = loser
        self.score = self.process_score(score)

    @staticmethod
    def process_score(score):
        parts = score.split('-')
        if parts[0] > parts[1]:
            return score
        else:
            return parts[1] + '-' + parts[0]

    def __str__(self):
        return "%s %s %s" % (self.winner, self.score, self.loser)
    @staticmethod
    def get_winner(self):
        return self.winner
    @staticmethod
    def get_loser(self):
        return self.loser
    @staticmethod
    def get_score(self):
        return self.score
