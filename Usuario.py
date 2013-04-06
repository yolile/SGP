from sqlalchemy import Column, Table
from sqlalchemy import Integer, String
from sqlalchemy.sql import select

def get_table(metadata):
    usuario_table = Table(
                          'usuario', metadata,
                          Column('idusuario', Integer, primary_key=True),
                          Column('username', String(45), unique=True),
                          Column('passwrd', String(160)),
                          Column('nombre', String(45)),
                          Column('apellido', String(45)),
                          Column('telefono', String(45)),
                          Column('ci', Integer),
                          )
    return usuario_table

class Usuario(object):
    def __init__(self, idusuario, username, passwrd, nombre, apellido, telefono, ci):
        self.idusuario = idusuario
        self.username = username
        self.passwrd = passwrd
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.ci = ci


    def __repr__(self):
        return "<Usuario '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idusuario, self.username, self.passwrd, self.nombre, self.apellido, self.telefono, self.ci 

