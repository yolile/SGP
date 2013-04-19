'''
Created on 05/04/2013

@author: thelma

Controla si un usuario es eliminado correctamente
'''
import unittest
from CtrlAdmUsrTest import crearUsr,buscarUsuario,getMayorIdUsuario,getUsername,getPasswrd,getNombre,getApellido,getTelefono,getCi,eliminarUsr

class crearUsrTest(unittest.TestCase):
    global id_user
    def createScenario(self):
        crearUsr('usuario','1234','diana','noguera','123098','87877')
        idusuario=getMayorIdUsuario()
        return idusuario
    
    def checkResults(self,idusuario):   
        assert buscarUsuario(idusuario)==False, 'ERROR: El usuario no fue eliminado'

    def cleanScenario(self,iduser):
        eliminarUsr(iduser)
        
    def runTest(self):
        id_user = self.createScenario()
        eliminarUsr(id_user)
        self.checkResults(id_user)
            
def makeCrearUsrTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(crearUsrTest())
    return suite

if __name__ == '__main__':
    # Cuando este modulo se ejecuta directamente, corren todos sus tests
    unittest.main()