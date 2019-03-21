class Bracket:
    standings = {}
    info_json = ""

    def __init__(self, standings, info_json):
        self.standings = standings
        self.info_json = info_json

    def get_standings(self):
        return self.standings

    def get_info(self):
        return self.info_json