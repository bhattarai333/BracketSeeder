import src.bracket
import pandas as pd

class Series:
    name = ""
    brackets = []
    full_head_to_head = []

    def __init__(self, name, brackets):
        self.name = name
        self.brackets = brackets
        self.full_head_to_head = self.combine_h2h(brackets)

    def combine_h2h(self, brackets):
        full_h2h = pd.DataFrame
        for bracket in brackets:
            full_h2h = self.merge_dataframes(full_h2h, bracket)

        return brackets  #delete this

    def merge_dataframes(self, df1, df2):
        return df1