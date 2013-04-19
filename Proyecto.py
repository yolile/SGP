from sqlalchemy import Column, Table
from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.sql import select

def get_table(metadata):
    proyecto_table = Table(
                          'proyecto', metadata,
                          Column('idproyecto', Integer, primary_key=True),
                          Column('nombre', String(45)),
                          Column('descripcion', String(200)),
                          Column('fechacreacion',Date),
                          Column('complejidad',String(45)),
                          Column('estado',String(45)),
                          Column('usuariolider',Integer,ForeignKey('Usuario.idusuario')),
                          Column('presupuesto',Integer)
                          )
    return proyecto_table

class Proyecto(object):
    def __init__(self,idproyecto,nombre,descripcion,fechacreacion,complejidad,estado,usuariolider):
        self.idproyecto = idproyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechacreacion = fechacreacion
        self.complejidad = complejidad
        self.estado = estado
        self.usuariolider = usuariolider
        self.presupuesto = presupuesto

#     def __repr__(self):
#         return "<Proyecto '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idproyecto, self.nombre, self.descripcion, self.fechacreacion, self.complejidad, self.estado, self.usuariolider self.presupuesto