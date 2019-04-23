import numpy as np
import pandas as pd
import random
import csv
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from scipy import stats
import math

def split_data(data, prob):
    """Split data into fractions [prob, 1 - prob]"""
    results = [], []
    for row in data:
        results[0 if random.random() < prob else 1].append(row)
    return results

def train_test_split(x, y, test_pct):
    """Split the features X and the labels y into x_train, x_test and y_train, y_test
    designated by test_pct. A common convention in data science is to do a 80% training
    data 20% test data split"""
    data = zip(x, y)								# pair corresponding values
    train, test = split_data(data, 1 - test_pct)    # split the data set of pairs
    x_train, y_train = zip(*train)					# magical un-zip trick
    x_test, y_test = zip(*test)
    return x_train, x_test, y_train, y_test

features = ['instant', 'dteday', 'season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered']

label = 'cnt'

def MultipleLinearRegression(X, y, linear_model):

    lm = linear_model
	### DO NOT TOUCH THIS PORTION OF THE CODE###
    params = np.append(lm.intercept_,lm.coef_)
    predictions = lm.predict(X)

    newX = np.append(np.ones((len(X),1)), X, axis=1)
    MSE = (sum((y-predictions)**2))/(len(newX)-len(newX[0]))

    var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
    sd_b = np.sqrt(var_b)
    ts_b = params/ sd_b

    p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-1))) for i in ts_b]

    myDF3 = pd.DataFrame()
    myDF3["Coefficients"],myDF3["Standard Errors"],myDF3["t values"],myDF3["Probabilites"] = [params,sd_b,ts_b,p_values]
    print(myDF3)

def MSE(X,y, linear_model):
    lm = linear_model
    predictions = lm.predict(X)
    newX = np.append(np.ones((len(X),1)), X, axis=1)
    return (sum((y-predictions)**2))/(len(newX)-len(newX[0]))


if __name__=='__main__':

	# DO not change this seed. It guarantees that all students perform the same train and test split
    random.seed(1)
	# Setting p to 0.2 allows for a 80% training and 20% test split
    p = 0.2
    X = []
    y = []
	#############################################
	# TODO: open csv and read data into X and y #
	#############################################
    def load_file(file_path):
        X = []
        y = []
        #with open(file_path, 'r', encoding='latin1') as file_reader:
            #reader = csv.reader(file_reader, delimiter=',', quotechar='"')
        with open('complete_data.csv') as features_file:
            csv_reader = csv.DictReader(features_file, delimiter = ',')
            #next(reader)
            for row in csv_reader:
                if row == []:
                    continue
                explanatory_var = []

                ### TODO: Select independent variables that might best predict the dependent variables ###
                explanatory_var.append(float(row['danceability']))
                explanatory_var.append(float(row['energy']))
                explanatory_var.append(float(row['tempo']))
                explanatory_var.append(float(row['loudness']))


                # Since our label bike_share_cnt is at the end of the row
                X.append(explanatory_var)
                #Since our label bike_share_cnt is at the end of the row
                bike_share_cnt = math.floor(float(row['score']))
                y.append(bike_share_cnt)
        return np.array(X, dtype='float64'), np.array(y, dtype='float64')


    X, y = load_file("complete_data.csv")


	##################################################################################
	# TODO: use train test split to split data into x_train, x_test, y_train, y_test #
	#################################################################################
    X_train, X_test, y_train, y_test = train_test_split(X, y, p)


	##################################################################################
	# TODO: Use Sci-Kit Learn to create the Linear Model and Output R-squared
	#################################################################################
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    r_squared = linear_model.score(X_test,y_test)

	# Prints out the Report
    MultipleLinearRegression(X_train, y_train, linear_model)
    mse_train = MSE(X_train, y_train, linear_model)
    mse_test = MSE(X_test, y_test, linear_model)

	# TODO: print linear_model score
    print(r_squared)
    print(mse_train)
    print(mse_test)
