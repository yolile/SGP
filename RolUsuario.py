from sqlalchemy import Column, Table
from sqlalchemy import Integer, String
from sqlalchemy.sql import select

def get_table(metadata):
    rolusuario_table = Table(
                          'RolUsuario', metadata,
                          Column('idRol', Integer, primary_key=True),
                          Column('idUsuario', Integer, primary_key=True),
                          )
    return rolusuario_table

class RolUsuario(object):
    def __init__(self, idrol,idusuario):
        self.idrol = idrol
        self.idusuario = idusuario


    def __repr__(self):
        return "<RolUsuario '%s' '%s'>" % self.idrol, self.idUsuario