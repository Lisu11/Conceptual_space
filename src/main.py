#!/usr/bin/python3

import numpy as np
import fuzzy
import fuzzyComparator
from fuzzy import num_to_fuzzy
import algorithm
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv
from tqdm import tqdm, tqdm_gui
import random


def assignColors(prots):
        cols = []
        for i in range(len(prots)):
            hsv = (i/len(prots), 0.55, 0.9)
            cols.append(hsv_to_rgb(hsv))
        return cols

def plotSpace2D(space, prototypes):
    
    print("Partitioning")
    partAlg = algorithm.PartitioningAlgorithm(space, prototypes)
    labeled = partAlg.run()
    print("Partitioning complete")

    print("Processing data from algorithm")
    colors = assignColors(prototypes)
    labeled.sort(key = lambda x: x[1]) # sort by labels
    patritions = []
    for _ in prototypes:
        patritions.append([])

    for (p, l) in labeled:
        patritions[l].append(p)
    
    print("Plotting regions")
    for i in tqdm(range(len(patritions))):
        l = tuple(zip(*patritions[i]))
        if len(l) != 0:
            plt.scatter(l[0], l[1], marker='.', c=np.array([colors[i]]))
        else:
            print("Prototype", i, "is very weak")

    # plot prototypes with slightly different shade
    print("Plotting prototypes")
    for i in tqdm(range(len(prototypes))):
        hsv = rgb_to_hsv(colors[i])
        hsv[1] = 1 # make it darker
        col = hsv_to_rgb(hsv)
        l = tuple(zip(*prototypes[i].domain()))
        plt.scatter(l[0], l[1], c=np.array([col]))
    plt.show()

def generateSpace(begin, end, count=50):
    xs = np.linspace(begin, end, num = count)
    ys = np.linspace(begin, end, num = count)
    spaceDom = []
    spaceCod = []
    for x in xs:
        for y in ys:
            spaceDom.append((x, y))
            spaceCod.append(num_to_fuzzy(1))
    return fuzzy.FuzzySet(spaceDom, spaceCod, num_to_fuzzy(0))
    # return spaceDom

def generateSamplePrototypes():
    dom = [(1, 1.5), (2, 1.5), (1.5, 0.9)]
    cod = [ num_to_fuzzy(0.5), num_to_fuzzy(0.2), num_to_fuzzy(0.2)]
    f1 = fuzzy.FuzzySet(dom, cod, defZero=num_to_fuzzy(0))


    dom = [(6.6, 7.7), (6.8, 7.5), (7, 7.8)]
    cod = [num_to_fuzzy(0.2), num_to_fuzzy(0.2), num_to_fuzzy(0.9)]
    f2 = fuzzy.FuzzySet(dom, cod, defZero=num_to_fuzzy(0))


    dom = [(4, 4), (4.1, 3.9), (3.7, 4.2)]
    cod = [num_to_fuzzy(0.6), num_to_fuzzy(1), num_to_fuzzy(1)]
    f3 = fuzzy.FuzzySet(dom, cod, defZero=num_to_fuzzy(0))

    dom = [(1, 9), (1.2, 8.8), (0.9, 9.1)]
    cod = [num_to_fuzzy(0.9), num_to_fuzzy(0.1), num_to_fuzzy(0.5)]
    f4 = fuzzy.FuzzySet(dom, cod, num_to_fuzzy(0))
    return [f1, f2, f3, f4]


if __name__ == '__main__':
   
    fuzzy.FuzzyNumber.comparator = fuzzyComparator.chang
    plotSpace2D(generateSpace(-5, 15, 110), generateSamplePrototypes())
 
    # plotSpace2D(generateSpace(0, 10, 100), generateSamplePrototypes(),\
    #      metric=(lambda p, q: max(abs(p[0]-q[0]), abs(p[1]-q[1]))))
    
    # plotSpace2D(generateSpace(0, 10, 100), generateSamplePrototypes(),\
    #      metric=(lambda p, q: abs(p[0]-q[0])+ abs(p[1]-q[1])))
