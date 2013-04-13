from sqlalchemy import Column, Table
from sqlalchemy import Integer, String
from sqlalchemy.sql import select

def get_table(metadata):
    permiso_table = Table(
                          'permiso', metadata,
                          Column('idpermiso', Integer, primary_key=True),
                          Column('nombre', String(160)),
                          Column('descripcion', String(400)),
                          )
    return permiso_table

class Rol(object):
    def __init__(self, idpermiso,nombre, descripcion):
        self.idpermiso = idpermiso
        self.nombre = nombre
        self.descripcion = descripcion


    def __repr__(self):
        return "<Rol '%s' '%s' '%s'>" % self.idpermiso, self.nombre, self.descripcion