import os
import index
import unittest
import tempfile
import CtrlAdmProy
import CtrlAdmRol
import CtrlAdmUsr

def tearDown():
    CtrlAdmUsr.truncarUsuario()
    CtrlAdmRol.truncarRol()
    CtrlAdmUsr.truncarRolUsuario()
    CtrlAdmRol.truncarRolPermiso()
    CtrlAdmProy.truncarProyecto()
    CtrlAdmProy.truncarFase()
        
class SGPTestCase(unittest.TestCase):

    """----------Funciones para las pruebas---------"""
    def setUp(self):
        index.app.config['TESTING'] = True
        self.app = index.app.test_client()
        
    def login(self, username, password):
        return self.app.post('/login', 
                             data=dict(
                                       username=username,
                                       password=password), 
                            follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def crearUsr(self, opcion, username, passwrd, nombre, apellido, telefono, ci):
        return self.app.post('/crearUsr', 
                             data=dict(
                                       opcion=opcion,
                                       username=username,
                                       passwrd=passwrd,
                                       nombre=nombre,
                                       apellido=apellido,
                                       telefono=telefono,
                                       ci=ci), 
                            follow_redirects=True)

    def modUsr(self, opcion, idusuario, username, passwrd, nombre, apellido, telefono, ci):
        return self.app.post('/modUsr', 
                             data=dict(
                                       opcion=opcion,
                                       idusuario=idusuario,
                                       username=username,
                                       passwrd=passwrd,
                                       nombre=nombre,
                                       apellido=apellido,
                                       telefono=telefono,
                                       ci=ci), 
                            follow_redirects=True)

    def asigRoles(self, opcion, idusuario, roles):
        return self.app.post('/asigRoles', 
                             data=dict(
                                       opcion=opcion,
                                       idusuario=idusuario,
                                       roles=roles
                                       ), 
                            follow_redirects=True)

    def crearRol(self, opcion, nombre, descripcion, permisos):
        return self.app.post('/crearRol', 
                             data=dict(
                                       opcion=opcion,
                                       nombre=nombre,
                                       descripcion=descripcion,
                                       permisos=permisos
                                       ), 
                            follow_redirects=True)

    def modRol(self, opcion, idrol, nombre, descripcion, permisos):
        return self.app.post('/modRol', 
                             data=dict(
                                       opcion=opcion,
                                       idrol=idrol,
                                       nombre=nombre,
                                       descripcion=descripcion,
                                       permisos=permisos
                                       ), 
                            follow_redirects=True)

    def crearProy(self, opcion, nombre, descripcion, presupuesto):
        return self.app.post('/crearProy', 
                             data=dict(
                                       opcion=opcion,
                                       nombre=nombre,
                                       descripcion=descripcion,
                                       presupuesto=presupuesto), 
                            follow_redirects=True)

    def crearFase(self, opcion, idproyecto, nombre, descripcion):
        return self.app.post('/crearFase', 
                             data=dict(
                                       opcion=opcion,
                                       idproyecto=idproyecto,
                                       nombre=nombre,
                                       descripcion=descripcion), 
                            follow_redirects=True)

    """---------Test---------"""
    def test_crearUsr(self):
        tearDown()
        rv = self.crearUsr('Crear',
                            'prueba', 
                            'prueba', 
                            'Usuario', 
                            'Prueba', 
                            '99999999', 
                            '9999999')
        assert 'Usuario creado' in rv.data
        tearDown()

    def test_login(self):
        tearDown()
        CtrlAdmUsr.insertarUsuario('1','prueba','prueba','nombre','apellido','111','222')
        rv = self.login('prueba', 'prueba')
        assert 'Estas logueado' in rv.data
        tearDown()
        
    def test_logout(self):
        rv = self.logout()
        assert 'Estas deslogueado' in rv.data
    
    def test_modUsr(self):
        tearDown()
        rv = self.modUsr('Modificar', 
                         '2',
                         'prueba', 
                         'prueba', 
                         'Usuario', 
                         'Prueba', 
                         '88888888', 
                         '8888888')
        assert 'Usuario modificado' in rv.data
        tearDown()
        
    def test_crearRol(self):
        tearDown()
        rv = self.crearRol('Crear', 
                         "Rol Prueba",
                         "Este rol fue creado con la intencion de hacer pruebas en el caso de uso crear rol",
                         ['201','202','203'])
        assert 'Rol creado' in rv.data
        tearDown()
    
    def test_asigRoles(self):
        tearDown()
        permisos=[200,201]
        CtrlAdmRol.insertarRol('101','rol de prueba','rol de prueba',permisos)
        CtrlAdmUsr.insertarUsuario('2','prueb','123','prueba','unitaria','1','3000')
        rv = self.asigRoles('Aceptar', 
                         "2",
                         ['101'])
        assert 'Roles asignados al usuario' in rv.data
        tearDown()
       
    def test_modRol(self):
        tearDown()
        rv = self.modRol('Modificar', 
                           "101",
                         "Rol Prueba Modificado",
                         "Este rol fue creado con la intencion de hacer pruebas en el caso de uso modificar rol",
                         ['202','203'])
        assert 'Rol modificado' in rv.data   
        tearDown()
    
    def test_crearProy(self):
        tearDown()
        CtrlAdmUsr.insertarUsuario('2','prueba','prueba','prueba','unitaria','1','3000')
        rv = self.login('prueba', 'prueba')
        rv = self.crearProy('Crear', 
                           "Proyecto prueba",
                         "Este proyecto fue creado con la intencion de hacer pruebas en el caso de uso crear proyecto",
                         '1000')
        assert 'Proyecto creado' in rv.data 
        tearDown()

if __name__ == '__main__':
    unittest.main()
    
