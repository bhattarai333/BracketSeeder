from itertools import permutations
import pandas as pd
import numpy as np

class Bracket:

    def __init__(self, participants, info_json, head_to_head, isSmashGG):
        self.entrants_list = participants
        self.info_json = info_json
        self.head_to_head = head_to_head
        self.isSmashGG = isSmashGG
        self.entrants_num = len(participants)
        self.names_list = [row[1] for row in self.entrants_list]
        self.player_info = self.set_player_info()
        self.analysis_features = self.set_features()

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
        p = self.calculate_player_permutations()
        features = {}
        for perm in p:#
            data = self.calculate_features(perm)
            features[perm] = data
        return features

    def set_player_info(self):
        d = {}
        for entrant in self.entrants_list:
            d[entrant[1]] = entrant[0], entrant[0] + entrant[2]
        return d

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
        win_loss_ratio = self.get_win_loss_ratio(players)
        features.append(win_loss_ratio[0])
        features.append(win_loss_ratio[1])
        #self.analysis_features[players] = features
        return features

    def get_win_loss_ratio(self, players):
        p1 = players[0]
        p2 = players[1]
        h2h_p1 = self.head_to_head[p1]
        h2h_p2 = self.head_to_head[p2]

        p1_wins = h2h_p1[0]
        p1_losses = h2h_p1[1]

        p2_wins = h2h_p2[0]
        p2_losses = h2h_p2[1]

        p1_win_seeds = []
        p1_loss_seeds = []

        for win in p1_wins:
            other_player = win.loser
            other_player_info = self.player_info[other_player]
            p1_win_seeds.append(other_player_info[1])

        for loss in p1_losses:
            other_player = loss.winner
            other_player_info = self.player_info[other_player]
            p1_loss_seeds.append(other_player_info[1])

        p2_win_seeds = []
        p2_loss_seeds = []

        for win in p2_wins:
            other_player = win.loser
            other_player_info = self.player_info[other_player]
            p2_win_seeds.append(other_player_info[1])

        for loss in p2_losses:
            other_player = loss.winner
            other_player_info = self.player_info[other_player]
            p2_loss_seeds.append(other_player_info[1])

        p1_win_sum = sum(p1_win_seeds)
        p1_win_len = len(p1_win_seeds)

        p1_win_ratio = 0
        if p1_win_len != 0:
            p1_win_ratio = float(p1_win_sum/p1_win_len)

        p2_win_sum = sum(p2_win_seeds)
        p2_win_len = len(p2_win_seeds)

        p2_win_ratio = 0
        if p2_win_len != 0:
            p2_win_ratio = float(p2_win_sum/p2_win_len)


        p1_loss_sum = sum(p1_loss_seeds)
        p1_loss_len = len(p1_loss_seeds)

        p1_loss_ratio = 0
        if p1_loss_len != 0:
            p1_loss_ratio = float(p1_loss_sum/p1_loss_len)

        p2_loss_sum = sum(p2_loss_seeds)
        p2_loss_len = len(p2_loss_seeds)

        p2_loss_ratio = 0
        if p2_loss_len != 0:
            p2_loss_ratio = float(p2_loss_sum / p2_loss_len)

        #winning_ratio = 0
        #if p2_win_ratio != 0:
        #    winning_ratio = p1_win_ratio/p2_win_ratio
        #losing_ratio = 0
        #if p2_loss_ratio !=0:
        #    losing_ratio = p1_loss_ratio/p2_loss_ratio
        return (p1_win_ratio, p2_win_ratio), (p1_loss_ratio, p2_loss_ratio)

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
        return abs(p1_seed - p2_seed), abs(p1_placement - p2_placement), (p1_seed - p1_placement, p2_seed - p2_placement)


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
                    if parts[0] == 'None':
                        p1_score = 0
                    else:
                        p1_score = int(parts[0])
                    if parts[1] == 'None':
                        p2_score = 0
                    else:
                        p2_score = int(parts[1])
                    p1_games += int(p1_score)
                    p2_games += int(p2_score)
        if loss_len > 0:
            for loss in losses:
                if loss.winner == p2:
                    loss_count += 1
                    score = loss.score
                    parts = score.split('~')
                    p1_games += int(parts[1])
                    p2_games += int(parts[0])




        h2h_data2 = self.head_to_head[p2]
        wins2 = h2h_data2[0]
        losses2 = h2h_data2[1]

        win_len2 = len(wins2)
        loss_len2 = len(losses2)

        #if win_len2 == 0:
        #    win_ratio = 0
        #else:
        #    win_ratio = float(win_len / win_len2)

        #if loss_len2 == 0:
        #    loss_ratio = 0
        #else:
        #    loss_ratio = float(loss_len / loss_len2)



        return (win_count, loss_count), (p1_games, p2_games), (win_len, win_len2), (loss_len, loss_len2)


    def calculate_player_permutations(self):
        perm_iter = permutations(self.names_list, 2)
        perm = []
        for element in perm_iter:
            p1 = element[0]
            p2 = element[1]
            if p1 >= p2:
                continue
            perm.append(element)
        return perm
