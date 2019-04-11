class Bracket:
    entrants_num = 0
    entrants_list = []
    head_to_head = {}
    info_json = ""
    isSmashGG = True

    def __init__(self, participants, info_json, head_to_head, isSmashGG):
        self.entrants_list = participants
        self.info_json = info_json
        self.head_to_head = head_to_head
        self.isSmashGG = isSmashGG
        self.entrants_num = len(participants)

    def __str__(self):
        if self.isSmashGG:
            s = "smash.gg"
        else:
            s = "challonge"
        return "%s entrants, %s(W), %s" % (self.entrants_num, self.entrants_list[0][1], s)

    def __repr__(self):
        return self.__str__()

    def get_standings(self):
        return self.entrants_list

    def get_info(self):
        return self.info_json
