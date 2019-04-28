import pandas as pd
import sklearn
from sklearn import linear_model
def start_prediction(model, entrants):
    prediction = model.predict(entrants)