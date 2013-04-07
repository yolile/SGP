'''
Created on 05/04/2013

@author: thelma

Controla si un usuario es creado correctamente
'''
import unittest
from CtrlAdmUsr import crearUsr,getMayorIdUsuario,getUsername,getPasswrd,getNombre,getApellido,getTelefono,getCi,eliminarUsr
class crearUsrTest(unittest.TestCase):
    global id_user
    def createScenario(self):
        crearUsr('usuario','1234','diana','noguera','123098','87877')
        idusuario=getMayorIdUsuario()
        return idusuario
    
    def checkResults(self,idusuario):   
        username = getUsername(idusuario)
        passwrd = getPasswrd(idusuario)
        nombre = getNombre(idusuario)
        apellido = getApellido(idusuario)
        telefono = getTelefono(idusuario)
        ci = getCi(idusuario)
        assert username == 'usuario', 'ERROR:El username no es el esperado, se esperaba: usuario, se obtuvo: ' + username
        assert passwrd == '1234', 'ERROR:El password no es el esperado, se esperaba: 1234, se obtuvo: ' + passwrd
        assert nombre == 'diana', 'ERROR:El nombre no es el esperado, se esperaba: diana, se obtuvo: ' + nombre
        assert apellido == 'noguera', 'ERROR:El apellido no es el esperado, se esperaba: noguera, se obtuvo: ' + apellido
        assert telefono == '123098', 'ERROR:El telefono no es el esperado, se esperaba: 123098, se obtuvo: ' + telefono
        assert ci == 87877, 'ERROR:El ci no es el esperado, se esperaba: 87877, se obtuvo: ' + str(ci)
        
    def cleanScenario(self,iduser):
        eliminarUsr(iduser)
        
    def runTest(self):
        self.cleanScenario(getMayorIdUsuario())
        id_user = self.createScenario()
        self.checkResults(id_user)
        self.cleanScenario(id_user)
            
def makeCrearUsrTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(crearUsrTest())
    return suite

if __name__ == '__main__':
    # When this module is executed from the command-line, run all its tests
    unittest.main()