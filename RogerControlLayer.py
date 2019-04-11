######################################
# https://github.com/MartinDepardieu #
######################################
# Roger's Control layer #
#########################
# the control layer is where all elements are assembled to create predictive models
######################### loading of Roger's elements #########################
# Roger's Ear is where global parameters are stored
from RogerEar import *
# Roger's Eyes are SQL connexions to the database
from RogerEye import *
# Level 1 neuron
from RogerNeuronLayerOne import *
# Level 2 neuron
from RogerNeuronLayerTwo import *
# Level 3 neuron
from RogerNeuronLayerThree import *
# Level 4 neuron
from RogerNeuronLayerFour import *
######################### Connections to database to fetch all x values
# echo
if echoGlobal:
    print ('Roger will create a model to predict ', toPredict, ' from the ', numerOfParameters, ' given parameters : ', parameters)
# one eye = one database connexion to fetch one x, y combination
# eyes list
RogerEyes = []
# number of datapoint for each x, y
numberOfDatapoints = 0
# for each parameter, one SQL connexion fetches x, y
for this_parameter in range(numerOfParameters):
    # SQL request parameters
    sqlRequest = [parameters[this_parameter], toPredict]
    # execution of SQL request by building an Eye and asking it what it sees
    RogerEyes.append(RogerEye(sqlRequest).whatDoYouSee())
    # number of datapoints for this parameter
    numberOfDatapoints += len(RogerEyes[this_parameter][0])
# echo
if echoGlobal:
    print ('Roger has found ', numberOfDatapoints, ' datapoints for which all parameters are assigned a value.\n')
######################### Layer 1 creation
# one N1 for each parameter, fit combination
# number of neurons to create : number of parameters * number of possible fits for each parameters
numberNeuronsLayerOne = numerOfParameters*numberOfFits
# echo
if echoGlobal:
    print ('Roger will populate his first neuronal layer with ', numberNeuronsLayerOne, ' neurons.')
# list of Layer 1 neurons, organised by [parameter[fit], ]
RogerLayerOne = []
# for each parameter, fetching x, y from the SQL connexion and feeding them to the N1 for fitting
for this_parameter in range(numerOfParameters):
    # list of N1 fitting for this parameter
    N1sForThisParameter=[]
    # one N1 created for each possible fit
    for this_fit in range(numberOfFits):
        # N1 input : x, y coming from the eyes' list
        xForN1 = RogerEyes[this_parameter][0]
        yForN1 = RogerEyes[this_parameter][1]
        # x, y, type of fit
        inputForN1 = [xForN1, yForN1, fitTypes[this_fit]]
        # N1 creation and synapse connexion to fetch output which is function fitting x, y sent with this fit type
        N1sForThisParameter.append(RogerNeuronLayerOne(inputForN1).synapse())
        # echo
        if echoGlobal:
            print ('N1 number ', len(RogerLayerOne)+this_fit, ' has fitted ', parameters[this_parameter], ' with fit type ', fitTypes[this_fit])
    # adding the N1s for this parameter to the Layer 1
    RogerLayerOne.append(N1sForThisParameter)
######################### Layer 2 creation
# for each parameter, an arbitrary number of N2 are created
# in each cluster, the N2s give random weights to the fits created in the first layer
# the N2 sends back a list of models for a parameter with a list of weights for each model
# echo
if echoGlobal:
    print ('\nRoger will populate his second neuronal layer with ', numerOfParameters, ' clusters each containing ', numberNeuronsPerL2Cluster, ' neurons.')
# list of clusters, one per parameter
RogerLayerTwo = []
# one cluster is created for each parameter
for this_parameter in range(numerOfParameters):
    # echo
    if echoGlobal:
        print ('Cluster number ', len(RogerLayerTwo)+1, ' : ')
    # N2 list in this clusters
    thisCluster=[]
    # the models for this parameter are the input for the N2s in each cluster/parameter
    modelsForThisParameter = RogerLayerOne[this_parameter]
    # creation of an arbitrary number of N2 per cluster
    for i in range(numberNeuronsPerL2Cluster):
        # N2 creation and synapse connexion to fetch output which is fits, weights for this parameter
        thisCluster.append(RogerNeuronLayerTwo(modelsForThisParameter).synapse())
    # adding this cluster to the Layer 2
    RogerLayerTwo.append(thisCluster)
######################### Layer 3 creation
# the L3 weights each parameter
# it takes in the L2 and outputs a complete model
# echo
if echoGlobal:
    print('\nRoger is now populating his third layer with ', numberNeuronsLayerThree, ' neurons.')
# list of N3 neurons
RogerLayerThree=[]
# creation of an arbitrary number of N3
for this_neuron in range(numberNeuronsLayerThree):
    # N3 creation and synapse connexion to fetch output : complete models
    RogerLayerThree.append(RogerNeuronLayerThree(RogerLayerTwo).synapse())
######################### Layer 4 creation
# this layer only has one L4 neuron
# the L4 samples random datapoints in the database then uses the models from each N3 to generate a list of predictions
# the predictions are compared to reality and the best model is selected = the best pathway/combination of weights/N3
# echo
if echoGlobal:
    print('\nRoger is now creating a layer 4 neuron to select the best neuronal pathway.')
# N4 creation, sending it L3, getting data back from synapse
# returns best model by RMSE, its RMSE, its max error, best model by error, its RMSE, its max error
RogerLayerFour = RogerNeuronLayerFour(RogerLayerThree).synapse()
# echo
if echoGlobal:
    print('\nRoger has finished learning.\n')
########## END learning - Start saving
# function to save models to text files
def saveModel(fileName, RMSE, MaxError, model):
    # creating the file and saving all relevant global parameters
    fileToSaveTo = open(fileName, "w")
    fileToSaveTo.write(str(RMSE)+'\n'+str(MaxError)+'\n'+ str(layerFourSampleRate) +'\n')
    fileToSaveTo.write(str(database)+'\n'+str(table)+'\n'+str(toPredict)+'\n')
    fileToSaveTo.write(str(numberOfFits)+'\n')
    # writing down fitted parameters
    for i in range(numerOfParameters):
        fileToSaveTo.write(str(parameters[i]) + ' ')
    fileToSaveTo.write('\n')
    # weights for each of these these parameters
    for i in range(numerOfParameters):
        fileToSaveTo.write(str(RogerLayerThree[model][0][i]) + ' ')
    fileToSaveTo.write('\n')
    # models for the parameters
    for i in range(numerOfParameters):
        for u in range(numberOfFits):
            fileToSaveTo.write(str(RogerLayerThree[model][1][i][0][u]) + '\n')
    # weights for the models
    for i in range(numerOfParameters):
        for u in range(numberOfFits):
            fileToSaveTo.write(str(RogerLayerThree[model][1][i][1][u]) + '\n')
    # closing the file
    fileToSaveTo.close()
# from the best models gotten back from L4
# L4 returns best model by RMSE, its RMSE, its max error, best model by max error, its RMSE, its max error
# best model by RMSE
bestModelByRMSE = RogerLayerFour[0]
bestModelByRMSERmse = RogerLayerFour[1]
bestModelByRMSEMaxError = RogerLayerFour[2]
# best model by lowest max error
bestModelByMaxError = RogerLayerFour[3]
bestModelByMaxErrorRmse = RogerLayerFour[4]
bestModelByMaxErrorMaxError = RogerLayerFour[5]
# saving the best model by RMSE
# if the file already exists
try:
    # open the file to read it
    fromFileBMR = open("bestModelByRMSE.txt", "r")
    # fetch each line
    fileLinesBMR = fromFileBMR.read().splitlines()
    # close the file
    fromFileBMR.close()
# if the file doesn't exist already
except:
    # echo
    print('No existing best RMSE model, saving the one coming from N3 number ', bestModelByRMSE)
    # save the current best RMSE model
    saveModel("bestModelByRMSE.txt", bestModelByRMSERmse, bestModelByRMSEMaxError, bestModelByRMSE)
# if the file already exist
else:
    # RMSE for the existing model
    existingModelRMSE = float(fileLinesBMR[0])
    # if new model's RMSE is better than the existing model's
    if bestModelByRMSERmse < existingModelRMSE:
        # echo
        print('The model from N3 number ', bestModelByRMSE, ' has a better RMSE than the existing saved model : ', bestModelByRMSERmse, 'vs', existingModelRMSE)
        print('Overwriting the old model...')
        # overwriting the file with new model
        saveModel("bestModelByRMSE.txt", bestModelByRMSERmse, bestModelByRMSEMaxError, bestModelByRMSE)
    # if the new model is no better than the old one
    else:
        # echo
        print('No new model had a better RMSE than the currently saved model.')
# doing the same thing but with the model with the lowest maximal error
try:
    fromFileBE = open("bestModelByBE.txt", "r")
    fileLinesBE = fromFileBE.read().splitlines()
    fromFileBE.close()
except:
    print('\nNo existing best maximum error model, saving the one coming from N3 number ', bestModelByMaxError)
    saveModel("bestModelByBE.txt", bestModelByMaxErrorRmse, bestModelByMaxErrorMaxError, bestModelByMaxError)
else:
    # maximal error of saved model
    existingModelMaxError = float(fileLinesBE[1])
    # if the max error of the current model is better than the saved one's
    if bestModelByMaxErrorMaxError < existingModelMaxError:
        print('\nThe model from N3 number ', bestModelByMaxError, ' has a better maximum error than the existing saved model : ', bestModelByMaxErrorMaxError, 'vs', existingModelMaxError)
        print('Overwriting the old model...')
        saveModel("bestModelByBE.txt", bestModelByMaxErrorRmse, bestModelByMaxErrorMaxError, bestModelByMaxError)
    else:
        print('\nNo new model had a better maximum error than the currently saved model.')
