import requests
import pysmash
import json
import pandas as pd



import src.bracket as bracket
import src.set as smash_set

smash = pysmash.SmashGG()
game = "smash-ultimate-singles"

def get_API_keys():
    """
    Sample apikey.txt:

    {
        "smash.gg": "token",
        "challonge": "key"
    }
    """

    with open("apikey.txt", 'r') as f:
        json_keys = json.loads(f.read())
    challonge_key = json_keys["challonge"]
    smash_key = json_keys["smash.gg"]
    return challonge_key, smash_key

def get_urls(tournament_file_path):
    """
    Sample tournaments.txt:

    https://spartanweeklies.challonge.com/sw40
    https://smash.gg/tournament/spartan-weeklies-41/details
    https://smash.gg/tournament/spartan-weeklies-42/details
    """

    output = []
    with open(tournament_file_path, 'r') as f:
        for line in f:
            u = line.strip()
            output.append(u)
    return output

def determine_website(url):
    if "challonge" in url:
        return 0
    else:
        return 1

def separate_websites(tournament_url_list):
    challonge_list = []
    smash_list = []
    for url in tournament_url_list:
        ruling = determine_website(url)
        if ruling:
            smash_list.append(url)
        else:
            challonge_list.append(url)
    return challonge_list, smash_list

def get_challonge_name_from_URL(url):
    parts = url.split("challonge")
    suborg = parts[0]

    subparts = parts[1].split('/')
    code = subparts[1]

    suborg = suborg.replace("www", '')
    suborg = suborg.replace("https", '')
    suborg = suborg.replace("http", '')
    suborg = suborg.replace('/', '')
    suborg = suborg.replace(':', '')
    suborg = suborg.replace('.', '')
    if len(suborg)>0:
        code = suborg + '-' + code
    return code

def get_challonge_bracket(url, key):
    tournament_name = get_challonge_name_from_URL(url)
    endpoint = "https://challonge.com/api/tournaments/%s.json?include_matches=1&include_participants=1&api_key=%s" % (tournament_name, key)
    response = requests.get(endpoint)
    json_data = json.loads(response.content.decode())
    f = open("output.txt", "w")
    f.write(json.dumps(json_data))
    return json_data

def get_challonge_brackets(urls, key):
    brackets = []
    for url in urls:
        brackets.append(get_challonge_bracket(url, key))
    return brackets

def get_code_from_URL(url):
    s = url
    start = "tournament/"
    end = "/details"
    output = s[s.find(start) + len(start):s.rfind(end)]  # find between
    return output

def get_smash_bracket(url, key):
    event_code = get_code_from_URL(url)
    info = (smash.tournament_show_with_brackets(event_code, event=game))
    return info

def get_smash_brackets(urls, key):
    brackets = []
    for url in urls:
        brackets.append(get_smash_bracket(url, key))
    return brackets

def add_head_to_head(head_to_head, winner_name, loser_name, s):
    try:
        head_to_head[winner_name][loser_name].append(s)
    except AttributeError:
        empty_list = list()
        empty_list.append(s)
        head_to_head[winner_name][loser_name] = empty_list
    return head_to_head

def process_challonge(challonge):
    participants = challonge["tournament"]["participants"]
    players = []
    IDs = {}
    for participant in participants:
        participant = participant["participant"]
        player_data = []
        name = participant["name"]
        placing = participant["final_rank"]
        seed_distance = participant["seed"] - placing
        ID = participant["id"]
        IDs[ID] = name


        player_data.append(placing)
        player_data.append(name)
        player_data.append(seed_distance)
        players.append(player_data)
    players = sorted(players, key=lambda x: x[0])

    names = [row[1] for row in players]
    head_to_head = pd.DataFrame(index=names, columns=names)




    matches = challonge["tournament"]["matches"]
    for match in matches:
        match = match["match"]
        winner_ID = match["winner_id"]
        winner_name = IDs[winner_ID]
        loser_ID = match["loser_id"]
        loser_name = IDs[loser_ID]
        score = match["scores_csv"]
        s = smash_set.Set(winner_name, loser_name, score, )
        head_to_head = add_head_to_head(head_to_head, winner_name, loser_name, s)

    b = bracket.Bracket(players, challonge, head_to_head, 0)
    return b

def process_challonge_list(challonge_info):
    challonge_brackets = []
    for challonge in challonge_info:
        result = process_challonge(challonge)
        challonge_brackets.append(result)
    return challonge_brackets

def get_score_from_match(match):
    entrant_1_score = match["entrant_1_score"]
    entrant_2_score = match["entrant_2_score"]
    score = entrant_1_score + '-' + entrant_2_score
    return score


def process_smash(smashgg, key):
    endpoint = "https://api.smash.gg/gql/alpha"
    tournament_ID = smashgg["tournament_id"]
    bracket_IDs = smashgg["bracket_ids"]
    bracket_IDs = bracket_IDs[:-1]
    players = []
    IDs = {}
    for bracket_ID in bracket_IDs:
        players_json = smash.bracket_show_players(bracket_ID)
        ind_players = []
        for player in players_json:
            player_data = []
            name = player["tag"]
            placing = player["final_placement"]
            seed_distance = player["seed"] - placing
            ID = player["entrant_id"]
            IDs[ID] = name

            player_data.append(placing)
            player_data.append(name)
            player_data.append(seed_distance)
            ind_players.append(player_data)
        players += ind_players

    players = sorted(players, key=lambda x: x[0])

    names = [row[1] for row in players]
    head_to_head = pd.DataFrame(index=names, columns=names)

    for bracket_ID in bracket_IDs:
        matches = smash.bracket_show_sets(bracket_ID)
        for match in matches:
            try:
                winner_ID = match["winner_id"]
                winner_name = IDs[winner_ID]
                loser_ID = match["loser_id"]
                loser_name = IDs[loser_ID]
                score = get_score_from_match(match)
                s = smash_set.Set(winner_name, loser_name, score, )
                head_to_head = add_head_to_head(head_to_head, winner_name, loser_name, s)
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

def collect_data(api_keys):
    challonge_key = api_keys[0]
    smash_key = api_keys[1]

    urls = get_urls("tournaments.txt")
    separated_urls = separate_websites(urls)
    challonge_url_list = separated_urls[0]
    smash_url_list = separated_urls[1]
    challonge_brackets = get_challonge_brackets(challonge_url_list, challonge_key)
    smash_brackets = get_smash_brackets(smash_url_list, smash_key)
    f = open("output.txt", "w")
    f.write(json.dumps(smash_brackets[0]))
    return challonge_brackets, smash_brackets

def process_data(d, smashkey):
    challonge_info = d[0]
    smash_info = d[1]

    challonge_brackets = process_challonge_list(challonge_info)
    smash_brackets = process_smash_list(smash_info, smashkey)


    return challonge_brackets + smash_brackets

def analyze_data(brackets):
    return brackets

def predict(m):
    return m

def write_to_file(prediction):
    pass

print("Starting Data Collection")
keys = get_API_keys()
data = collect_data(keys)
print("Starting Data Processing")
data = process_data(data, keys[1])
print("Starting Data Analysis")
model = analyze_data(data)

prediction = predict(model)
write_to_file(prediction)
