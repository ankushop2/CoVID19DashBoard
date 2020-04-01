import requests
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import operator
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def train_model(x, y, polynomial_degree):
    polynomial_features = PolynomialFeatures(degree=polynomial_degree)
    x_poly = polynomial_features.fit_transform(x)

    model = LinearRegression()
    model.fit(x_poly, y)

    return model

def get_predictions(x, model, polynomial_degree):
    polynomial_features = PolynomialFeatures(degree=polynomial_degree)
    x_poly = polynomial_features.fit_transform(x)

    return model.predict(x_poly)

def print_stats( model, x, y, polynomial_degree, days_to_predict):
    y_pred = np.round(get_predictions(x, model, polynomial_degree), 0).astype(np.int32)
    days_pred = print_forecast(model, polynomial_degree, beginning_day=len(x), limit=days_to_predict)
    actual_poly = print_model_polynomial(model)

    return y_pred, days_pred, actual_poly

    #plot_graph(model_name, x, y, y_pred)

def print_model_polynomial( model):
    coef = model.coef_
    intercept = model.intercept_
    poly = "{0:.3f}".format(intercept)

    for i in range(1, len(coef)):
        if coef[i] >= 0:
            poly += " + "
        else:
            poly += " - "
        
        poly += "{0:.5f}".format(coef[i]).replace("-", "") + "X^" + str(i)

    return poly
   #print("The " + model_name + " model function is: f(X) = " + poly)

def plot_graph( x, y, y_pred):
    plt.scatter(x, y, s=10)
    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(x, y_pred), key=sort_axis)
    x, y_pred = zip(*sorted_zip)
    
    plt.plot(x, y_pred, color='m')
    plt.title("Amount of " + model_name + " in each day")
    plt.xlabel("Day")
    plt.ylabel(model_name)
    plt.show()

def print_forecast(model, polynomial_degree, beginning_day=0, limit=10):
    next_days_x = np.array(range(beginning_day, beginning_day + limit)).reshape(-1, 1)
    next_days_pred = np.round(get_predictions(next_days_x, model, polynomial_degree), 0).astype(np.int32)
    return next_days_pred;

    # print("The forecast for " + model_name + " in the following " + str(limit) + " days is:")

    # for i in range(0, limit):
    #     print(str(i + 1) + ": " + str(next_days_pred[i]))



def final():
    URL = "https://pomber.github.io/covid19/timeseries.json"
    r = requests.get(URL)
    data = r.json()
    india = data["India"]
    india_data = [d.get("confirmed") for d in india]
    x = []
    for i in range(0, len(india_data)):
        x.append(i)
    
    x = np.array(x).reshape(-1, 1)
    y = np.array(india_data)
    model = train_model(x, y,5)
    y_pred, days_pred, actual_poly = (print_stats(model, x, y, 5, 5))
    return x, y, y_pred, days_pred

