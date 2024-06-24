# -*- coding: utf-8 -*-
###########################################
# program trains a neural network.        #
# file: LinetrackingTraining.py           #
# Author: Th. Kaffka, Düsseldorf, Germany #
# Date: 21.06.2024 13:31  		  #
# MIT License				  #
# Copyright (c) 2024 Thomas Kaffka	  # 
# The above copyright notice and this     # 
# permission notice shall be included in  #
# all copies or substantial portions of   # 
# the Software.				  # 
###########################################

from xml.dom import minidom
from math import exp
import random

xml_path = "C:/Users/thkaf/Documents/_Thomas/Roboter/Calliope/MotionKit/Projekte/LineTracking/"

#######################
# get the example data.
dom = minidom.parse(xml_path + 'LineTracking.xml')
elements_x = dom.getElementsByTagName('ExampleX')
elements_y = dom.getElementsByTagName('ExampleY')

example = []

for element in elements_x:
    value1 = float(element.attributes['value1'].value)
    value2 = float(element.attributes['value2'].value)
    example += [[value1, value2]]

ndx = 0
for element in elements_y:
    value1 = float(element.attributes['value1'].value)
    value2 = float(element.attributes['value2'].value)
    ex = example[ndx]
    ex += [value1, value2]
    ndx += 1

###################
# creates an array.
def MakeArray(n):
   array = []
   for i in range(0, n):
      array.append(0.0)
   return array

##########################
# creates an 2 dim. array.
def MakeArray2Dim(row, column):
   array_main = []
   for i in range(0, row):
      array = []
      for j in range(0, column):
         array.append(0.0)
      array_main.append(array)
   return array_main

#################################
# initializes the neural network.
x_columns = 2
y_columns = 2
x = []
y = []
d = []
nh = 5
h = []
w1 = []
w2 = []
max_error_net = -1000
max_error = -100000
epsilon = 0.3

x = MakeArray(x_columns)
x.append(1.0) # adds the bias.
y = MakeArray(y_columns)
d = MakeArray(y_columns)
h = MakeArray(nh)
h.append(1.0) # adds the bias.
w1 = MakeArray2Dim(x_columns + 1, nh + 1)
w2 = MakeArray2Dim(nh + 1, y_columns)

for i in range(0, nh + 1):
    for j in range(0, x_columns + 1):
        w1[j][i] = random.random()

for i in range(0, nh + 1):		
    for j in range(0, y_columns):
        w2[i][j] = random.random()

####################
# transfer function.
def T(a):
    try:
       ax = 1.0 / (1.0 + exp(-a))
    except:
       ax = 1.0
    return ax

#############################
# execute the neural network.
def Execute():
   for k in range(0, nh):
       a = 0.0
       for i in range(0, x_columns + 1):
           a += w1[i][k] * x[i]
       h[k] = T(a)
   for j in range(0, y_columns):
       a = 0.0
       for k in range(0, nh + 1):
           a += w2[k][j] * h[k]
       y[j] = T(a)

###############################
# execute the back propagation.
def BackPropagate():
    global max_error_net
    
    # gradient descend.
    Err_H = MakeArray(nh + 1) # error of the hidden elements.

    for k in range(0, nh + 1):
        Err_H[k] = 0.0
    
    max_error_net = -10000

    for j in range(0, y_columns): # adjustment of the w2 weights, to calculate the error in the elements H[k], Err_H[k].
        delta = abs(d[j] - y[j])
        if (delta > max_error_net):
            max_error_net = delta # error in the y layer.
			
        delta = (d[j] - y[j]) * y[j] * (1.0 - y[j])

        for k in range(0, nh + 1):
            Err_H[k] += delta * w2[k][j]
            w2[k][j] += epsilon * delta * h[k] # deviation.

    for k in range(0, nh): # adjustment W1
        delta = Err_H[k] * h[k] * (1.0 - h[k])
        for i in range(x_columns + 1):
           w1[i][k] += epsilon * delta * x[i] # deviation.

#################################
# execute the learning procedure.
def Learning():
    global max_error
	
	# learning of the net.
    max_error = -1000000
		
    length = len(example)
    for p in range(0, length):
		# transfer the examples to the net.
        for i in range(x_columns):
            x[i] = example[p][i]
        for j in range(y_columns):
            d[j] = example[p][x_columns + j]
        
		# learn.
        Execute()
        BackPropagate()
			
        # prepare the error computing.
        if (max_error_net > max_error):
            max_error = max_error_net

###########
# training.		
for step in range(30000):
    Learning()
    if (step % 1000 == 0):
        print(step, max_error)

print()
for i in range(0, nh + 1):
    for j in range(0, x_columns + 1):
        print("w1[{}][{}]={}".format(j, i, w1[j][i]))

print()
for i in range(0, nh + 1):		
    for j in range(0, y_columns):
        print("w2[{}][{}]={}".format(i, j, w2[i][j]))
