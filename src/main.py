import src.data_collection as data_collection
import src.data_processing as process
import src.data_analysis as analysis
import src.predict_data as predict
from src.series import Series

import os
import ast
import pandas as pd

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

def get_entrants(path):
    """
    Example entrants.txt:
    gomakenpi
    nebula
    nom
    dylster
    j3
    ...
    """
    entrants = []
    with open(path, 'r') as f:
        for line in f:
            entrants.append(line.strip())
    return entrants

def write_prediction(pred, path):
    with open(path, 'w') as f:
        i = 0
        for line in pred:
            i += 1
            content = str(i) + ". " + line + '\n'
            f.write(content)


tournament_path = "./resources/tournaments.txt"
dataframe_path = "./resources/df.xlsx"
entrants_path = "./resources/entrants.txt"
prediction_path = "./resources/prediction.txt"

exists = os.path.isfile(dataframe_path)


all_series = []
weeklies = get_urls(tournament_path)
for weekly in weeklies:
    print(weekly)  # Series name
    ser = Series(weekly, data_collection.get_data(weeklies[weekly]))
    all_series.append(ser)
print("Starting Data Processing")
df = process.process_data(all_series)
print(df.shape)
df.to_excel(dataframe_path)
print("Starting Data Analysis")
model = analysis.start_analysis(df)
entrants = get_entrants(entrants_path)
prediction = predict.start_prediction(model, entrants, df)
print("Writing Prediction to File")
write_prediction(prediction, prediction_path)


