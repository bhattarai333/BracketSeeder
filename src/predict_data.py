import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from itertools import permutations

def calculate_player_permutations(entrants):
    perm_iter = permutations(entrants, 2)
    perm = []
    for element in perm_iter:
        p1 = element[0]
        p2 = element[1]
        if p1 == p2:
            continue
        perm.append(element)
    return perm

def get_relevant_data(perm, df):
    relevant_data = df.loc[perm]         #only works if df was not read from file
    relevant_data = relevant_data.drop(columns=["H2H Set Count"])
    relevant_data = relevant_data.replace([np.inf, -np.inf], np.nan)
    relevant_data = relevant_data.fillna(0)
    return relevant_data

def start_prediction(model, entrants, df):
    permutations = calculate_player_permutations(entrants)
    relevant_data = get_relevant_data(permutations, df)
    print("Predicting Seeding")
    prediction = model.predict(relevant_data)
    relevant_data["Prediction"] = prediction
    relevant_data.index = pd.MultiIndex.from_tuples(relevant_data.index)
    left_values = relevant_data["Prediction"].groupby(level=0).mean()
    right_values = relevant_data["Prediction"].groupby(level=1).mean()
    values = left_values - right_values
    #values[0] = left_values[0]
    #values[-1] = right_values[-1]
    values = values.sort_values(ascending=False)
    print(values)
    return values.index.tolist()
