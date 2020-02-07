#!/usr/bin/python3

import numpy as np
# from types import Callable
import matplotlib.pyplot as plt
import fuzzyComparator
import copy

class NotUniqueDomainException(Exception):
    ...

class FuzzySet:
    'Descrete Fuzzy Set implementation'

    def __init__(self, domain, codomain, defZero):
        if(len(domain) != len(codomain)):
            raise AttributeError("Lengths of domain and codomain are different")
        
        # i should have check uniqueness. How?
        self.rejectIfNotUnique(domain)
        l = list(zip(domain, codomain))
        self.charFun = l
        
        self.default = defZero
    

    def inSet(self, _point):
        for (point, v) in self.charFun:
            # print("point, _point: ", point, _point)
            if point == _point:
                return v
        return self.default
    def __call__(self, x):
        return self.inSet(x)


    def unzip(self):
        return list(zip(* self.charFun))

    def domain(self):
        return self.unzip()[0]
    def codomain(self):
        return self.unzip()[1]

    def __eq__(self, other):
        for x in self.domain():
            if other.inSet(x) != self.inSet(x):
                return False
        for x in other.domain():
            if other.inSet(x) != self.inSet(x):
                return False
        return True
    
    def __ne__(self, other):
        return not self == other
    
    def rejectIfNotUnique(self, dom):
        # c = 9
        d = sorted(dom)
        for i in range(len(d) -1):
            if d[i] == d[i+1]:
                raise NotUniqueDomainException(str(dom)) 



class FuzzyNumber(FuzzySet):
    
    comparator = fuzzyComparator.centerOfMaxima

    def __init__(self, dom, cod):
        (d, c) = self.checkUniqueness(list(zip(dom, cod)))
        super().__init__(d, c, defZero=0)

    def map(self, fun):
        l = list(map(lambda v : (fun(v[0]), v[1]), self.charFun))
        (dom, cod) = self.checkUniqueness(l)
        self.charFun = list(zip(dom, cod))

    def __le__(self, other):
        return FuzzyNumber.comparator(other, self)
    def __lt__(self, other):
        return self != other and self <= other
    def __ge__(self, other):
        return FuzzyNumber.comparator(self, other)
    def __gt__(self, other):
        return self != other and self >= other
    def __neg__(self):
        self.map(lambda x: -x)
        return self
    def __add__(self, other):
        newCharFun = []
        for (x1, y1) in self.charFun:
            for (x2, y2) in other.charFun:
                newCharFun.append((x1 + x2, min(y1, y2)))
        (dom, cod) = self.checkUniqueness(newCharFun)
        return FuzzyNumber(dom, cod)

    def times(self, num):
        new = copy.deepcopy(self)
        new.map(lambda x : x*num)
        return new
        

    def print(self):
        (xs, ys) = self.unzip()
        plt.plot(xs, ys, '.')
        plt.show()

    def alphaCut(self, alpha):
        s = []
        for (x, y) in self.charFun:
            if y >= alpha:
                s.append(x)
        return np.array(s)
    
    def getMaxEndpoint(self, alpha):
        return self.alphaCut(alpha).max()
    def getMinEndpoint(self, alpha):
        return self.alphaCut(alpha).min()

    def possibility(self, event):
        return max([self(x) for x in event])
    def necessity(self, event):
        return 1 - max([self(x) for x in self.domain() if x not in event ])


    def integrate(self):
        return np.array(self.charFun).sum(axis=0)[1]
    
    def expectedVal(self):
        return np.array(self.charFun).prod(axis=1).sum()
    
    def generalizedExpected(self, g):
        return np.array(list(map(lambda x: g(x[0]) * x[1], self.charFun))).sum()
    def checkUniqueness(self, charFun):
        newCharFun = np.array(sorted(charFun, key=lambda x : x[0])) # sort by domain
        dom = []
        cod = []
        for i in range(len(newCharFun)-1):
            (x, y) = newCharFun[i]
            if x == newCharFun[i+1][0]:
                newCharFun[i+1][1] = max(y, newCharFun[i+1][1])
            else:
                dom.append(x)
                cod.append(y)
        # i may have missed last one
        if not dom or dom[-1] != newCharFun[-1][0]:
            dom.append(newCharFun[-1][0])
            cod.append(newCharFun[-1][1])
        return (dom, cod)
    

def num_to_fuzzy(num):
    return FuzzyNumber([num], [1])
def empty_number():
    return FuzzyNumber([], [])

def integratFuzzyFunction(X, fun) -> FuzzyNumber:
    sum = num_to_fuzzy(0)
    for x in X:
        sum = sum + fun(x)
    return sum