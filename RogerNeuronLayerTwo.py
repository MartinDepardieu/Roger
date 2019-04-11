######################################
# https://github.com/MartinDepardieu #
######################################
# Roger's Layer Two Neuron #
############################
# input : models for a parameter
# ouput : models, weights for these models
######################### importations
# import global parameters
from RogerEar import *
# random importation
import random
######################### class definition
class RogerNeuronLayerTwo:
    # initialisation
    def __init__(self, input):
        # input : models
        self.fits = input
        # creation of a list with a weight for each fit
        self.listWeights = []
        # for each fit
        for self.i in range(numberOfFits):
            # random number generation between 0 and 1, starts at 1 to avoid rare division by 0
            self.listWeights.append(random.randint(1, 100)/100)
        # total weight
        self.totalWeight = sum(self.listWeights)
        # weights normalisation
        for self.i in range(numberOfFits):
            self.listWeights[self.i] = self.listWeights[self.i]/self.totalWeight
        # echo
        if echoLayer2:
            print('N2 weighting ', numberOfFits, ' fits : ', self.listWeights)
    # synapse
    def synapse(self):
        # returns fits, weights for these fits
        return self.fits, self.listWeights
