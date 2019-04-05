import src.data_collection as data_collection
import src.series as series
import pandas as pd

def get_urls(tournament_file_path):
    """

    Sample tournaments.txt:
    https://spartanweeklies.challonge.com/sw40
    https://smash.gg/tournament/spartan-weeklies-41/details
    https://smash.gg/tournament/spartan-weeklies-42/details

    """

    output = []
    with open(tournament_file_path, 'r') as f:
        for line in f:
            u = line.strip()
            if u == "::":
                break
            output.append(u)
    return output

def analyze_data(brackets):
    return brackets

def predict(m):
    return m

def write_to_file(prediction):
    pass

def figure_it_out(df1, df2):
    df3 = pd.concat([df1, df2], join="outer", axis=0)
    return df3

#urls = get_urls("tournaments.txt")
#data = data_collection.get_data(urls)
#print("Starting Data Analysis")
#print(data[0].head_to_head)
#ser = series.Series("MSU", data)
#model = analyze_data(data)
#prediction = predict(model)
#write_to_file(prediction)

data = data_collection.get_data(["https://challonge.com/xzu8nugn", "https://challonge.com/md75oh1n"])
df1 = data[0].head_to_head

df2 = data[1].head_to_head
df3 = figure_it_out(df1, df2)

print(df3)


