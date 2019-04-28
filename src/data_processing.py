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


def find_ratio(df, name):
    n1 = name + '1'
    n2 = name + '2'
    df[name] = df[n1] / df[n2]
    df = df.drop(columns=[n1, n2])
    return df

def handle_duplicates(df):
    df = df.groupby(df.index).agg({
        "H2H Set Count1": sum,
        "H2H Set Count2": sum,
        "H2H Games1": sum,
        "H2H Games2": sum,
        "Avg Win Ratio1": sum,
        "Avg Win Ratio2": sum,
        "Avg Loss Ratio1": sum,
        "Avg Loss Ratio2": sum,
        "Avg Seeding Difference": "mean",
        "Avg Placing Difference": "mean",
        "Avg Seed Disparity Ratio1": "mean",
        "Avg Seed Disparity Ratio2": "mean",
        "Avg Winning Seed Disparity Ratio1": "mean",
        "Avg Winning Seed Disparity Ratio2": "mean",
        "Avg Losing Seed Disparity Ratio1": "mean",
        "Avg Losing Seed Disparity Ratio2": "mean"
        # Use these metrics to predict set count
    })

    df = find_ratio(df, "H2H Set Count")
    df = find_ratio(df, "H2H Games")
    df = find_ratio(df, "Avg Win Ratio")
    df = find_ratio(df, "Avg Loss Ratio")
    df = find_ratio(df, "Avg Seed Disparity Ratio")
    df = find_ratio(df, "Avg Winning Seed Disparity Ratio")
    df = find_ratio(df, "Avg Losing Seed Disparity Ratio")
    return df

def combine_dataframes(all_df):
    full_df = pd.DataFrame()
    for df in all_df:
        full_df = pd.concat([full_df, df], join='outer')
    full_df = handle_duplicates(full_df)
    return full_df

def construct_dataframe_from_iter(series_set):

    print("Creating DataFrame")
    all_df = []
    col_names = ["H2H Set Count1", "H2H Set Count2", "H2H Games1", "H2H Games2", "Avg Win Ratio1", "Avg Win Ratio2", "Avg Loss Ratio1", "Avg Loss Ratio2", "Avg Seeding Difference", "Avg Placing Difference", "Avg Seed Disparity Ratio1", "Avg Seed Disparity Ratio2", "Avg Winning Seed Disparity Ratio1", "Avg Winning Seed Disparity Ratio2", "Avg Losing Seed Disparity Ratio1", "Avg Losing Seed Disparity Ratio2"]

    for ser in series_set:
        for bracket in ser.brackets:
            df = pd.DataFrame.from_dict(bracket.analysis_features, orient='index', columns=col_names)
            all_df.append(df)
    df = combine_dataframes(all_df)
    return df


def create_full_list(series_set):
    all_entrants = []
    for series in series_set:
        all_entrants += series.full_entrants_list
    all_entrants = list(set(all_entrants))
    all_entrants.sort()
    return all_entrants


def process_data(series_set):
    df = construct_dataframe_from_iter(series_set)
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)
    return df