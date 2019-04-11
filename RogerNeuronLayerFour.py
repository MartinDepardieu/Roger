######################################
# https://github.com/MartinDepardieu #
######################################
# Roger's Layer Four Neuron #
#############################
# input : layer 3 : each N3 has a complete model to input x1, x2 .... and outputs y prediction
# samples data from database
# tests each N3 : creates the y' from the models
# calculates root mean square error
# output : best model (best N3), RMSE of this model
######################### importations
# import global parameters
from RogerEar import *
# import the Eye
from RogerEye import *
# numpy, sqlite, math and random importation
import random
import math
import sqlite3
import numpy as np
######################### class definition
class RogerNeuronLayerFour:
    # initialisation
    def __init__(self, input):
        # input = layer 3
        self.L3 = input
        # echo
        if echoLayer4 :
            print('Found ', numberNeuronsLayerThree, ' L3 neurons treating ', numerOfParameters, ' parameters each.')
        # list of parameter construction to use in SQL request
        self.listOfParameters = parameters[0]
        for self.i in range(numerOfParameters-1):
            self.listOfParameters = self.listOfParameters + ',' + parameters[self.i+1]
        # database connexion
        self.dataBaseConnexion = sqlite3.connect(database)
        # cursor creation to move around the database
        self.curseur = self.dataBaseConnexion.cursor()
        # definition of SQL request
        # will return y + x
        self.SQLRequest = 'SELECT ' + toPredict + ',' + self.listOfParameters + ' FROM ' + table
        # execution of SQL request
        self.curseur.execute(self.SQLRequest)
        # verification that each row contains all values
        self.validValues = []
        # for each row
        for self.row in self.curseur:
            # assuming all values are present
            self.allValuesOk=1
            # for each parameter + y
            for self.this_parameter in range(numerOfParameters+1):
                # if the value exists for this parameter
                if self.row[self.this_parameter]:
                    # doing nothing
                    self.valueOk = 1
                else:
                    # if it doesn't exist, all values is 0
                    self.allValuesOk=0
            # if all values are present
            if self.allValuesOk:
                # adding this row to the list of valid rows
                self.validValues.append(self.row)
        # number of valid rows
        self.numberOfValidValues = len(self.validValues)
        # number of datapoints to sample
        self.numberOfSamplePoints = int(self.numberOfValidValues*layerFourSampleRate)
        # echo
        if echoLayer4:
            print(self.numberOfValidValues, ' complete rows found for these parameters in the database, sampling ',
            layerFourSampleRate*100, '% of them = ', self.numberOfSamplePoints, '\n')
        # list of positions for the values to sample
        self.positionsToSample=[]
        # for each sample point
        for self.i in range(self.numberOfSamplePoints):
            # random position in the complete list of values
            self.positionsToSample.append(random.randint(0, self.numberOfValidValues))
        # creation of the list of sample rows
        self.sampleRows=[]
        # for each point to sample
        for self.i in range(self.numberOfSamplePoints):
            # position to sample in the list
            self.positionToSample = self.positionsToSample[self.i]
            # addition of this position to the list of sample rows
            self.sampleRows.append(self.validValues[self.positionToSample])
        # complete table for y, x1, x2... for each parameter
        self.YXTable = []
        # for each x column + y
        for self.this_parameter in range(numerOfParameters+1):
            # addition of a column
            self.YXTable.append([])
            # for each row in the sample
            for self.row in self.sampleRows:
                # addition of the value for this parameter in this row
                self.YXTable[self.this_parameter].append(self.row[self.this_parameter])
        # real y table
        self.realY = self.YXTable[0]
        # y column deletion
        del self.YXTable[0]
        # x table = yx table without the y
        self.Xinput = self.YXTable
        # list of root mean square errors and maximum error
        self.listRMSE = []
        self.listMaxError = []
        # for each neuron in L3
        for self.this_neuron in range(numberNeuronsLayerThree):
            # list of y' calculated per parameter
            self.listYprimes = []
            # for each parameter
            for self.this_parameter in range(numerOfParameters):
                # each N3 returns list of weights for each parameter, list of [[models], [weights]] for each parameter
                # fetching models and weights for this parameter
                self.modelsForThisParameter = self.L3[self.this_neuron][1][self.this_parameter][0]
                self.weightsForThisParameter = self.L3[self.this_neuron][1][self.this_parameter][1]
                # calculating a list y' for each model
                self.YPrimePerModel = []
                # for each model
                for self.this_model in range(numberOfFits):
                    # function
                    self.function = np.poly1d(self.modelsForThisParameter[self.this_model])
                    # weight
                    self.weight = self.weightsForThisParameter[self.this_model]
                    # list of y primes for this model
                    self.YPThisModel = []
                    # for each x
                    for self.i in range(self.numberOfSamplePoints):
                        # x
                        self.x = self.Xinput[self.this_parameter][self.i]
                        # f(x)
                        self.fx = self.function(self.x)
                        # weight * f(x)
                        self.fxw = self.weight*self.fx
                        # add to the list
                        self.YPThisModel.append(self.fxw)
                    # add these y' to the list of y'
                    self.YPrimePerModel.append(self.YPThisModel)
                # final y' calculation per parameter
                self.YPParam = []
                # for each sample point
                for self.i in range(self.numberOfSamplePoints):
                    # create this value
                    self.YPParam.append(0)
                    # for each model
                    for self.this_model in range(numberOfFits):
                        # addition of each weighted values to obtain the final value
                        self.YPParam[self.i]=self.YPParam[self.i]+self.YPrimePerModel[self.this_model][self.i]
                # add this value to the list of y'
                self.listYprimes.append(self.YPParam)
            # weight of the parameters
            # each N3 returns list of weights for each parameter, list of [[models], [weights]] for each parameter
            self.weightsParameters = self.L3[self.this_neuron][0]
            # list of final y'
            self.YPrimes = []
            # for each point
            for self.i in range(self.numberOfSamplePoints):
                # creation of variable
                self.thisYPrime = 0
                # for each parameter
                for self.this_parameter in range(numerOfParameters):
                    # y' for this parameter
                    self.YPForThisParameter = self.listYprimes[self.this_parameter][self.i]
                    # weight for this parameter
                    self.weightForThisParameter = self.weightsParameters[self.this_parameter]
                    # y' calculated by weighting all y' for each parameter
                    self.thisYPrime = self.thisYPrime + int(self.YPForThisParameter*self.weightForThisParameter)
                # add this y' to the list
                self.YPrimes.append(self.thisYPrime)
            # list of squared differences
            self.listOfSquaredDifferences = []
            # for each sample point
            for self.i in range(self.numberOfSamplePoints):
                # real y
                self.RealY = self.realY[self.i]
                # calculated y'
                self.YPrime = self.YPrimes[self.i]
                # difference real/calculated
                self.difference = self.RealY - self.YPrime
                # squared difference, add to the list
                self.listOfSquaredDifferences.append(self.difference*self.difference)
            # sum of errors
            self.totalError = sum(self.listOfSquaredDifferences)
            # RMSE
            self.rmse = math.sqrt(self.totalError/self.numberOfValidValues)
            # maximum difference
            self.maxDiff = math.sqrt(max(self.listOfSquaredDifferences))
            # minimum difference
            self.minDiff=math.sqrt(min(self.listOfSquaredDifferences))
            # add the RMSE to the list
            self.listRMSE.append(self.rmse)
            # add the maximum difference to the list
            self.listMaxError.append(self.maxDiff)
            # echo
            if echoLayer4:
                print('RMSE for neuron', self.this_neuron, ' : ', self.rmse, ', error between ', self.minDiff, ' and ', self.maxDiff)
        # minimal RMSE among N3
        self.lowestRMSE = min(self.listRMSE)
        # best model for best RMSE
        self.bestModelRMSE = self.listRMSE.index(self.lowestRMSE)
        # maximum RMSE
        self.maxRMSE = max(self.listRMSE)
        # lowest difference
        self.lowestError = min(self.listMaxError)
        # for each model
        for self.i in range(numberNeuronsLayerThree):
            # if this model's max error is the same as the lowest error AND its RMSE is smaller than the maxRMSE
            if self.listMaxError[self.i] == self.lowestError and self.listRMSE[self.i] <= self.maxRMSE:
                # the max RMSE is now this model's
                self.maxRMSE = self.listRMSE[self.i]
                # this model is now the best model by error
                self.bestModelError = self.i
        # echo
        if echoLayer4:
            print('\nThe best model by RMSE comes from neuron ', self.bestModelRMSE, ' with a RMSE of ', self.lowestRMSE,
            ' and a maximal error of ', self.listMaxError[self.bestModelRMSE]
            ,'\nThe best model by maximal error comes from neuron ', self.bestModelError, ' with an error of ', self.lowestError,
            ' and a RMSE of ', self.listRMSE[self.bestModelError])
    # synapse
    def synapse(self):
        # returns best model by RMSE, its RMSE, its max error, best model by max error, its RMSE, its max error
        return self.bestModelRMSE, self.lowestRMSE, self.listMaxError[self.bestModelRMSE], self.bestModelError, self.listRMSE[self.bestModelError], self.lowestError
