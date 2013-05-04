import os
os.environ['DATABASE_URI']='postgresql+psycopg2://admin:admin@localhost/sgptest'
import index
import unittest
import tempfile
import CtrlAdmRol
import CtrlAdmUsr
import CtrlAdmTipoItem
from Modelo import init_db, drop_db, engine
 
class SGPTestCase(unittest.TestCase):

    """----------Funciones para las pruebas---------"""
    def setUp(self):
        self.engine = engine
        drop_db()
        init_db()
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

    def insertarUsr(self, opcion, username, passwrd, nombre, apellido, telefono, ci):
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
        
    def crearTipoItem(self, opcion, nombre, descripcion, idtipoitem):
        return self.app.post('/crearTipoItem',
                             data=dict(
                                       opcion=opcion,
                                       nombre=nombre,
                                       descripcion=descripcion,
                                       idtipoitemtemp=idtipoitem),
                             follow_redirects=True)
        
    def crearItem(self, opcion, nombre, tipoItem, descripcion, costo, prioridad, complejidad):
        return self.app.post('/crearItem',
                             data=dict(
                                       opcion=opcion,
                                       nombre=nombre,
                                       tipoItem=tipoItem,
                                       descripcion=descripcion,
                                       costo=costo,
                                       prioridad=prioridad,
                                       complejidad=complejidad),
                             follow_redirects=True)

    """---------Test---------"""
    def test_insertarUsr(self):
        rv = self.insertarUsr('Crear',
                            'test1-username', 
                            'test1-password', 
                            'test1-nombre', 
                            'test1-apellido', 
                            'test1-telefono', 
                            '1000')
        assert 'Usuario creado' in rv.data
        
    def test_login(self):
        #creando escenario
        idusuario=CtrlAdmUsr.insertarUsr('test2-username',
                                         'test2-password',
                                         'test2-nombre',
                                         'test2-apellido',
                                         'test2-telefono',
                                         '1000')
        #prueba
        rv = self.login('test2-username', 'test2-password')
        assert 'Estas logueado' in rv.data
        
    def test_logout(self):
        rv = self.logout()
        assert 'Estas deslogueado' in rv.data


    def test_modUsr(self):
        #creando escenario
        idusuario=CtrlAdmUsr.insertarUsr('test4-username',
                                         'test4-password',
                                         'test4-nombre',
                                         'test4-apellido',
                                         'test4-telefono',
                                         '1000')
        rv = self.modUsr('Modificar', 
                         idusuario,
                         'test4-usernamemod',
                         'test4-passwordmod',
                         'test4-nombremdo', 
                         'test4-apellidomod', 
                         'test4-telefonomod', 
                         '1000')
        assert 'Usuario modificado' in rv.data
        
    def test_crearRol(self):
        #creando escenario, se crean los permisos 200,201,202 y 203
        CtrlAdmRol.insertarPermiso(200,'','')
        CtrlAdmRol.insertarPermiso(201,'','')
        CtrlAdmRol.insertarPermiso(202,'','')
        CtrlAdmRol.insertarPermiso(203,'','')
        #pruebara no tenemos tiempo para eso :( ... creo que yo le toque en bus
        rv = self.crearRol('Crear', 
                         "test5-nombre",
                         "test5-descripcion",
                         ['201','202','203'])
        assert 'Rol creado' in rv.data
                
    def test_asigRoles(self):
        # creando escenario
        idusuario=CtrlAdmUsr.insertarUsr('test6-username',
                                         'test6-password',
                                         'test6-nombre',
                                         'test6-apellido',
                                         'test6-telefono',
                                         '1000')
        idrol=CtrlAdmRol.insertarRol('test6-nombre',
                    'test6-descripcion',
                    ['200','201','202'])
        #pruebas
        rv = self.asigRoles('Aceptar', 
                         idusuario,
                         [idrol])
        assert 'Roles asignados al usuario' in rv.data
       
    def test_modRol(self):
        # crear escenario
        idrol=CtrlAdmRol.insertarRol('test7-nombre',
                    'test7-descripcion',
                    ['200','201','202'])
        # prueba      setupTestDB()
        rv = self.modRol('Modificar', 
                           idrol,
                         "test7-nombre-modificado",
                         "test7-descripcion=-modificado",
                         ['202','203'])
        assert 'Rol modificado' in rv.data
        
    def test_crearProy(self):
        #crear escenario
        idusuario=CtrlAdmUsr.insertarUsr('test8-username',
                                 'test8-password',
                                 'test8-nombre',
                                 'test8-apellido',
                                 'test8-telefono',
                                 '1000')
        #prueba
        rv = self.login('test8-username', 'test8-password')
        rv = self.crearProy('Crear', 
                           "test8-nombre",
                         "test8-descripcion",
                         '1000')
        assert 'Proyecto creado' in rv.data
        
    def test_crearTipoItem(self):
        #crear escenario
        idusuario=CtrlAdmUsr.insertarUsr('test9-username',
                                 'test9-password',
                                 'test9-nombre',
                                 'test9-apellido',
                                 'test9-telefono',
                                 '1000')
        idtipoitem=CtrlAdmTipoItem.crearTipoItem('test9-nombre',
                                                 'test9-descripcion')
        #prueba
        rv = self.login('test9-username', 'test9-password')
        rv = self.crearTipoItem('Crear',
                              'test9-nombre',
                              'test9-descripcion',
                              idtipoitem)
        assert 'Tipo de Item Creado' in rv.data
        
    def crearItem(self):
        #crear escenario
        idusuario=CtrlAdmUsr.insertarUsr('test10-username',
                                 'test10-password',
                                 'test10-nombre',
                                 'test10-apellido',
                                 'test10-telefono',
                                 '1000')
        idtipoitem=CtrlAdmTipoItem.crearTipoItem('test10-nombre',
                                                 'test10-descripcion')
        #prueba
        rv=self.crearItem('Crear', 'nombre', idtipoitem, 'descripcion', '1', '1', '1')
        assert 'Debe Cargar Valores a los Atributos de Tipo de Item' in rv.data
    
        
        
        
if __name__ == '__main__':
    unittest.main()

    
    
