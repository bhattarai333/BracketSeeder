import requests
import graphene

def get_urls(tournament_file_path):
    output = list()
    with open(tournament_file_path, 'r') as f:
        for line in f:
            u = line.strip()
            output.append(u)
    return output

urls = get_urls("tournaments.txt")
