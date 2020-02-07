#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import fuzzy as f 


def adamo(f1, f2, alpha=0.5) -> bool:
    return f1.getMaxEndpoint(alpha) >= f2.getMaxEndpoint(alpha)

def  centerOfMaxima(f1 , f2, alpha=0.5 ) -> bool:
    a1 = (f1.getMinEndpoint(alpha) + f1.getMaxEndpoint(alpha))/2
    a2 = (f2.getMinEndpoint(alpha) + f2.getMaxEndpoint(alpha))/2

    return a1 >= a2

def centerOfGravity(f1 , f2 ) -> bool:
    frac1 = f1.expectedVal()/ f1.integrate()
    frac2 = f2.expectedVal()/ f2.integrate()
    # print("frac1, frac2: ", frac1, frac2)
    return frac1 >= frac2

def yager1(f1 , f2 , fun) -> bool:
    frac1 = f1.generalizedExpected(fun)/ f1.integrate()
    frac2 = f2.generalizedExpected(fun)/ f2.integrate()
    
    return frac1 >= frac2

def chang(f1 , f2) -> bool:
    return f1.expectedVal() >= f2.expectedVal()