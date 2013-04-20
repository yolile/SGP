from sqlalchemy import Column, Table
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.sql import select

def get_table(metadata):
    fase_table = Table(
                          'fase', metadata,
                          Column('idfase', Integer, primary_key=True),
                          Column('idproyecto', Integer, ForeignKey(
                                                                   'Proyecto.idproyecto',
                                                                   onupdate="CASCADE",
                                                                   ondelete="CASCADE")
                                                                   ),
                          Column('posicionfase', Integer),
                          Column('nombre', String(45)),
                          Column('descripcion', String(45)),
                          )
    return fase_table

class Fase(object):
    def __init__(self, idfase, idproyecto, posicionfase, nombre, descripcion):
        self.idfase = idfase
        self.idproyecto = idproyecto
        self.posicionfase = posicionfase
        self.nombre = nombre
        self.descripcion = descripcion


    def __repr__(self):
        return "<Fase '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idfase, self.idproyecto, self.posicionfase, self.nombre, self.descripcion 
