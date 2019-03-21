import requests
import pysmash
import json
import bracket
smash = pysmash.SmashGG()

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
    info = (smash.tournament_show(event_code))
    return info

def get_smash_brackets(urls, key):
    brackets = []
    for url in urls:
        brackets.append(get_smash_bracket(url, key))
    return brackets

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

def process_challonge(challonge):
    participants = challonge["tournament"]["participants"]
    players = []
    for participant in participants:
        participant = participant["participant"]
        player_data = []
        name = participant["name"]
        placing = participant["final_rank"]
        seed_distance = participant["seed"] - placing

        player_data.append(placing)
        player_data.append(name)
        player_data.append(seed_distance)
        players.append(player_data)
    players = sorted(players, key=lambda x: x[0])

    b = bracket.Bracket(players, challonge, 0)
    return b

def process_challonge_list(challonge_info):
    challonge_brackets = []
    for challonge in challonge_info:
        result = process_challonge(challonge)
        challonge_brackets.append(result)
    return challonge_brackets

def process_smash(smashgg):
    return smashgg

def process_smash_list(smash_info):
    smash_brackets = []
    for smashgg in smash_info:
        result = process_smash(smashgg)
        smash_brackets.append(result)
    return smash_brackets

def process_data(d):
    challonge_info = d[0]
    smash_info = d[1]

    challonge_brackets = process_challonge_list(challonge_info)
    smash_brackets = process_smash_list(smash_info)


    return d #delete this

def analyze_data():
    return "To Do"

def predict(m):
    return m

def write_to_file(prediction):
    pass

keys = get_API_keys()
data = collect_data(keys)
data = process_data(data)
model = analyze_data()

prediction = predict(model)
write_to_file(prediction)