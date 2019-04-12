from itertools import permutations
import pandas as pd
import numpy as np

class Bracket:
    entrants_num = 0
    entrants_list = []
    names_list = []
    head_to_head = {}
    isSmashGG = True
    analysis_features = {}
    info_json = ""

    def __init__(self, participants, info_json, head_to_head, isSmashGG):
        self.entrants_list = participants
        self.info_json = info_json
        self.head_to_head = head_to_head
        self.isSmashGG = isSmashGG
        self.entrants_num = len(participants)
        self.names_list = [row[1] for row in self.entrants_list]
        self.set_features()
        print(self.analysis_features)

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

    def set_features(self):
        permutations = self.calculate_player_permutations()
        for perm in permutations:
            self.calculate_features(perm)

    def calculate_features(self, players):
        features = []
        h2h = self.get_h2h(players)
        features.append(h2h[0])
        features.append(h2h[1])
        features.append(h2h[2])
        features.append(h2h[3])
        seeding_data = self.get_seed_disparity(players)
        features.append(seeding_data[0])
        features.append(seeding_data[1])
        features.append(seeding_data[2])
        self.analysis_features[players] = features
        #print(self.analysis_features)

    def get_seed_disparity(self, players):
        p1 = players[0]
        p2 = players[1]

        p1_data = None
        p2_data = None

        for person in self.entrants_list:
            if person[1] == p1:
                p1_data = person
            if person[1] == p2:
                p2_data = person

        p1_seed = p1_data[0] + p1_data[2]
        p2_seed = p2_data[0] + p2_data[2]
        p1_placement = p1_data[0]
        p2_placement = p2_data[0]
        return abs(p1_seed - p2_seed), abs(p1_placement - p2_placement), float(p1_seed - p1_placement / p2_seed - p2_placement)


    def get_h2h(self, players):
        p1 = players[0]
        p2 = players[1]

        h2h_data = self.head_to_head[p1]
        wins = h2h_data[0]
        losses = h2h_data[1]

        win_count = 0
        loss_count = 0

        p1_games = 0
        p2_games = 0

        win_len = len(wins)
        loss_len = len(losses)

        if win_len > 0:
            for win in wins:
                if win.loser == p2:
                    win_count += 1
                    score = win.score
                    parts = score.split('~')
                    p1_games += int(parts[0])
                    #print(score)
                    p2_games += int(parts[1])
        if loss_len > 0:
            for loss in losses:
                if loss.winner == p2:
                    loss_count += 1
                    score = loss.score
                    parts = score.split('~')
                    p1_games += int(parts[1])
                    p2_games += int(parts[0])




        h2h_data2 = self.head_to_head[p1]
        wins2 = h2h_data2[0]
        losses2 = h2h_data2[1]

        win_len2 = len(wins2)
        loss_len2 = len(losses2)

        if win_len2 == 0:
            win_ratio = 0
        else:
            win_ratio = float(win_len / win_len2)

        if loss_len2 == 0:
            loss_ratio = 0
        else:
            loss_ratio = float(loss_len / loss_len2)



        return (win_count, loss_count), (p1_games, p2_games), win_ratio, loss_ratio


    def calculate_player_permutations(self):
        perm_iter = permutations(self.names_list, 2)
        perm = []
        for element in perm_iter:
            p1 = element[0]
            p2 = element[1]
            if p1 > p2:
                continue
            perm.append(element)
        return perm
