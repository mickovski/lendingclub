# Week 1: default/charged off prediction (LASSO) 
import os
import numpy as np
import pandas as pd
from sklearn import linear_model as lm

# change to your directory
os.chdir("/Users/mickovskii/Documents/EAI")
# convert % to float
# lending_data = pd.read_csv("loanData.csv", converters={'dti':p2f})
lending_data = pd.read_csv("loanData.csv")

# find number of rows
numOfLoans = len(lending_data["loan_status"][~pd.isnull(lending_data["loan_status"])]) - 1
# truncate data
lending_data = lending_data.truncate(after = numOfLoans)

# % to float
def p2f(x):
    return float(x.strip('%'))/100

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

# fill missing values
lending_data = lending_data.fillna(0)   

# first instance of Lasso
data = lending_data.loc[:, lending_data.columns != "loan_status"]
status = lending_data["loan_status"]

#log = lm.LogisticRegression(penalty='l1', solver='liblinear')
#log.fit(data, status)
#initialpred = log.predict(data)

# Use LASSO
las = lm.Lasso(alpha = 0.1)
las.fit(data, status)
# number of non-zero coeff
sum(las.coef_ != 0)
for number in range(len(las.coef_)):
    if las.coef_[number] != 0: print(list(lending_data)[number + 1])

# cross validation to find optimal l1 penalty
allAlphas = [1e-15, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20]
#logistic_cv = lm.LogisticCV(alphas=alpha_lasso_logisitic, fit_intercept=False, normalize=True, cv=5)
#logistic_cv.fit(data, status)
#tuninglambda = logistic_cv.alpha_
#logistic_model = lm.LogisticRegression(penalty = 'l1', solver = 'liblinear', alpha= tuninglambda, fit_intercept=False, normalize=True, max_iter=1e9)
#logistic_model.fit(data, status)

# Cross Validation
lasso_cv = lm.LassoCV(alphas = allAlphas)
lasso_cv.fit(data, status)
# The amount of penalization chosen by cross validation
lasso_cv.alpha_