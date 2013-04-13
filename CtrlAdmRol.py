from Rol import Rol, get_table 
from RolPermiso import RolPermiso, get_table
from Permiso import Permiso, get_table 
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.sql import select
   
    
engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgp')
metadata = MetaData(bind=engine)
usuario_table = get_table(metadata)
mapper(Usuario, usuario_table)
conn = engine.connect()

def getRolList():
    """Funcion que retorna la lista de todos los roles en la base de datos."""
    s = select([rol_table])
    result = s.execute()
    return result

def buscarUsuario(username):
    """Funcion que retorna verdadero si el usuario se encuentra en la BD"""
    usuarioList = getUsuarioList()
    for user in usuarioList:
        if username == user.username:
            return True
    return False

def getMayorIdRol():
    """Funcion que retorna el mayor idRol en la tabla usuarios"""
    lista = getUsuarioList()
    idusuariomax =0
    for user in lista:
        if idusuariomax < user.idusuario:
            idusuariomax = user.idusuario
    return idusuariomax   

def getIdRol(idrol):
    s = select([rol_table],rol_table.c.idrol==idrol)
    result = conn.execute(s)
    row = result.fetchone()
    return row['idrol']
def getNombreRol(idrol):
    s = select([rol_table],rol_table.c.idrol==idrol)
    result = conn.execute(s)
    row = result.fetchone()
    return row['nombre']
def getDescripcionRol(idrol):
    s = select([rol_table],rol_table.c.idrol==idrol)
    result = conn.execute(s)
    row = result.fetchone()
    return row['descripcion']

def rol(idRol):
    """Funcion que recibe el Id de un Rol y retorna el objeto rol"""
    lista = getRolList()
    for rol in lista:
        if idRol == rol.idrol:
            return rol
def permiso(idPermiso):
    """Funcion que recibe el Id de un Permiso y retorna el objeto Permiso"""
    lista = getPermisoList()
    for permiso in lista:
        if idpermiso == permiso.idpermiso:
            return permiso