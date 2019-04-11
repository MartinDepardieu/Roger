######################################
# https://github.com/MartinDepardieu #
######################################
# Roger's Ear #
###############
# the ear of Roger is where global parameters are stored
# each component of Roger has access to these parameters
# global echo
echoGlobal = 1
# echo layer 1
echoLayer1 = 0
# echo layer 2
echoLayer2 = 1
#echo layer 3
echoLayer3  = 1
#echo layer 4
echoLayer4 = 1
# arbitrary number of neurons in each layer 2 cluster
numberNeuronsPerL2Cluster = 10
# arbitrary number of neurons in the layer 3
numberNeuronsLayerThree = 10
# parameters for the model generation
# database name
database = 'database.sqlite'
# table name
table = 'Player_Attributes'
# parameter to predict
toPredict='overall_rating'
# parameters to modelise :
'''
parameters=[  # full parameters
'crossing' , 'finishing', 'heading_accuracy', 'short_passing', 'volleys',
'dribbling', 'curve', 'free_kick_accuracy', 'long_passing', 'ball_control',
'acceleration', 'sprint_speed', 'agility', 'reactions', 'balance',
'shot_power', 'jumping', 'stamina', 'strength', 'long_shots',
'aggression', 'interceptions', 'positioning', 'vision', 'penalties',
'marking', 'standing_tackle', 'sliding_tackle', 'gk_diving', 'gk_handling',
'gk_kicking', 'gk_positioning', 'gk_reflexes'
]
'''
parameters=[  # test
'crossing' , 'finishing', 'heading_accuracy', 'short_passing', 'volleys'#,
#'dribbling', 'curve', 'free_kick_accuracy', 'long_passing', 'ball_control'
]
# degrees-1 for the polynomial fits that will be used in the layer 1
fitTypes=[0, 1, 2]
# sample rate for models testing by layer 4
layerFourSampleRate = 0.001
# number of parameters to take into account
numerOfParameters = len(parameters)
# number of possible fits
numberOfFits = len(fitTypes)
