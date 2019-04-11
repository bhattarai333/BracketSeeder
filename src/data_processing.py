import src.bracket as bracket
import src.set as smash_set

import pysmash
import re


def get_union(path):
    u = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip().lower()
            parts = line.split(',')
            u[parts[0]] = parts[1]
    return u

def process_name(name):
    if '|' in name:
        parts = name.rpartition('|')
        name = parts[-1]

    if '*' in name:
        name = name.replace('*', '')

    if '-' in name:
        name = name.replace('-', '')

    if '_' in name:
        name = name.replace('_', '')

    if '~' in name:
        name = name.replace('~', '')

    if '(' in name and ')' in name:
        name = re.sub(r" ?\([^)]+\)", "", name)

    if '\'' in name:
        name = name.replace('\'', '')

    name = name.strip().lower()

    if name in union:
        new_name = union[name]
        name = new_name

    return name.strip().lower()

def instantiate_head_to_head(names):
    h2h = {}
    for name in names:
        tup = ([], [])
        h2h[name] = tup
    return h2h

def add_head_to_head(head_to_head, winner_name, loser_name, s):
    head_to_head[winner_name][0].append(s)
    head_to_head[loser_name][1].append(s)

def get_score_from_match(match):
    entrant_1_score = match["entrant_1_score"]
    entrant_2_score = match["entrant_2_score"]
    score = str(entrant_1_score) + '-' + str(entrant_2_score)
    return score

def process_smash(smashgg, key):
    bracket_IDs = smashgg["bracket_ids"]
    players = []
    IDs = {}
    for bracket_ID in bracket_IDs:
        players_json = smash.bracket_show_players(bracket_ID)  #bad practice, collecting data in data_processing
        ind_players = []
        for player in players_json:
            player_data = []
            name = process_name(player["tag"])
            placing = player["final_placement"]
            try:
                seed_distance = player["seed"] - placing
            except TypeError:
                seed_distance = 0
            ID = player["entrant_id"]
            IDs[str(ID)] = name

            player_data.append(placing)
            player_data.append(name)
            player_data.append(seed_distance)
            ind_players.append(player_data)
        players += ind_players

    players = sorted(players, key=lambda x: x[0])

    names = [row[1] for row in players]
    head_to_head = instantiate_head_to_head(names)


    for bracket_ID in bracket_IDs:
        matches = smash.bracket_show_sets(bracket_ID)  #bad practice, collecting data in data_processing
        for match in matches:
            try:
                winner_ID = match["winner_id"]
                winner_name = IDs[winner_ID]
                loser_ID = match["loser_id"]
                loser_name = IDs[loser_ID]
                score = get_score_from_match(match)
                s = smash_set.Set(winner_name, loser_name, score)
                add_head_to_head(head_to_head, winner_name, loser_name, s)
            except KeyError:
                continue

    b = bracket.Bracket(players, smashgg, head_to_head, 1)
    return b

def process_smash_list(smash_info, key):
    smash_brackets = []
    for smashgg in smash_info:
        result = process_smash(smashgg, key)
        smash_brackets.append(result)
    return smash_brackets





def process_challonge(challonge):
    participants = challonge["tournament"]["participants"]
    players = []
    IDs = {}
    for participant in participants:
        participant = participant["participant"]
        player_data = []
        name = process_name(participant["display_name"])
        placing = participant["final_rank"]
        try:
            seed_distance = participant["seed"] - placing
        except TypeError:
            seed_distance = 0
        ID = participant["id"]
        IDs[ID] = name


        player_data.append(placing)
        player_data.append(name)
        player_data.append(seed_distance)
        players.append(player_data)
    players = sorted(players, key=lambda x: x[0])

    names = [row[1] for row in players]
    head_to_head = instantiate_head_to_head(names)




    matches = challonge["tournament"]["matches"]
    for match in matches:
        match = match["match"]
        winner_ID = match["winner_id"]
        winner_name = IDs[winner_ID]
        loser_ID = match["loser_id"]
        loser_name = IDs[loser_ID]
        score = match["scores_csv"]
        s = smash_set.Set(winner_name, loser_name, score)
        add_head_to_head(head_to_head, winner_name, loser_name, s)

    b = bracket.Bracket(players, challonge, head_to_head, 0)
    return b

def process_challonge_list(challonge_info):
    challonge_brackets = []
    for challonge in challonge_info:
        result = process_challonge(challonge)
        challonge_brackets.append(result)
    return challonge_brackets

def process_data(d, smashkey):
    print("Starting Data Processing")
    challonge_info = d[0]
    smash_info = d[1]
    challonge_brackets = process_challonge_list(challonge_info)
    smash_brackets = process_smash_list(smash_info, smashkey)


    return challonge_brackets + smash_brackets


smash = pysmash.SmashGG()  #bad practice, global variables
union = get_union("./resources/union.txt")