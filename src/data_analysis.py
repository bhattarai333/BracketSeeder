from src.set import Set as smash_set
from src.bracket import Bracket
from src.series import Series

import os
import math
from itertools import permutations
import copy
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
    return perm_iter

def common_tournament(element, series_set):
    p1 = element[0]
    p2 = element[1]
    common_series = []
    for s in series_set:
        series_entrants = s.full_entrants_list
        if not (p1 in series_entrants and p2 in series_entrants):
            continue
        common_series.append(s)

    common_series.sort(key=lambda Series: Series.unique_entrants_num)
    for s in common_series:
        for bracket in s.brackets:
            names = bracket.names_list
            if p1 in names:
                if p2 in names:
                    #print("ADDED")
                    return True
    #print("REMOVED")
    return False
def merge_dataframes(df, full_df):

    return df #delete this

def combine_dataframes(all_df):
    full_df = pd.DataFrame()
    for df in all_df:
        full_df = merge_dataframes(df, full_df)
    return full_df

def construct_dataframe_from_iter(series_set):

    print("Creating DataFrame")
    all_df = []
    for ser in series_set:
        for bracket in ser.brackets:
            print(len(bracket.analysis_features))
            print(len(bracket.head_to_head))
            df = pd.DataFrame.from_dict(bracket.analysis_features, orient='index')
            df.columns = ["H2H Set Count", "H2H Games", "Avg Win Ratio", "Avg Loss Ratio", "Avg Seeding Difference", "Avg Placing Difference", "Avg Seed Disparity Ratio", "Avg Winning Seed Disparity Ratio", "Avg Losing Seed Disparity Ratio"]
            all_df.append(df)

    df = combine_dataframes(all_df)

    df.to_excel("./resources/df.xlsx")
    return df


def create_full_list(series_set):
    all_entrants = []
    for series in series_set:
        all_entrants += series.full_entrants_list
    all_entrants = list(set(all_entrants))
    all_entrants.sort()
    return all_entrants


def analyze_data(series_set):
    #all_entrants = create_full_list(series_set)
    #perm_iter = get_permutations(all_entrants)

    df = construct_dataframe_from_iter(series_set)
    #print(df)
    #dataframe_path = "./resources/dataframe.pd"
    #exists = os.path.isfile(dataframe_path_path)
    #if exists:
    #    with open(dataframe_path_path, 'rb') as f:
    #        df = pickle.load(f)
    #else:
    #    df = construct_dataframe_from_iter(perm_iter, series_set)
    #    with open(dataframe_path_path, 'wb') as f:
    #        pickle.dump(perm, f)
    return series_set  #delete this