#from Rol import Rol, get_table 
import Rol
#from RolPermiso import RolPermiso, get_table
import RolPermiso 
import Permiso
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.sql import select
from sqlalchemy import exc
   
    
engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgptest')
metadata = MetaData(bind=engine)

rol_table = Rol.get_table(metadata)
mapper(Rol.Rol, rol_table)

permiso_table = Permiso.get_table(metadata)
mapper(Permiso.Permiso, permiso_table)

rolpermiso_table = RolPermiso.get_table(metadata)
mapper(RolPermiso.RolPermiso, rolpermiso_table)

conn = engine.connect()

def getRolList():
    """Funcion que retorna la lista de todos los roles en la base de datos."""
    s = select([rol_table])
    result = s.execute()
    return result

def getPermisoList():
    """Funcion que retorna la lista de todos los permisos en la base de datos."""   
    s = select([permiso_table])
    result = s.execute()
    return result

def getRolPermisoList():
    """Funcion que retorna la lista de todos los rolpermisos en la base de datos."""   
    s = select([rolpermiso_table])
    result = s.execute()
    return result

def getMayorIdRol():
    """Funcion que retorna el mayor idRol en la tabla roles"""
    lista = getRolList()
    idrolmax =0
    for rol in lista:
        if idrolmax < rol.idrol:
            idrolmax = rol.idrol
    return idrolmax   

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
        
def crearRol(nombre,descripcion,idPermisoList):
    """Funcion que recibe los atributos de un usuario y lo persiste en la base de datos.
    Retorna el nuevo idrol en caso de exito y -1 en caso de error de integridad"""
    try:
        idrolmax=getMayorIdRol()
        result = rol_table.insert().execute(idrol=idrolmax+1,
                                                 nombre=nombre,
                                                 descripcion=descripcion)
        
        for idpermiso in idPermisoList:
            result = rolpermiso_table.insert().execute(idrol=idrolmax+1,
                                                 idpermiso = int(idpermiso))
    except exc.SQLAlchemyError:
        return -1
    return idrolmax+1

def idPermisoList(idRol):
    """Funcion que recibe el Id de un Rol y retorna la lista de rolpermisos del rol.
    En caso de malos parametros, captura el error y retorna -1, en caso de 
    exito, retorna la lista de permisos"""
    try:
        lista = getRolPermisoList()
        idPermisoList=[]
        for rolpermiso in lista:
            if(rolpermiso.idrol == idRol):
                idPermisoList.append(rolpermiso.idpermiso)
    except ValueError:
        return -1
    return idPermisoList

def modRol(idrol,nombre,descripcion,idPermisoList):
    """Funcion que recibe los atributos de un usuario y lo modifica en la base de datos"""
    conn.execute(rol_table.update().
                    where(rol_table.c.idrol==idrol).
                    values(nombre=nombre,
                           descripcion=descripcion)
                )
    conn.execute(rolpermiso_table.delete().where(rolpermiso_table.c.idrol==idrol))
    for idpermiso in idPermisoList:
        result = rolpermiso_table.insert().execute(idrol=idrol,
                                             idpermiso = int(idpermiso))
        
def elimRol(idrol):
    """Funcion que recibe un idrol y lo elimina de la base de datos,
    Retorna 0 en caso de exito.
    Retorna -1 si no se encuentra el rol a eliminar"""
    try:
        conn.execute(rolpermiso_table.delete().where(rolpermiso_table.c.idrol==idrol)) 
        conn.execute(rol_table.delete().where(rol_table.c.idrol==idrol))
    except Exception:
        return -1
    return 0
        
    