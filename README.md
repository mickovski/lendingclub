# lendingclub
Lending Club for EAI
## Run LASSO regression
- Use data from Lending Club website
- In order to get which variables to use in the model, we run LASSO regression which will yield several variables with coefficients of zero.
- For NaN values, we replace them with zeros (such as number of months since last deliquency)
- From 34 variables in the data, there are 11 of them that have nonzero coefficients after fitting the model:
  * loan_amnt
  * annual_inc
  * fico_range_low
  * fico_range_high
  * total_pymnt
  * total_rec_prncp
  * total_rec_int
  * last_fico_range_high
  * last_fico_range_low
  * avg_cur_bal
  * percent_bc_gt_75
- Using cross validation, we find that the amount of penalization chosen by cross validation alpha = **0.0001**
