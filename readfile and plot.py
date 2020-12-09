import matplotlib.pyplot as plt
import numpy as np
filename = 'result1209.txt'
with open(filename, 'r') as f:
    revenue = f.readline()
    cost = f.readline()
    acc = f.readline()
    RC = f.readline()
revenue = revenue[11:-2]
print(revenue)
revenue = revenue.translate({ord(','): None}) #remove the comma
revenue = revenue.split()
revenue = [ int(float(x)) for x in revenue] # convert string to int
cost = cost[8:-2]
cost = cost.translate({ord(','): None})
cost = cost.split()
cost = [ int(float(x)) for x in cost]
acc = acc[20:-2]
acc = acc.translate({ord(','): None})
acc = acc.split()
acc = [ float(x) for x in acc] #convert string to float
RC = RC[13:-2]
RC = RC.translate({ord(','): None})
RC = RC.split()
RC = [ float(x) for x in RC]

