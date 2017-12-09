# Week 1: default/charged off prediction 
import os
import numpy as np
import pandas as pd
from sklearn import linear_model as lm

# change to your directory
os.chdir("C:\\Users\\Walter Li\\Desktop\\eai quant")
lending_data = pd.read_csv("loanData.csv")

# if loan has defaulted or been charged off, return 1, else return 0
def checkDelinquency(index):
    loan = lending_data.iloc[index]
    status = loan["loan_status"]
    if status == "Default" or status == "Charged Off":
        lending_data.set_value(index, "loan_status", 1)
        return 1
    else:
        lending_data.set_value(index, "loan_status", 0)
        return 0
    
# update statuses
for i in lending_data.index:
    if i % 100 == 0: print(i)
    checkDelinquency(i)

# first instance of logistic regresison
data = lending_data.loc[:, lending_data.columns != "loan_status"]
status = lending_data["loan_status"]
log = lm.LogisticRegression(penalty='l1', solver='liblinear')
log.fit(data, status)

initialpred = log.predict(data)

# cross validation to find optimal l1 penalty
alpha_lasso_logsitic = [1e-15, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20]
logistic_cv = lm.LogisticCV(alphas=alpha_lasso_logistic, fit_intercept=False, normalize=True, cv=5)
logistic_cv.fit(data, status)
tuninglambda = logistic_cv.alpha_
logistic_model = lm.LogisticRegression(penalty = 'l1', solver = 'liblinear', alpha= tuninglambda, fit_intercept=False, normalize=True, max_iter=1e9)
logistic_model.fit(data, status)

