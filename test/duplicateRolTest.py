#!flask/bin/python

import unittest

from CtrlAdmRol import crearRol,elimRol

"""La siguiente prueba ingresa dos roles identicos y comprueba
si se lanza el error esperado que es -1, error de integridad"""

class duplicateRolTest(unittest.TestCase):
    nuevoidrol=0
    permisoList=[201,202]
    def setUp(self):
        self.nuevoidrol=crearRol('ROL1','TESTROL',self.permisoList)

    def tearDown(self):
        elimRol(self.nuevoidrol)

    def test_duplicate(self):
        variable=crearRol('ROL1','TESTROL',self.permisoList)
        assert variable==-1, 'ERROR:Se esperaba error -1 (error de integridad),no se obtuvieron errores'
        print('SGP:Test finalizado sin errores')
    def runTest(self):
        self.setUp()
        self.test_duplicate()
        self.tearDown()
        
    
def makeDuplicateRolTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(duplicateRolTest())
    return suite

if __name__ == '__main__':
    unittest.main()