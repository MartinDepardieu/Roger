######################################
# https://github.com/MartinDepardieu #
######################################
# Roger's Prediction Run #
##########################
# Roger's predictive models are loaded from the files saved by the learning run
# Importing Roger's models testing function
from RogerPrediction import *
# test models by pickign random rows from the database and comparing real value to predicted value

# testing the best model by RMSE
testModelFromFile("bestModelByRMSE.txt")

# testing the best model by maximal error
#testModelFromFile("bestModelByBE.txt")

# using models to compute user values into a prediction

# using the best model by RMSE
#testModelUserValues("bestModelByRMSE.txt")

# using the best model by maximal error
#testModelUserValues("bestModelByBE.txt")
