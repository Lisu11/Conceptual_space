#!/usr/bin/python3

import numpy as np
import fuzzy

def euclidianMetric(p, q):
    return np.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)

def supMetric(fn1, fn2):
    xs = fn1.domain() + fn2.domain()
    return max([abs(fn1(x) - fn2(x)) for x in xs])



def fuzzyMetric(f1, f2):
    (p, f) = f1
    (q, h) = f2
    d2 = euclidianMetric(p, q)
    ds = supMetric(f, h)
    return d2 + ds