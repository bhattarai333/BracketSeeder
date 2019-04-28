import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.neural_network import MLPClassifier
from matplotlib import pyplot as plt


def start_analysis(df):
    y = df["H2H Set Count"]
    X = df.drop(columns=["H2H Set Count"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    print("Training Model")
    alg = linear_model.LinearRegression()
    alg.fit(X_train, y_train)
    #predictions = lm.predict(X_test)
    #print(predictions)
    return alg