######################################
# https://github.com/MartinDepardieu #
######################################
# Roger's Layer One Neuron #
############################
# input : x, y, fit type
# output : model
######################### importations
# import global parameters
from RogerEar import *
# numpy importation
import numpy as np
######################### class definition
class RogerNeuronLayerOne:
    # initialisation
    def __init__(self, input):
        # input is a table containing two tables for the values of x and y, and fit type
        self.tableX = input[0]
        self.tableY = input[1]
        self.fitType = input[2]
        # using numpy's polyfit function to fit the data with a polynomial of degree fitType + 1
        self.fromPolyfit = np.polyfit(self.tableX, self.tableY, self.fitType+1)
        # using poly1d to build a function usable in calculs from the fit's results
        self.fittedFunction = np.poly1d(self.fromPolyfit)
        # echo
        if echoLayer1:
            print('N1 gives fit : ', self.fittedFunction)
    # synapse to communicate with other elements
    def synapse(self):
        # returns the function that was found to fit the data
        return self.fromPolyfit
