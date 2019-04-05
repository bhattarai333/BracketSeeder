import pandas as pd

class Bracket:
    entrant_numbers = 0
    participants = []
    head_to_head = pd.DataFrame
    info_json = ""
    isSmashGG = True

    def __init__(self, participants, info_json, head_to_head, isSmashGG):
        self.participants = participants
        self.info_json = info_json
        self.head_to_head = head_to_head
        self.isSmashGG = isSmashGG
        self.entrant_numbers = len(participants)

    def __str__(self):
        return "%s %s %s" % (self.entrant_numbers, self.participants[0][0], self.isSmashGG)

    def get_standings(self):
        return self.participants

    def get_info(self):
        return self.info_json
