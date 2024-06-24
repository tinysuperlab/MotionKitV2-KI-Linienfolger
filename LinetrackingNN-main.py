###############################################
# LinetrackingNN                              #
# Author: Th. Kaffka, Düsseldorf, Germany     #
# Date: 21.06.2024 13:31  		                #
# MIT License				                      #
# Copyright (c) 2024 Thomas Kaffka	          # 
# The above copyright notice and this         # 
# permission notice shall be included in      #
# all copies or substantial portions of       # 
# the Software.				                   # 
###############################################
from calliopemini import *
from MotionKit import*
from math import exp

x_columns = 2
y_columns = 2
x = []
y = []
nh = 5
h = []
w1 = []
w2 = []

###################
# creates an array.
def makeArray(n):
   array = []
   for i in range(0, n):
      array.append(0.0)
   return array

##########################
# creates an 2 dim. array.
def makeArray2Dim(row, column):
   array_main = []
   for i in range(0, row):
      array = []
      for j in range(0, column):
         array.append(0.0)
      array_main.append(array)
   return array_main

####################
# transfer function.
def t(a):
    try:
       ax = 1.0 / (1.0 + exp(-a))
    except:
       ax = 1.0
    return ax

#############################
# execute the neural network.
def execute():
   for k in range(0, nh):
       a = 0.0
       for i in range(0, x_columns + 1):
           a += w1[i][k] * x[i]
       h[k] = t(a)
   for j in range(0, y_columns):
       a = 0.0
       for k in range(0, nh + 1):
           a += w2[k][j] * h[k]
       y[j] = t(a)

#########################################
# execute the neural network with values.
def executeFunction(x1, y1):
   x[0] = x1
   x[1] = y1
   execute()
   result = [y[0], y[1]]
   return result

#################################
# initializes the neural network.
x = makeArray(x_columns)
x.append(1.0) # adds the bias.
y = makeArray(y_columns)
h = makeArray(nh)
h.append(1.0) # adds the bias.
w1 = makeArray2Dim(x_columns + 1, nh + 1)
w2 = makeArray2Dim(nh + 1, y_columns)

w1[0][0]=4.825543485979368
w1[1][0]=-4.657038455171622
w1[2][0]=2.1911501059061904
w1[0][1]=-3.399153195862444
w1[1][1]=1.9405685358115248
w1[2][1]=-2.9063549397398414
w1[0][2]=-3.045723890146699
w1[1][2]=3.5393031776186534
w1[2][2]=1.6094504715196265
w1[0][3]=-4.451935744115603
w1[1][3]=4.822620755945099
w1[2][3]=2.060141869495222
w1[0][4]=-0.14634936861028106
w1[1][4]=1.248617737599801
w1[2][4]=0.4544227289206888
w1[0][5]=0.7348344376711272
w1[1][5]=0.4073663743156959
w1[2][5]=0.6124884382972615

w2[0][0]=5.172231477156584
w2[0][1]=1.005276215633418
w2[1][0]=-4.082417008439689
w2[1][1]=0.8729970144585879
w2[2][0]=0.5043306434005668
w2[2][1]=2.220016222093835
w2[3][0]=0.6297432129409449
w2[3][1]=4.726995029233251
w2[4][0]=-1.2998034021280291
w2[4][1]=-1.2153224460224736
w2[5][0]=-2.434457286032953
w2[5][1]=-4.048083047652453

go = 0
while True:
    if (button_a.is_pressed()):
        go = 1
    if (button_b.is_pressed()):
        go = 0
        motorR(0,0)
        motorL(0,0)
    if (go == 0):
        continue
    sleep(200)
    motorR(0,20)
    motorL(0,20)
    line_right = read_lineFollowR()
    line_left = read_lineFollowL()
    result = [0, 0]
    if (line_right == 0 and line_left == 0):
        result = executeFunction(0.1, 0.1)
    elif  (line_right == 1 and line_left == 0):
        result = executeFunction(0.9, 0.1)
    elif  (line_right == 0 and line_left == 1):
        result = executeFunction(0.1, 0.9)
    elif  (line_right == 1 and line_left == 1):
        result = executeFunction(0.9, 0.9)
    if(result[0] > 0 and result[0] < 0.5
       and result[1] > 0.5 and result[1] < 1.0):
        motorR(0,0)
    if(result[0] > 0.5 and result[0] < 1
       and result[1] > 0 and result[1] < 0.5):
        motorL(0,0)
