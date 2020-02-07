#!/usr/bin/python3

import unittest
import fuzzy
from fuzzy import num_to_fuzzy
import numpy as np
import algorithm


def dupa():
    begin = 0
    end = 5
    count = 50
    xs = np.arange(begin, end, (end-begin)/count)
    ys = np.arange(begin, end, (end-begin)/count)
    space = []
    for x in xs:
        for y in ys:
            space.append((x, y))
    dom1 = [(1, 1.5), (2, 1.5), (1.5, 0.9)]
    cod1 = [ num_to_fuzzy(1.5), num_to_fuzzy(0.5), num_to_fuzzy(1.2)]
    f1 = fuzzy.FuzzySet(dom1, cod1, defZero=num_to_fuzzy(0))
    # plt.scatter(*zip(*dom))

    dom2 = [(6.6, 7.7), (6.8, 7.5), (7, 7.8)]
    cod2 = [num_to_fuzzy(2), num_to_fuzzy(3), num_to_fuzzy(2)]
    f2 = fuzzy.FuzzySet(dom2, cod2, defZero=num_to_fuzzy(0))
    # plt.scatter(*zip(*dom))

    dom3 = [(4, 4), (4.1, 3.9), (3.7, 4.2)]
    cod3 = [num_to_fuzzy(1.6), num_to_fuzzy(1), num_to_fuzzy(1)]
    f3 = fuzzy.FuzzySet(dom3, cod3, defZero=num_to_fuzzy(0))

    return algorithm.PartitioningAlgorithm(space, [f1, f3])

class AlgorithmTest(unittest.TestCase):

    
    def test_integration(self):
        alg = dupa()
        print(alg.phi((3.3, 3), 0) <= alg.phi((3.3, 3), 1))
        print(alg.phi((3.4, 3), 0) <= alg.phi((3.4, 3), 1))
        lab = alg.run()
        for (p, l) in lab:
            print(p)
            if p == (3.3, 3):
                print("label ", l)
        
        