class Bracket:
    participants = []
    info_json = ""
    isSmashGG = True

    def __init__(self, participants, info_json, isSmashGG):
        self.participants = participants
        self.info_json = info_json
        self.isSmashGG = isSmashGG

    def get_standings(self):
        return self.participants

    def get_info(self):
        return self.info_json