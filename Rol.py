from sqlalchemy import Column, Table
from sqlalchemy import Integer, String
from sqlalchemy.sql import select

def get_table(metadata):
    rol_table = Table(
                          'rol', metadata,
                          Column('idrol', Integer, primary_key=True),
                          Column('nombre', String(160)),
                          Column('descripcion', String(300))
                          )
    return rol_table

class Rol(object):
    def __init__(self, idrol,nombre, descripcion):
        self.idrol = idrol
        self.nombre = nombre
        self.descripcion = descripcion


    def __repr__(self):
        return "<Rol '%s' '%s' '%s'>" % self.idrol, self.nombre, self.descripcion
