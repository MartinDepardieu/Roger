######################################
# https://github.com/MartinDepardieu #
######################################
# Roger's Prediction functions #
################################
# both functions will load a model from a file
# testModelUserValues(filename) loads a model from a file then let the user input values for the parameters
# this function is useful to generate predictions from real world data
# testModelFromFile(filename) will load the database and pick random rows, then compare the result given by the model with the real result
# this function is used to play with the models and test them rapidly
######################### importations
# numpy, sqlite and random importation
import random
import sqlite3
import numpy as np
######################### function def
def testModelUserValues(fileName):
    # if the file exists
    try:
        # opening to read
        fromFile = open(fileName, "r")
        # feteching lines
        fileLines = fromFile.read().splitlines()
    # if the file does not exist
    except:
        # echo
        print('No model found, please run Roger\'s learning routing to generate one.')
    # if the file exists
    else:
        # loading the model's parameters from the file
        database = fileLines[3]
        table = fileLines[4]
        toPredict = fileLines[5]
        numberOfFits = int(fileLines[6])
        parameters = fileLines[7].split()
        numberOfParameters = len(parameters)
        weightsParameters = fileLines[8].split()
        # listing all the models and weights for them
        allModels=[]
        allWeights=[]
        # for each parameter
        for i in range(numberOfParameters):
            # models and weights for this parameter
            modelsForThisParameter=[]
            weightsForThisParameter=[]
            # for each fit
            for u in range(numberOfFits):
                # cleaning data from file
                rawLine = fileLines[9+i+u]
                rawNumbers = rawLine[2:-1]
                # splitting the string to get polynomial's params
                thisModel = [float(x) for x in rawNumbers.split()]
                # adding this model to the list
                modelsForThisParameter.append(thisModel)
                # same with the weights
                thisWeight = fileLines[9+numberOfFits*numberOfParameters+i+u]
                weightsForThisParameter.append(thisWeight)
            # adding models and weights for this parameter to the tables
            allModels.append(modelsForThisParameter)
            allWeights.append(weightsForThisParameter)
        # echo
        print(numberOfParameters, ' parameters being inputed to predict ', toPredict, ' : ', parameters, '\n')
        # values input
        Xinput=[]
        # for each parameter
        for thisParameter in range(numberOfParameters):
            # user input
            prompt = 'Value for ' + parameters[thisParameter] + ' : '
            # adding the values to the list
            Xinput.append(int(input(prompt)))
        # final y' calculation per parameter
        YPParam = []
        # for each parameter
        for this_parameter in range(numberOfParameters):
            # each N3 returns list of weights for each parameter, list of [[models], [weights]] for each parameter
            # fetching models and weights for this parameter
            modelsForThisParameter = allModels[this_parameter]
            weightsForThisParameter = allWeights[this_parameter]
            # calculating a list y' for each model
            YPrimePerModel = []
            # for each model
            for this_model in range(numberOfFits):
                # function
                function = np.poly1d(modelsForThisParameter[this_model])
                # weight
                weight = weightsForThisParameter[this_model]
                # x
                x = Xinput[this_parameter]
                # f(x)
                fx = function(x)
                # weight * f(x)
                YPThisModel = float(weight)*fx
                # add these y' to the list of y'
                YPrimePerModel.append(YPThisModel)
            # create this value
            YPParam.append(0)
            # for each model
            for this_model in range(numberOfFits):
                # addition of each weighted values to obtain the final value
                YPParam[this_parameter]=YPParam[this_parameter]+YPrimePerModel[this_model]
        # weight of the parameters
        # creation of variable
        thisYPrime = 0
        # for each parameter
        for this_parameter in range(numberOfParameters):
            # y' for this parameter
            YPForThisParameter = YPParam[this_parameter]
            # weight for this parameter
            weightForThisParameter = float(weightsParameters[this_parameter])
            # y' calculated by weighting all y' for each parameter
            thisYPrime = thisYPrime + YPForThisParameter*weightForThisParameter
        # final y
        finalPrediction = int(thisYPrime)
        # echo
        print('\nPredicted value of ', toPredict, ' for the given parameters : ', finalPrediction)
######################### function def
def testModelFromFile(fileName):
    # the first part is the exact same as in the first function to load the model
    try:
        fromFile = open(fileName, "r")
        fileLines = fromFile.read().splitlines()
    except:
        print('No model found, please run Roger\'s learning routing to generate one.')
    else:
        database = fileLines[3]
        table = fileLines[4]
        toPredict = fileLines[5]
        numberOfFits = int(fileLines[6])
        parameters = fileLines[7].split()
        numberOfParameters = len(parameters)
        weightsParameters = fileLines[8].split()
        allModels=[]
        allWeights=[]
        for i in range(numberOfParameters):
            modelsForThisParameter=[]
            weightsForThisParameter=[]
            for u in range(numberOfFits):
                rawLine = fileLines[9+i+u]
                rawNumbers = rawLine[2:-1]
                thisModel = [float(x) for x in rawNumbers.split()]
                modelsForThisParameter.append(thisModel)
                thisWeight = fileLines[9+numberOfFits*numberOfParameters+i+u]
                weightsForThisParameter.append(thisWeight)
            allModels.append(modelsForThisParameter)
            allWeights.append(weightsForThisParameter)
        print(numberOfParameters, ' parameters being inputed to predict ', toPredict, ' : ', parameters, '\n')
############## this part is where the x input is randomly drawn from the database
        # list of parameter construction to use in SQL request
        listOfParameters = parameters[0]
        for i in range(numberOfParameters-1):
            listOfParameters = listOfParameters + ',' + parameters[i+1]
        # database connexion
        dataBaseConnexion = sqlite3.connect(database)
        # cursor creation to move around the database
        curseur = dataBaseConnexion.cursor()
        # definition of SQL request
        # will return y + x
        SQLRequest = 'SELECT ' + toPredict + ',' + listOfParameters + ' FROM ' + table
        # execution of SQL request
        curseur.execute(SQLRequest)
        # verification that each row contains all values
        validValues = []
        # for each row
        for row in curseur:
            # assuming all values are present
            allValuesOk=1
            # for each parameter + y
            for this_parameter in range(numberOfParameters+1):
                # if the value exists for this parameter
                if row[this_parameter]:
                    # doing nothing
                    valueOk = 1
                else:
                    # if it doesn't exist, all values is 0
                    allValuesOk=0
            # if all values are present
            if allValuesOk:
                # adding this row to the list of valid rows
                validValues.append(row)
        # number of valid rows
        numberOfValidValues=len(validValues)
        # echo
        print('\n', numberOfValidValues, ' complete rows found for these parameters in the database.\n')
        print('Database loaded, starting predictions.\nPress enter for another prediction, q + enter to quit.')
        # loop to continue making predictions until user quits
        intheloop = 1
        while intheloop:
            # list of positions for the values to sample
            positionToSample = random.randint(0, numberOfValidValues)
            # echo
            print('\nTesting position ', positionToSample)
            # creation of the list of sample rows
            sampleRow=validValues[positionToSample]
            # complete table for y, x1, x2... for each parameter
            YXTable = []
            # for each x column + y
            for this_parameter in range(numberOfParameters+1):
                # addition of a column
                YXTable.append([])
                # addition of the value for this parameter in this row
                YXTable[this_parameter].append(sampleRow[this_parameter])
            # real y table
            realY = YXTable[0][0]
            # y column deletion
            del YXTable[0]
            # x table = yx table without the y
            Xinput = YXTable
            # final y' calculation per parameter
            YPParam = []
            # for each parameter
            for this_parameter in range(numberOfParameters):
                # each N3 returns list of weights for each parameter, list of [[models], [weights]] for each parameter
                # fetching models and weights for this parameter
                modelsForThisParameter = allModels[this_parameter]
                weightsForThisParameter = allWeights[this_parameter]
                # calculating a list y' for each model
                YPrimePerModel = []
                # for each model
                for this_model in range(numberOfFits):
                    # function
                    function = np.poly1d(modelsForThisParameter[this_model])
                    # weight
                    weight = weightsForThisParameter[this_model]
                    # x
                    x = Xinput[this_parameter]
                    # f(x)
                    fx = function(x)
                    # weight * f(x)
                    YPThisModel = float(weight)*fx
                    # add these y' to the list of y'
                    YPrimePerModel.append(YPThisModel)
                # create this value
                YPParam.append(0)
                # for each model
                for this_model in range(numberOfFits):
                    # addition of each weighted values to obtain the final value
                    YPParam[this_parameter]=YPParam[this_parameter]+YPrimePerModel[this_model]
            # weight of the parameters
            # creation of variable
            thisYPrime = 0
            # for each parameter
            for this_parameter in range(numberOfParameters):
                # y' for this parameter
                YPForThisParameter = YPParam[this_parameter]
                # weight for this parameter
                weightForThisParameter = float(weightsParameters[this_parameter])
                # y' calculated by weighting all y' for each parameter
                thisYPrime = thisYPrime + YPForThisParameter*weightForThisParameter
            # final y
            finalPrediction = int(thisYPrime)
            # echo
            print('Predicted :', finalPrediction, ', real : ', realY, ", error : ", abs(int(((finalPrediction-realY)/realY)*100)), '%')
            # user input : enter restarts prediction loop
            prompt = input('')
            # if user prompts q, get out of the loop
            if prompt  == "q":
                intheloop=0
