from Modelo import Permiso, Rol, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
   
    
#engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgptest')

Session = sessionmaker(bind=engine)
session = Session()   

def getRolList():
    """Funcion que retorna la lista de todos los roles en la base de datos."""
    result = session.query(Rol).all()
    return result

def getPermisoList():
    """Funcion que retorna la lista de todos los permisos en la base de datos."""   
    result = session.query(Permiso).all()
    return result

# def getRolPermisoList():
#     """Funcion que retorna la lista de todos los rolpermisos en la base de datos."""   
#     s = select([rolpermiso_table])
#     result = s.execute()
#     return result

def getMayorIdRol():
    """Funcion que retorna el mayor idRol en la tabla roles"""
    lista = getRolList()
    idrolmax =0
    for rol in lista:
        if idrolmax < rol.idrol:
            idrolmax = rol.idrol
    return idrolmax   

# def getIdRol(idrol):
#     s = select([rol_table],rol_table.c.idrol==idrol)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['idrol']

# def getNombreRol(idrol):
#     s = select([rol_table],rol_table.c.idrol==idrol)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['nombre']

# def getDescripcionRol(idrol):
#     s = select([rol_table],rol_table.c.idrol==idrol)
#     result = conn.execute(s)
#     row = result.fetchone()
#     return row['descripcion']

def rol(idRol):
    """Funcion que recibe el Id de un Rol y retorna el objeto rol"""
    result = session.query(Rol).filter(Rol.idrol==idRol).first()
    return result

def permiso(idPermiso):
    """Funcion que recibe el Id de un Permiso y retorna el objeto Permiso"""   
    result = session.query(Permiso).filter(Permiso.idpermiso==idPermiso).first()
    return result
        
def crearRol(nombre,descripcion,idPermisoList):
    """Funcion que recibe los atributos de un usuario y lo persiste en la base de datos."""
    idrolmax=getMayorIdRol()
    nuevo_rol = Rol(idrolmax+1,nombre,descripcion)
    listapermisos = session.query(Permiso).filter(Permiso.idpermiso.in_(idPermisoList)).all()
    nuevo_rol.permisos = listapermisos
    session.add(nuevo_rol)
    session.commit()
    
def idPermisoList(idRol):
    """Funcion que recibe el Id de un Rol y retorna la lista de rolpermisos del rol"""
    rol = session.query(Rol).filter(Rol.idrol==idRol).first()
    idPermisoList=[]
    for rolpermiso in rol.permisos:
            idPermisoList.append(rolpermiso.idpermiso)
    return idPermisoList

def modRol(idrol,nombre,descripcion,idPermisoList):
    """Funcion que recibe los atributos de un usuario y lo modifica en la base de datos"""
    rol = session.query(Rol).filter(Rol.idrol==idrol).first()
    rol.nombre = nombre
    rol.descripcion = descripcion
    listapermisos = session.query(Permiso).filter(Permiso.idpermiso.in_(idPermisoList)).all()
    rol.permisos = listapermisos
    session.commit()
        
def elimRol(idrol):
    res = session.query(Rol).filter(Rol.idrol==idrol).first()
    session.delete(res)
    session.commit()
    
def busquedaRol(parametro,atributo):
    if atributo == 'nombre':
        result = session.query(Rol).filter(Rol.nombre.like(parametro+'%')).all()
    return result

    
# def truncarPermiso():
#     trans = conn.begin()
#     try:
#         conn.execute('truncate table "public"."permiso" cascade')
#         trans.commit()
#     except :
#         trans.rollback()
#         
# def truncarRol():
#     trans = conn.begin()
#     try:
#         conn.execute('truncate table "public"."rol" cascade')
#         trans.commit()
#     except :
#         trans.rollback()
#         
# def truncarRolPermiso():
#     trans = conn.begin()
#     try:
#         conn.execute('truncate table "public"."rolpermiso" cascade')
#         trans.commit()
#     except :
#         trans.rollback()
# 
# def insertarRol(idrol,nombre,descripcion,idPermisoList):
#     """Funcion utilizada solo en tests"""
#     result = rol_table.insert().execute(idrol=idrol,
#                                              nombre=nombre,
#                                              descripcion=descripcion)   
#     for idpermiso in idPermisoList:
#         result = rolpermiso_table.insert().execute(idrol=idrol,
#                                              idpermiso = int(idpermiso))
