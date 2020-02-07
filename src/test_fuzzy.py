#!/usr/bin/python3

import unittest
import fuzzy
from fuzzy import num_to_fuzzy
import numpy as np

class FuzzySetTest(unittest.TestCase):
    def test_inSet(self):
        cod = list(map(fuzzy.num_to_fuzzy,\
             [0.5, 0.2, 0.4, 1, 1, 0.5, 0.2, 0.8, 0.4, 0.4]))
        dom = list(range(10))
        fuz = fuzzy.FuzzySet(dom, cod, fuzzy.num_to_fuzzy(0))
        for i in range(len(cod)):
            self.assertEqual(fuz(i), cod[i])
        # self.assertEqual(fuz.inSet(5), 0.5)

    def test_uniqueness(self):
        cod = list(map(fuzzy.num_to_fuzzy,\
             [0.5, 0.2, 0.4, 1, 1, 0.5, 0.2, 0.8, 0.4, 0.4]))
        dom = list(range(5)) + list(range(5))
        with self.assertRaises(fuzzy.NotUniqueDomainException):
            fuzzy.FuzzySet(dom, cod, fuzzy.num_to_fuzzy(0))
    
    def test_domain_codomain(self):
        dom = np.arange(-5, 5, .01)
        cod = list(map(fuzzy.num_to_fuzzy, np.exp(-0.5*(dom**2))))
        f =fuzzy.FuzzySet(dom, cod, fuzzy.num_to_fuzzy(0))
        domain = f.domain()
        codomain = f.codomain()

        for i in range(len(dom)):
            self.assertEqual(dom[i], domain[i])
            self.assertEqual(cod[i], codomain[i])
    
   
    # map has been moved to fuzzyNumber 

    # def test_map(self):
    #     cod = list(map(fuzzy.num_to_fuzzy,\
    #          [0.5, 0.2, 0.4, 1, 1, 0.5, 0.2, 0.8, 0.4, 0.4]))
    #     dom = list(range(10))
    #     fuz = fuzzy.FuzzySet(dom, cod, fuzzy.num_to_fuzzy(0))
    #     fuz.map(lambda x: fuzzy.num_to_fuzzy(1))
    #     self.assertEqual([fuzzy.num_to_fuzzy(1)]*10, list(fuz.domain()))
    
    def test_eq(self):
        cod = list(map(fuzzy.num_to_fuzzy,\
             [0.5, 0.2, 0.4, 1, 1, 0.5, 0.2, 0.8, 0.4, 0.4]))
        dom = list(range(10))
        fuz = fuzzy.FuzzySet(dom, cod, fuzzy.num_to_fuzzy(0))

        fuz2 = fuzzy.FuzzySet(list(range(11)),\
             cod + [fuzzy.num_to_fuzzy(0.2)], fuzzy.num_to_fuzzy(0))
        cod = list(map(fuzzy.num_to_fuzzy,\
             [0.5, 0.2, 0.4, 1, 1, 0.5, 0.1, 0.8, 0.4, 0.4]))
        fuz3 = fuzzy.FuzzySet(list(range(10)), cod, fuzzy.num_to_fuzzy(0))
        self.assertTrue(fuz == fuz)
        self.assertFalse(fuz == fuz2)
        self.assertFalse(fuz == fuz3)
    
    def test_neq(self):
        cod = list(map(fuzzy.num_to_fuzzy,\
             [0.5, 0.2, 0.4, 1, 1, 0.5, 0.2, 0.8, 0.4, 0.4]))
        dom = list(range(10))
        fuz = fuzzy.FuzzySet(dom, cod, fuzzy.num_to_fuzzy(0))

        fuz2 = fuzzy.FuzzySet(list(range(11)),\
             cod + [fuzzy.num_to_fuzzy(0.2)], fuzzy.num_to_fuzzy(0))
        cod = list(map(fuzzy.num_to_fuzzy,\
             [0.5, 0.2, 0.4, 1, 1, 0.5, 0.1, 0.8, 0.4, 0.4]))
        fuz3 = fuzzy.FuzzySet(list(range(10)), cod, fuzzy.num_to_fuzzy(0))
        self.assertTrue(fuz != fuz2)
        self.assertTrue(fuz != fuz3)
        self.assertTrue(fuz3 != fuz2)
    
    def test_input_list_of_tuples(self):
        dom = [(2, 7.8), (3, 7.5), (2.5, 7), (2.5, 7.5), (2.5, 8)]
        cod = [num_to_fuzzy(5), num_to_fuzzy(8), num_to_fuzzy(5), num_to_fuzzy(3), num_to_fuzzy(1)]
        f1 = fuzzy.FuzzySet(dom, cod, defZero=num_to_fuzzy(0))
        f1([2, 7.8])

class FuzzyNumberTest(unittest.TestCase):

    def test_uniqueness(self):
        f = fuzzy.FuzzyNumber([1,1], [0.8, 1])
        self.assertEqual(f, fuzzy.num_to_fuzzy(1))

    def test_alphaCut(self):
        vals = [0.5, 0.2, 0.4, 1, 1, 0.5, 0.2, 0.8, 0.4, 0.4]
        fuz = fuzzy.FuzzyNumber(list(range(10)), vals)
        alpha = fuz.alphaCut(0.5)
        vals = [0, 3, 4, 5, 7]
        for i in range(len(vals)):
            self.assertEqual(vals[i], alpha[i])

    def test_MaxEndpoint(self):
        dom = np.arange(-5, 5, .01)
        cod = np.exp(-0.5*(dom**2))
        f =fuzzy.FuzzyNumber(dom, cod)
        self.assertAlmostEqual(f.getMaxEndpoint(1), 0)
        self.assertAlmostEqual(f.getMinEndpoint(1), 0)
        # self.assertAlmostEqual(f.getMinEndpoint(np.exp(-2)), -2)

    def test_itegration(self):
        dom = np.arange(-5, 5, .01)
        cod = np.exp(-0.5*(dom**2))
        f =fuzzy.FuzzyNumber(dom, cod)
        # self.assertAlmostEqual(f.integrate(), 1)

    def test_map(self):
        vals = [0.5, 0.2, 0.4, 1, 1, 0.5, 0.2, 0.8, 0.4, 0.4]
        fuz = fuzzy.FuzzyNumber(list(range(10)), vals)
        fuz.map(lambda x: x+1)
        self.assertEqual(list(range(1,11)), list(fuz.domain()))
    
    def test_eq(self):
        vals = [0.5, 0.2, 0.4, 1, 1, 0.5, 0.2, 0.8, 0.4, 0.4]
        fuz = fuzzy.FuzzyNumber(list(range(10)), vals)
        fuz2 = fuzzy.FuzzyNumber(list(range(11)), vals + [0.2])
        vals = [0.5, 0.2, 0.4, 1, 1, 0.5, 0.1, 0.8, 0.4, 0.4]
        fuz3 = fuzzy.FuzzyNumber(list(range(10)), vals)
        self.assertTrue(fuz == fuz)
        self.assertFalse(fuz == fuz2)
        self.assertFalse(fuz == fuz3)
    
    def test_neq(self):
        vals = [0.5, 0.2, 0.4, 1, 1, 0.5, 0.2, 0.8, 0.4, 0.4]
        fuz = fuzzy.FuzzyNumber(list(range(10)), vals)
        fuz2 = fuzzy.FuzzyNumber(list(range(11)), vals + [0.2])
        vals = [0.5, 0.2, 0.4, 1, 1, 0.5, 0.1, 0.8, 0.4, 0.4]
        fuz3 = fuzzy.FuzzyNumber(list(range(10)), vals)
        self.assertTrue(fuz != fuz2)
        self.assertTrue(fuz != fuz3)
        self.assertTrue(fuz3 != fuz2)
    def test_domain_codomain(self):
        dom = np.arange(-5, 5, .01)
        cod = np.exp(-0.5*(dom**2))
        f =fuzzy.FuzzyNumber(dom, cod)
        domain = f.domain()
        codomain = f.codomain()

        for i in range(len(dom)):
            self.assertEqual(dom[i], domain[i])
            self.assertEqual(cod[i], codomain[i])
    
    def test_neg(self):
        dom = np.arange(-5, 5, .01)
        cod = np.exp(-0.5*(dom**2))
        f = fuzzy.FuzzyNumber(dom, cod)
        f =  - f
        domain = f.domain()
        codomain = f.codomain()

        for i in range(len(dom)):
            self.assertTrue(-domain[i] in dom)
            self.assertTrue(codomain[i] in cod)
    
    def test_addition(self):
        dom1 = [2,3,4]
        dom2 = [3,4,6]
        dom3 = [5,6,7,8,9,10]
        cod1 = [0.7, 1, 0.6]
        cod2 = [0.8, 1, 0.5]
        cod3 = [0.7, 0.8, 1, 0.6, 0.5, 0.5]

        f1 = fuzzy.FuzzyNumber(dom1, cod1)
        f2 = fuzzy.FuzzyNumber(dom2, cod2)
        f3 = fuzzy.FuzzyNumber(dom3, cod3)
        self.assertEqual(f1 + f2 , f3)
    
    def test_scalar(self):
        dom = [5,6,7,8,9,10]
        cod = [0.7, 0.8, 1, 0.6, 0.5, 0.5]
        f = fuzzy.FuzzyNumber(dom, cod)
        self.assertEqual(f.times(1), f)
        self.assertEqual(f.times(2), fuzzy.FuzzyNumber(range(10,21,2), cod))


if __name__ == '__main__':
    unittest.main()