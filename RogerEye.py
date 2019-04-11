######################################
# https://github.com/MartinDepardieu #
######################################
# Roger's Eye #
###############
# the eyes of Roger are SQL connexions
# input : parameter's name for X, parameter's name for Y
# connects to the squlite3 database
# grabs rows for x, y
# only keeps rows that contain both values
# builds table for x and y values
# returns : X table, Y table
######################### importations
# import global parameters
from RogerEar import *
# import sqlite3
import sqlite3
######################### class definition
class RogerEye:
    # initialisation
    def __init__(self, input):
        # input is a table with name of parameter X, name of parameter Y
        self.nameX = input[0]
        self.nameY = input[1]
        # database connexion
        self.dataBaseConnexion = sqlite3.connect(database)
        # cursor creation to move around the database
        self.curseur = self.dataBaseConnexion.cursor()
        # definition of SQL request
        self.SQLRequest = 'SELECT ' + self.nameX + ',' + self.nameY + ' FROM ' + table
        # execution of SQL request
        self.curseur.execute(self.SQLRequest)
        # transformation of the SQL result into two tables for x, y
        self.tableX=[]
        self.tableY=[]
        # for each row sent back by the SQL request
        for self.row in self.curseur:
            # verification that both X and Y exist to eliminate partial entries
            if self.row[0] and self.row[1]:
                # add the values for x and y into their respective tables
                self.tableX.append(self.row[0])
                self.tableY.append(self.row[1])
        # closing of the database connexion
        self.dataBaseConnexion.close()
    # function to send the data back
    def whatDoYouSee(self):
        # returns a table for x, a table for y
        return self.tableX, self.tableY
