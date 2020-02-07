#!/usr/bin/python3

import numpy as np
import fuzzy
from tqdm import tqdm, tqdm_gui
import metrics
# from types import List

class PartitioningAlgorithm:
    
    euclidianMetric = (lambda p,q : np.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2))
    fuzzyMetric = metrics.fuzzyMetric

    def __init__(self, space, prototypes, metric=euclidianMetric):
        ''' space : type-2 fuzzy set with point as domain?
            prototypes - list of type-2 fuzzy prototypes?
        '''
        self.space = space
        if not space:
            raise Exception("Given empty space")
        dim = len(space[0]) 
        if dim == 2:
            self.dimCaseFun = lambda y: np.log(y)
        elif dim >= 3:
            self.dimCaseFun = lambda y: y**(2 - dim)
        else:
            raise Exception("1-dimentional space") # is it nessescary?
        self.metric = metric
        self.fuzzyIntegral = fuzzy.integratFuzzyFunction

        self.prototypeBases = list(map(lambda p : p.domain(), prototypes))
        self.prots = prototypes



    def phi(self, x, i):
        # prepare fuzzy function
        fuzzyFun = lambda y : self.prots[i](y).times(self.dimCaseFun(self.metric(x, y)))       
        return - self.fuzzyIntegral(self.prototypeBases[i], fuzzyFun)


    def deletePrototypes(self):
        sp = []
        for point in self.space:
            found = False
            for prot in self.prototypeBases:
                if point in prot:
                    found = True
            if not found:
                sp.append(point)
        return sp

    def run(self):
        sp = self.deletePrototypes()
        labeledSpace = []
        for x in tqdm(sp):
            phis = list(map(lambda i: self.phi(x, i), range(len(self.prots))))
            bestPhi = max(phis)
            bestIndex = phis.index(bestPhi)
            labeledSpace.append((x, bestIndex))
        return labeledSpace
