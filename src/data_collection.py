import src.data_preprocessing as data_processing

import requests
import pysmash
import pysmash.exceptions as exceptions
import json


def get_API_keys(path):
    """
    Sample apikey.txt:

    {
        "smash.gg": "token",
        "challonge": "key"
    }
    """

    with open(path, 'r') as f:
        json_keys = json.loads(f.read())
    challonge_key = json_keys["challonge"]
    smash_key = json_keys["smash.gg"]
    return challonge_key, smash_key

def determine_website(url):
    # Determines if website is challonge or smash.gg
    if "challonge" in url:
        return 0
    else:
        return 1

def separate_websites(tournament_url_list):
    # Separate list of all URLs into two separate lists for each website
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
    """
    Gets the bracket name from a url, for example:
    https://challonge.com/cmpg100
    returns: cmpg100
    https://spartanweeklies.challonge.com/sw40
    returns: spartanweeklies-sw40
    """

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
    """
    Gets the JSON information from challonge
    :param url: challonge URL
    :param key: challonge API key
    :return: full JSON data of bracket
    """
    tournament_name = get_challonge_name_from_URL(url)
    endpoint = "https://challonge.com/api/tournaments/%s.json?include_matches=1&include_participants=1&api_key=%s" \
               % (tournament_name, key)
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
    try:
        info = (smash.tournament_show_with_brackets(event_code, event=game))
    except exceptions.ValidationError:
        info = smash.tournament_show_with_brackets(event_code, event="ultimate-singles")
    return info

def get_smash_brackets(urls, key):
    brackets = []
    for url in urls:
        brackets.append(get_smash_bracket(url, key))
    return brackets

def collect_data(api_keys, urls):
    challonge_key = api_keys[0]
    smash_key = api_keys[1]
    separated_urls = separate_websites(urls)
    challonge_url_list = separated_urls[0]
    smash_url_list = separated_urls[1]
    #if len(challonge_url_list) > 0:
    challonge_brackets = get_challonge_brackets(challonge_url_list, challonge_key)
    #if len(smash_url_list) > 0:
    smash_brackets = get_smash_brackets(smash_url_list, smash_key)
    return challonge_brackets, smash_brackets



def get_data(urls):
    print("Starting Data Collection")
    keys = get_API_keys("./resources/apikey.txt")
    data = collect_data(keys, urls)
    data = data_processing.preprocess_data(data, keys[1])
    return data


smash = pysmash.SmashGG()  #bad practice, global variables
game = "smash-ultimate-singles"
