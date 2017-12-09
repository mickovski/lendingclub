# lendingclub
Lending Club for EAI
- Run LASSO regression
- For NaN values, we replace them with zeros
- From 34 variables in the data, there are 11 of them that have nonzero coefficients:
  loan_amnt
  annual_inc
  fico_range_low
  fico_range_high
  total_pymnt
  total_rec_prncp
  total_rec_int
  last_fico_range_high
  last_fico_range_low
  avg_cur_bal
  percent_bc_gt_75
- Using cross validation, we find that the amount of penalization chosen by cross validation alpha = 0.0001
