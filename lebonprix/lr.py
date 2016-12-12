import numpy as np
from sklearn import linear_model, preprocessing


class LinearRegression:
    def prepare_input(self, data, features, result):
        x = []
        y = []
        for elem in data:
            row = []
            for feature in features:
                row.append(float(elem[feature]))
            y.append(float(elem[result]))
            x.append(row)
        return (np.array(x), np.array(y))
        
    def lr(self, x, y, guess):
        """ Predict the value for some data
        
        Args:
            data (list(dict)) : an array of input data"""
        scaler = preprocessing.StandardScaler().fit(x)
        x_norm = scaler.transform(x)
        guess_norm = scaler.transform(guess)
        clf = linear_model.LinearRegression()
        clf.fit(x_norm, y)
        return clf.predict(guess_norm)