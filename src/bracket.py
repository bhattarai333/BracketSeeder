#import numpy as np

class Bracket:
    participants = []
    head_to_head = {}
    info_json = ""
    isSmashGG = True

    def __init__(self, participants, info_json, head_to_head, isSmashGG):
        self.participants = participants
        self.info_json = info_json
        self.head_to_head = head_to_head
        self.isSmashGG = isSmashGG

    def get_standings(self):
        return self.participants

    def get_info(self):
        return self.info_json
