import numpy as np

def mse(file):
    error = 0.0
    lines = file.readlines()
    for line in lines:
        found, true = line.split(":")
        error += np.square(float(found)-float(true))
    print "average mse: " + str(error/len(lines))
mse(open("results90mackeyglass.txt", "r"))

def average(file):
    error = 0.0
    lines = file.readlines()
    for line in lines:
        error += float(line)
    print "average mse: " + str(error / len(lines))
average(open("results100mackeyglass.txt", "r"))