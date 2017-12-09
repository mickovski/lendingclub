#Project 1 - loan default rate in lending club
import os
import numpy as np
import pandas as pd
import sklearn

os.chdir("C:\\Users\\Walter Li\\Desktop\\eai quant")
lending_data = pd.read_csv("LoanStats_2017Q3.csv")

# parse the data to only include 
# Logistic regression
from sklearn import linear_model as lm

alpha_lasso = [1e-15, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20]
lasso_cv = linear_model.LassoCV(alphas=alpha_lasso, fit_intercept=False, normalize=True, cv=5)
lasso_cv.fit(X,y)
tuninglambda = lasso_cv.alpha_
lasso_model = linear_model.Lasso(alpha= tuninglambda, fit_intercept=False, normalize=True, max_iter=1e9)
lasso_model.fit(X,y)
lassopred = lasso_model.predict(X)

