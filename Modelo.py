from sqlalchemy import Table, Integer, ForeignKey, String, Column, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


"""Modulo contenedor de las clases de las entidades"""  
__author__ = 'Grupo 5'
__date__ = '23/04/13'
__version__ = '1.0'
__credits__ = 'none'
__text__ = 'Modulo con las clases y las tablas relacionadas entre si'
__file__ = 'Modelo.py' 

Base = declarative_base()

"""------------------------TABLAS DE RELACION---------------------------------------"""
RolPermiso = Table('rolpermiso', Base.metadata,
    Column('idrol', Integer, ForeignKey('rol.idrol'),primary_key=True),
    Column('idpermiso', Integer, ForeignKey('permiso.idpermiso'),primary_key=True)
)

# #Tabla de asociacion entre Fase y Rol
# RolFase = Table('rolfase', Base.metadata,
#     Column('idrol', Integer, ForeignKey('rol.idrol')),
#     Column('idfase', Integer, ForeignKey('fase.idfase'))
# )

RolUsuario = Table('rolusuario', Base.metadata,
    Column('idusuario', Integer, ForeignKey('usuario.idusuario'),primary_key=True),
    Column('idrol', Integer, ForeignKey('rol.idrol'),primary_key=True)
)

"""------------------------USUARIO---------------------------------------""" 
class Usuario(Base):
    __tablename__ = 'usuario'
    idusuario = Column(Integer,primary_key = True)
    username = Column(String(45),unique = True)
    passwrd = Column(String(160))
    nombre = Column(String(45))
    apellido = Column(String(45))
    telefono = Column(String(45))
    ci = Column(Integer)
    roles = relationship("Rol",secondary=RolUsuario)   
    
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

"""------------------------ROL---------------------------------------"""
class Rol(Base):
    __tablename__ = 'rol'
    idrol = Column(Integer,primary_key=True)
    nombre = Column(String(160))
    descripcion = Column(String(300))
    permisos = relationship("Permiso", secondary=RolPermiso)

    def __init__(self, idrol,nombre, descripcion):
        self.idrol = idrol
        self.nombre = nombre
        self.descripcion = descripcion


    def __repr__(self):
        return "<Rol '%s' '%s' '%s'>" % self.idrol, self.nombre, self.descripcion

"""------------------------PERMISO---------------------------------------"""
class Permiso(Base):
    __tablename__ = 'permiso'
    idpermiso = Column(Integer,primary_key = True)
    nombre = Column(String(160))
    descripcion = Column(String(400))
  
    def __init__(self, idpermiso,nombre, descripcion):
        self.idpermiso = idpermiso
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return "<Permiso '%s' '%s' '%s'>" % self.idpermiso, self.nombre, self.descripcion 

"""------------------------PROYECTO---------------------------------------"""
class Proyecto(Base):
    __tablename__ = 'proyecto'
    idproyecto = Column(Integer,primary_key = True)
    nombre = Column(String(45))
    descripcion = Column(String(200))
    fechacreacion = Column(Date)
    complejidad = Column(Integer)
    estado = Column(String(45))
    usuariolider = Column(Integer, ForeignKey('usuario.idusuario'))
    usuario = relationship("Usuario")
    presupuesto = Column(Integer)
    
    def __init__(self,idproyecto,nombre,descripcion,fechacreacion,complejidad,estado,usuariolider,presupuesto):
        self.idproyecto = idproyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechacreacion = fechacreacion
        self.complejidad = complejidad
        self.estado = estado
        self.usuariolider = usuariolider
        self.presupuesto = presupuesto

    def __repr__(self):
        return "<Proyecto '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idproyecto, self.nombre, self.descripcion, self.fechacreacion, self.complejidad, self.estado, self.usuariolider, self.presupuesto

"""------------------------FASE---------------------------------------"""
class Fase(Base):

    __tablename__ = 'fase'
    idfase = Column(Integer,primary_key = True)
    idproyecto = Column(Integer,ForeignKey('proyecto.idproyecto',
                                            onupdate="CASCADE",
                                            ondelete="CASCADE"))
    proyecto = relationship("Proyecto")
    posicionfase = Column(Integer)
    nombre = Column(String(45))
    descripcion = Column(String(45))
#    roles = relationship("Rol", backref=backref("fase"))   
    
    def __init__(self, idfase, idproyecto, posicionfase, nombre, descripcion):
        self.idfase = idfase
        self.idproyecto = idproyecto
        self.posicionfase = posicionfase
        self.nombre = nombre
        self.descripcion = descripcion


    def __repr__(self):
        return "<Fase '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idfase, self.idproyecto, self.posicionfase, self.nombre, self.descripcion 



