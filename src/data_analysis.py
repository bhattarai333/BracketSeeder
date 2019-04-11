from src.set import Set as smash_set
from src.bracket import Bracket
from src.series import Series

import os
import math
from itertools import permutations
import pandas as pd
import numpy as np
import pickle
import sklearn

def nPr(n, r):
    f = math.factorial
    return f(n) // f(n - r)


def get_permutations(all_entrants):
    #3704
    length = len(all_entrants)
    val = nPr(length, 2)
    print("Calculating Permutations nPr(%s, 2): %s" % (length, val))
    perm_iter = permutations(all_entrants, 2)

    print("Removing Reversed Duplicates from Permutations %s/2" % val)

    perm = []
    for element in perm_iter:
        if element[0] > element[1]:
            perm.append(element)
    return perm

def construct_dataframe(permutations, series_set):
    df = pd.DataFrame(pd.np.empty((0, 9)))
    df.columns = ["Players", "H2H Set Count", "Avg Seeding Disparity", "Avg Placing Disparity", "Avg Seed Disparity Ratio", "Avg Loss Ratio", "Avg Win Ratio", "Avg Winning Seed Disparity Ratio", "Avg Losing Seed Disparity Ratio"]
    df["Players"] = permutations


    print(df)

def create_full_list(series_set):
    all_entrants = []
    for series in series_set:
        all_entrants += series.full_entrants_list
    all_entrants = list(set(all_entrants))
    all_entrants.sort()
    return all_entrants


def analyze_data(series_set):
    all_entrants = create_full_list(series_set)

    permutation_path = "./resources/permutations.pickle"
    exists = os.path.isfile(permutation_path)
    if exists:
        with open(permutation_path, 'rb') as f:
            perm = pickle.load(f)
    else:
        perm = get_permutations(all_entrants)
        with open(permutation_path, 'wb') as f:
            pickle.dump(perm, f)


    construct_dataframe(perm, series_set)
    return series_set  #delete this