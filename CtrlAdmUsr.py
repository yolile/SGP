from Usuario import Usuario, get_table 
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.sql import select

"""Modulo para ejemplificar el uso de pydoc."""  
__author__ = 'Grupo 5'
__date__ = 'hoy'
__version__ = '1.0'
__credits__ = 'none'
__text__ = 'some text'
__file__ = 'ejemplo.py'      

engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgp')
metadata = MetaData(bind=engine)
usuario_table = get_table(metadata)
mapper(Usuario, usuario_table)

def getUsuarioList():
    s = select([usuario_table])
    result = s.execute()
    return result

def validarUsuario(username, password):
        usuarioList = getUsuarioList()
        for user in usuarioList:
            if username == user.username:
                if password == user.passwrd:
                    return True
        return False


def crearUsr(username,passwrd,nombre,apellido,telefono,ci):
    lista = getUsuarioList()
    idusuariomax = 0
    for user in lista:
        if idusuariomax < user.idusuario:
            idusuariomax = user.idusuario
    result = usuario_table.insert().execute(idusuario=idusuariomax+1,
                                             username=username, 
                                             passwrd=passwrd,
                                             nombre=nombre, 
                                             apellido=apellido, 
                                             telefono=telefono, 
                                             ci=ci)
    return result

def elimUsr(iduser):
    conn = engine.connect()
    conn.execute(usuario_table.delete().where(usuario_table.c.idusuario==iduser)) 
    
    
def modUsr(iduser,username,passwrd,nombre,apellido,telefono,ci):
    conn = engine.connect()
    conn.execute(usuario_table.update().
                    where(usuario_table.c.idusuario==iduser).
                    values(username=username,
                           passwrd=passwrd,
                           nombre=nombre,
                           apellido=apellido,
                           telefono=telefono,
                           ci=ci)
                )

def usr(iduser):
    lista = getUsuarioList()
    for user in lista:
        if iduser == user.idusuario:
            return user
