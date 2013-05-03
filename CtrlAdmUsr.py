from Modelo import Usuario, Permiso, Rol, engine, Proyecto, Fase
from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker, join

"""Controlador de Administrador de Usuario."""  
__author__ = 'Grupo 5'
__date__ = '04-04-2013'
__version__ = '1.0'
__text__ = 'Este modulo contiene funciones que permiten el control de administracion de usuarios'
__file__ = 'CtrlAdmUsr.py'      
    
#engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgptest')

Session = sessionmaker(bind=engine)
session = Session()

def getUsuarioList():
    """Funcion que retorna la lista de todos los usuarios en la base de datos."""
    result = session.query(Usuario).all()
    return result

def validarUsuario(username, password):
    """Funcion que retorna verdadero si el usuario y password son correctos."""
    usr = session.query(Usuario).filter(and_(Usuario.username==username,Usuario.passwrd==password)).first()
    return (usr!=None)

def idRolList(idusuario):
    """Funcion que recibe el Id de un Rol y retorna la lista de rolpermisos del rol"""
    usr = session.query(Usuario).filter(Usuario.idusuario==idusuario).first()
    idRolList=[]
    for rol in usr.roles:
        idRolList.append(rol.idrol)
    return idRolList

# def buscarUsuario(username):
#     """Funcion para loguearse:retorna verdadero si el usuario se encuentra en la BD"""
#     usuarioList = getUsuarioList()
#     for user in usuarioList:
#         if username == user.username:
#             return True
#     return False

def getMayorIdUsuario():
    """Funcion que retorna el mayor idusuario en la tabla usuarios"""
    lista = getUsuarioList()
    idusuariomax =0
    for user in lista:
        if idusuariomax < user.idusuario:
            idusuariomax = user.idusuario
    return idusuariomax   

def crearUsr(username,passwrd,nombre,apellido,telefono,ci):
    """Funcion que recibe los atributos de un usuario y lo periste en la base de datos."""
    idusuariomax=getMayorIdUsuario()
    nuevo = Usuario(idusuariomax+1,username,passwrd,nombre,apellido,telefono,ci)
    session.add(nuevo)
    session.commit()
    return idusuario

def elimUsr(iduser):
    """Funcion que recibe el Id de un Usuario y elimina de la base de datos"""
    res = session.query(Usuario).filter(Usuario.idusuario==iduser).first()
    session.delete(res)
    session.commit()
    
def modUsr(iduser,username,passwrd,nombre,apellido,telefono,ci):
    """Funcion que recibe los atributos de un usuario y lo modifica en la base de datos"""
    usr = session.query(Usuario).filter(Usuario.idusuario==iduser).first()
    usr.username = username
    usr.passwrd = passwrd
    usr.nombre = nombre
    usr.apellido = apellido
    usr.telefono = telefono
    usr.ci = ci
    session.commit()
    
    
def asigRoles(iduser,idRolList):
    """Funcion que recibe los roles a asignarse a un usuario """
    usr = session.query(Usuario).filter(Usuario.idusuario==iduser).first()
    listaroles = session.query(Rol).filter(Rol.idrol.in_(idRolList)).all()
    usr.roles = listaroles
    session.commit()
# 
# def getId(iduser):
#     s = select([usuario_table],usuario_table.c.idusuario==iduser)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['idusuario']
# def getUsername(iduser):
#     s = select([usuario_table],usuario_table.c.idusuario==iduser)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['username']
# def getPasswrd(iduser):
#     s = select([usuario_table],usuario_table.c.idusuario==iduser)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['passwrd']
# def getNombre(iduser):
#     s = select([usuario_table],usuario_table.c.idusuario==iduser)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['nombre']
# def getApellido(iduser):
#     s = select([usuario_table],usuario_table.c.idusuario==iduser)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['apellido']
# def getTelefono(iduser):
#     s = select([usuario_table],usuario_table.c.idusuario==iduser)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['telefono']
# def getCi(iduser):
#     s = select([usuario_table],usuario_table.c.idusuario==iduser)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['ci']

def busquedaUsr(parametro,atributo):
    if atributo == 'nombre':
        result = session.query(Usuario).filter(Usuario.nombre.like(parametro+'%')).all()
    if atributo == 'apellido':
        result = session.query(Usuario).filter(Usuario.apellido.like(parametro+'%')).all()
    if atributo == 'username':
        result = session.query(Usuario).filter(Usuario.username.like(parametro+'%')).all()
    return result

def usr(iduser):
    """Funcion que recibe el Id de un Usuario y retorna el objeto usuario"""
    usr = session.query(Usuario).filter(Usuario.idusuario==iduser).first()
    return usr
        
def havePermission(usr,permiso):
    """Funcion que recibe como parametro un username y el codigo de un permiso y
    verifica si el usuario puede tiene acceso a ese permiso"""
    lista = session.query(Usuario).join((Rol,Usuario.roles)).join((Permiso, Rol.permisos)).filter(Permiso.idpermiso==permiso).all()
    for user in lista:
        if user.username == usr:
            return True
    return False
    
def getIdByUsername(usrname):
    """Funcion que retorna un idusuario dado un username"""
    usr = session.query(Usuario).filter(Usuario.username==usrname).first()
    if(usr != None):
        return usr.idusuario
    else:
        raise Exception('No existe este usuario')

def tienePermisoEnFase(idfase,username,idpermiso):
    """Funcion que indica si un usuario tiene permisos para
    una determinada accion en una fase.
    Para eso debe reunir al menos una de estas condiciones:
    1)El usuario es el lider del proyecto; o
    2)El usuario posee un rol que esta asignado a esa fase y ese rol
    posee el permiso requerido"""
    fase = session.query(Fase).filter(Fase.idfase==idfase).first()
    proyecto = session.query(Proyecto).filter(Proyecto.idproyecto==fase.idproyecto).first()
    iduser=getIdByUsername(username)
    if(iduser==proyecto.usuariolider):
        return True
    rolesFase=fase.roles
    rolesUsuario=usr(iduser).roles
    for rolfase in rolesFase:
        for rolusuario in rolesUsuario:
            if(rolfase.idrol==rolusuario.idrol):
                listaperm=rolfase.permisos
                for permiso in listaperm:
                    if(permiso.idpermiso==idpermiso):
                        return True
    return False

#===============================================================================
# Funciones utilizadas en test
#===============================================================================
    
def cleanScenarioUser(username):
    try:
        iduser=CtrlAdmUsr.getIdByUsername(username)
    except:
        iduser=None
    if(iduser!=None):
        CtrlAdmUsr.elimUsr(username)
        
def createScenarioUser(idusuario,username,passwrd,nombre,apellido,telefono,ci):
    nuevo=Usuario(idusuario,username,passwrd,nombre,apellido,telefono,ci)
    session.add(nuevo)
    session.commit()