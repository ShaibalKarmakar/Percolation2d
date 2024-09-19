import pickle 
import os
import numpy as np
import matplotlib.pyplot as plt

import statsmodels.api as sm

import pandas as pd


with open(os.path.join(os.getcwd(), "data.pkl"), "rb") as fp:
    data = pickle.load(fp)



for n in data.keys():
    print(data[n])

    X = np.array(list(data[n].keys()))
    Y = np.array([data[n][p] for p in X])
    x_ = -1*np.log(0.5-X)
    y_ = np.log(Y)

    df = pd.DataFrame({"x":x_, "y":y_})
    xdf = df["x"]
    ydf = df["y"]
    xdf = sm.add_constant(xdf)
    model = sm.OLS(ydf, xdf).fit()
    print(model.summary())
    m = model.params.iloc[1]
    c = model.params.iloc[0]
    a = np.linspace(np.min(x_)-1, np.max(x_)+1, 1000)
    b = m*a +c
    plt.plot(a,b)
    plt.plot(x_, y_, 'o')
    plt.savefig("regress.png")
    plt.close()



