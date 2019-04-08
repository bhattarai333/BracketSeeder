import src.data_collection as data_collection
import src.data_analysis as analysis
import src.series as series

import pickle
import os

def get_urls(tournament_file_path):
    """

    Sample tournaments.txt:
    MSU
    https://spartanweeklies.challonge.com/sw40
    https://smash.gg/tournament/spartan-weeklies-41/details
    https://smash.gg/tournament/spartan-weeklies-42/details
    ::
    UoM
    https://smash.gg/tournament/ann-arbor-arena-18/details
    https://smash.gg/tournament/ann-arbor-arena-19/details
    """

    output = {}
    with open(tournament_file_path, 'r') as f:
        weekly_series = []
        name = ""
        for line in f:
            u = line.strip()

            if name == "":
                name = u
                continue

            if u == "::":
                output[name] = weekly_series.copy()
                weekly_series.clear()
                name = ""
                continue
            if line[0] == '*':
                continue
            weekly_series.append(u)
        output[name] = weekly_series.copy()
    return output

def analyze_data(series_set):
    return series_set

def predict(m):
    return m

def write_to_file(prediction):
    pass

exists = os.path.isfile('data.pickle')

all_series = []
if exists:
    with open("data.pickle", 'rb') as f:
        all_series = pickle.load(f)
else:
    weeklies = get_urls("tournaments.txt")
    for weekly in weeklies:
        print(weekly)  # Series name
        ser = series.Series(weekly, data_collection.get_data(weeklies[weekly]))
        print(ser.full_head_to_head)
        all_series.append(ser)
    with open("data.pickle", 'wb') as f:
        pickle.dump(all_series, f)
print("Starting Data Analysis")
model = analysis.analyze_data(all_series)
prediction = predict(model)
write_to_file(prediction)


