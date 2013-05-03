import os
import index
import unittest
import tempfile
import CtrlAdmProy
import CtrlAdmRol
import CtrlAdmUsr
        
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
        CtrlAdmUsr.cleanScenarioUser('prueba')
        rv = self.crearUsr('Crear',
                            'prueba', 
                            'prueba', 
                            'Usuario', 
                            'Prueba', 
                            '99999999', 
                            '9999999')
        assert 'Usuario creado' in rv.data
        CtrlAdmUsr.cleanScenarioUser('prueba')

    def test_login(self):
        #limpiando escenario
        CtrlAdmUsr.cleanScenarioUser('prueba')
        #creando escenario
        CtrlAdmUsr.createScenarioUser('1','prueba','prueba','nombre','apellido','111','222')
        #prueba
        rv = self.login('prueba', 'prueba')
        assert 'Estas logueado' in rv.data
        #limpiando escenario
        CtrlAdmUsr.cleanScenarioUser('prueba')
        
    def test_logout(self):
        rv = self.logout()
        assert 'Estas deslogueado' in rv.data
    
    def test_modUsr(self):
        #limpiando escenario
        CtrlAdmUsr.cleanScenarioUser('prueba')
        #creando escenario
        CtrlAdmUsr.createScenarioUser('2','prueba','prueba','Usuario','Prueba','88888888','8888888')
        #el test
        rv = self.modUsr('Modificar', 
                         '2',
                         'prueba',
                         'prueba', 
                         'Usuario', 
                         'Prueba', 
                         '88888888', 
                         '8888888')
        assert 'Usuario modificado' in rv.data
        #limpiando escenario
        CtrlAdmUsr.cleanScenarioUser('prueba')
        
    def test_crearRol(self):
        rv = self.crearRol('Crear', 
                         "Rol Prueba",
                         "Este rol fue creado con la intencion de hacer pruebas en el caso de uso crear rol",
                         ['201','202','203'])
        assert 'Rol creado' in rv.data
        #limpiar escenario borrando el rol creado
        CtrlAdmRol.elimRol(CtrlAdmRol.getMayorIdRol())
    
    def test_asigRoles(self):
        #creando escenario
        if (CtrlAdmRol.idPermisoExiste(200)==False):
            CtrlAdmRol.insertarPermiso(200)
        if (CtrlAdmRol.idPermisoExiste(201)==False):
            CtrlAdmRol.insertarPermiso(201)
        if(CtrlAdmRol.idRolExiste==False):
            permisos=[200,201]
            CtrlAdmRol.insertarRol('101','rol de prueba','rol de prueba',permisos)
        if(CtrlAdmUsr.idUsuarioExiste==False):
            CtrlAdmUsr.createScenarioUser('2','prueb','123','prueba','unitaria','1','3000')
        #prueba
        rv = self.asigRoles('Aceptar', 
                         "2",
                         ['101'])
        assert 'Roles asignados al usuario' in rv.data
        #limpiando escenario
        CtrlAdmRol.elimRol(101)
        CtrlAdmUsr.elimUsr(2)      
       
    def test_modRol(self):
        # creando escenario
        if not(CtrlAdmRol.idRolExiste(101)):
            CtrlAdmRol.crearRol('101','','',[])
        if not(CtrlAdmRol.idPermisoExiste(202)):
            CtrlAdmRol.crearPermiso('202','','')
        if not(CtrlAdmRol.idPermisoExiste(203)):
            CtrlAdmRol.crearPermiso('203','','') 
        # prueba      
        rv = self.modRol('Modificar', 
                           "101",
                         "Rol Prueba Modificado",
                         "Este rol fue creado con la intencion de hacer pruebas en el caso de uso modificar rol",
                         ['202','203'])
        assert 'Rol modificado' in rv.data   
    
    def test_crearProy(self):
        #creando escenario
        CtrlAdmUsr.cleanScenarioUser('prueba')
        CtrlAdmUsr.createScenarioUser('2','prueba','prueba','prueba','unitaria','1','3000')
        #prueba
        rv = self.login('prueba', 'prueba')
        rv = self.crearProy('Crear', 
                           "Proyecto prueba",
                         "Este proyecto fue creado con la intencion de hacer pruebas en el caso de uso crear proyecto",
                         '1000')
        assert 'Proyecto creado' in rv.data 

if __name__ == '__main__':
    unittest.main()
    
