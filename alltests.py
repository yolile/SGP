'''
Created on 05/04/2013

@author: thelma

Ejecuta todos los tests
'''

import unittest

def suite():
    modules_to_test = ('crearUsrTest','eliminarUsrTest') # and so on
    alltests = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
