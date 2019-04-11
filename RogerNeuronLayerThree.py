######################################
# https://github.com/MartinDepardieu #
######################################
# Roger's Layer Three Neuron #
##############################
# input : layer 2 : clusters of models and weights for each parameter
# picks a N2 at random for each parameter
# weights the parameters
# ouput : models and weight for each parameter, weights for each parameter
######################### importations
# import global parameters
from RogerEar import *
# random importation
import random
######################### class definition
class RogerNeuronLayerThree:
    # initialisation
    def __init__(self, input):
        # each neuron in the layer 2 returns fits, weights for these fits
        self.L2 = input
        # weights for the parameters
        self.listWeights=[]
        # for each parameter
        for self.this_parameter in range(numerOfParameters):
            # generation of a weight between 0 and 1, start at 1 to avoid division by zero
            self.listWeights.append(random.randint(1, 100)/100)
        # total weight
        self.totalWeight = sum(self.listWeights)
        # weights normalisation
        for self.i in range(numerOfParameters):
            self.listWeights[self.i] = self.listWeights[self.i]/self.totalWeight
        # N2 selection : 1 per cluster that will give fits + weights for one parameter
        self.listPositions=[]
        # for each parameter
        for self.this_parameter in range(numerOfParameters):
            # random picking of a position in the cluster
            self.listPositions.append(random.randint(0, numberNeuronsPerL2Cluster-1))
        # fits list
        self.listModels=[]
        # in each cluster
        for self.this_cluster in range(numerOfParameters):
            # position of the neuron picked in the cluster
            self.thisPosition = self.listPositions[self.this_cluster]
            # select the models and weights from the N2 at this position in this cluster
            self.listModels.append(self.L2[self.this_cluster][self.thisPosition])
        # echo
        if echoLayer3:
            print('This N3 choose for ', numerOfParameters, ' clusters the weights ', self.listWeights, ' and from ',
            numberNeuronsPerL2Cluster, ' neurons in each cluster the fits outputed from neurons ', self.listPositions, '\n')
    # synapse
    def synapse(self):
        # returns list of weights for each parameter, list of [[models], [weights]] for each parameter
        return self.listWeights, self.listModels
