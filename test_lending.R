### NOT USED ###
## MICK ###
install.packages(c("httr", "jsonlite", "lubridate"))
library(httr)
library(jsonlite)
library(lubridate)

apikey <- "Key Here"
url <- "https://api.lendingclub.com/api/investor/v1/loans/listing"
loans <- GET(url, showAll = TRUE, add_headers("Authorization" = apikey))
loans_parsed<- (fromJSON(content(r, "text", encoding="UTF-8"),simplifyVector = TRUE))$loans

fundedAmount <- loans_parsed$fundedAmount
expDefaultRate <- loans_parsed$expDefaultRate
intRate <- loans_parsed$intRate
grade <- loans_parsed$grade
for (i in 1:length(grade)) {
  grade[i] <- utf8ToInt(grade[i]) - 65
}
grade <- as.numeric(grade)
dti <- loans_parsed$dti
mthsSinceLastDelinq <- loans_parsed$mthsSinceLastDelinq
X <- cbind(intRate, grade, dti, expDefaultRate)

# box-plot
boxplot(intRate~grade,
        cex=1, cex.axis = 1,
        main = "Interest rate on the loan by loan grade", 
        xlab = 'Grade', ylab = "Interest rate",
        col = rainbow(length(unique(grade))))

numberOfData <- length(grade)
shuffle <- sample(1:numberOfData)
test <- 1:20
train <- 21:numberOfData
x_test <- X[test, 1:3]
y_test <- X[test, 4]
x_train <- X[train, 1:3]
y_train <- X[train, 4]

# plot and l2
plot(expDefaultRate, intRate)
l2 <- lm(expDefaultRate ~ intRate + grade + dti)
summary(l2)$r.squared 
fittedValues <- cbind(1, x_test) %*% l2$coefficients
MSE <- mean((fittedValues - y_test) * (fittedValues - y_test))
MAE <- mean(abs(fittedValues - y_test))
MSE
MAE

# neural network
library(keras)
model <- keras_model_sequential()
model %>%
  layer_dense(units = 3, input_shape = c(3)) %>%
  layer_activation(activation = 'relu') %>%
  layer_dense(units = 2, input_shape = c(3)) %>%
  layer_activation(activation = 'relu') %>%
  layer_dense(units = 1) %>%
  layer_activation(activation = 'linear')

model %>% compile(
  loss = 'mean_squared_error',
  optimizer = 'sgd',
  metrics = c('mean_squared_error', 'mean_absolute_error')
)

model %>% fit(x_train, y_train, batch_size = 1, epochs = 100)
# out-of-sample test
score <- model %>% evaluate(x_test, y_test, batch_size = length(y_test))
score$mean_squared_error
score$mean_absolute_error

