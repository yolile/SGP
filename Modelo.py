import os
from sqlalchemy import Table, Integer, ForeignKey, String, Column, Date, LargeBinary
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import _SessionClassMethods
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

"""Modulo contenedor de las clases de las entidades"""  
__author__ = 'Grupo 5'
__date__ = '04/05/13'
__version__ = '3.0'
__credits__ = 'none'
__text__ = 'Modulo con las clases y las tablas relacionadas entre si'
__file__ = 'Modelo.py' 


rutaBD='postgresql+psycopg2://admin:admin@localhost/sgptest'

#engine = create_engine(os.environ['DATABASE_URI'])
engine=create_engine(rutaBD)
Base= declarative_base()
path="/home/divina/git/SGP/"

"""------------------------TABLAS DE RELACION---------------------------------------"""
RolPermiso = Table('rolpermiso', Base.metadata,
    Column('idrol', Integer, ForeignKey('rol.idrol'),primary_key=True),
    Column('idpermiso', Integer, ForeignKey('permiso.idpermiso'),primary_key=True)
)

RolUsuario = Table('rolusuario', Base.metadata,
    Column('idrol', Integer, ForeignKey('rol.idrol'),primary_key=True),
    Column('idusuario', Integer, ForeignKey('usuario.idusuario'),primary_key=True)
)

RolFase = Table('rolfase', Base.metadata,
    Column('idrol', Integer, ForeignKey('rol.idrol'),primary_key=True),
    Column('idfase', Integer, ForeignKey('fase.idfase'),primary_key=True)
)

ComiteCambios = Table('comitecambios', Base.metadata,
    Column('idusuario', Integer, ForeignKey('usuario.idusuario'),primary_key=True),
    Column('idproyecto', Integer, ForeignKey('proyecto.idproyecto'),primary_key=True)
)

TipoItemFase=Table('tipoitemfase', Base.metadata,
                   Column('idtipoitem', Integer, ForeignKey('tipoitem.idtipoitem'),primary_key=True),
                   Column('idfase', Integer, ForeignKey('fase.idfase'),primary_key=True)
)
  
ArchivoItem = Table('archivoitem', Base.metadata,
    Column('iditem', Integer, ForeignKey('item.iditem'),primary_key=True),
    Column('idarchivo', Integer, ForeignKey('archivo.idarchivo'),primary_key=True)
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
    estado = Column(Integer)
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
        self.estado=1
 
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
    fases = relationship("Fase")
    comitecambios = relationship("Usuario", secondary=ComiteCambios)

     
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
    idproyecto = Column(Integer,ForeignKey('proyecto.idproyecto'))
    proyecto = relationship("Proyecto")
    posicionfase = Column(Integer)
    nombre = Column(String(45))
    descripcion = Column(String(45))
    estado=Column(String(45))
    roles = relationship("Rol", secondary=RolFase)
    tipositems = relationship("TipoItem", secondary=TipoItemFase)
    
    items = relationship("Item")
    
    def __init__(self, idfase, idproyecto, posicionfase, nombre, descripcion, estado):
        self.idfase = idfase
        self.idproyecto = idproyecto
        self.posicionfase = posicionfase
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado


    def __repr__(self):
        return "<Fase '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' >" % self.idfase, self.idproyecto, self.posicionfase, self.nombre, self.descripcion, self.estado 

"""------------------------TIPO DE ITEM---------------------------------------"""
class TipoItem(Base):
    __tablename__ = 'tipoitem'
    idtipoitem = Column(Integer,primary_key=True)
    nombre = Column(String(160))
    descripcion = Column(String(300))
    atributos = relationship("AtributoTipo")
 
    def __init__(self, idtipoitem, nombre, descripcion):
        self.idtipoitem = idtipoitem
        self.nombre = nombre
        self.descripcion = descripcion
 
 
    def __repr__(self):
        return "<TipoItem '%s' '%s' '%s'>" % self.idtipoitem, self.nombre, self.descripcion
    
"""------------------------ATRIBUTO POR TIPO DE ITEM---------------------------------------"""
class AtributoTipo(Base):
    __tablename__ = 'atributotipo'
    idatributo = Column(Integer,primary_key=True)
    idtipoitem = Column(Integer,ForeignKey('tipoitem.idtipoitem',
                                        onupdate="CASCADE",
                                        ondelete="CASCADE"))
    nombre = Column(String(160))
    tipo = Column(String(45))
    valordefecto = Column(String(45))

    def __init__(self, idatributo, idtipoitem, nombre, tipo, valordefecto):
        self.idatributo=idatributo
        self.idtipoitem = idtipoitem
        self.nombre = nombre
        self.tipo = tipo
        self.valordefecto = valordefecto

    def __repr__(self):
        return "<AtributoTipo '%s' '%s' '%s' '%s' '%s'>" % self.idatributo, self.idtipoitem, self.nombre, self.tipo, self.valordefecto
        
"""------------------------ATRIBUTO DE ITEM POR TIPO DE ITEM---------------------------------------"""
class AtributoItemPorTipo(Base):
    __tablename__ = 'atributoitemportipo'
    iditem = Column(Integer, ForeignKey('item.iditem'),primary_key=True)
    idatributo = Column(Integer,ForeignKey('atributotipo.idatributo'),primary_key=True)
    valor = Column(String(45))
       
    def __init__(self, iditem, idatributo, valor):
        self.iditem = iditem
        self.idatributo = idatributo
        self.valor = valor
 
    def __repr__(self):
        return "<AtributoItemPorTipo '%s' '%s' '%s' '%s'>" % self.iditem, self.idatributo, self.valor
       
"""------------------------ITEM---------------------------------------"""
class Item(Base):
    __tablename__ = 'item'
    iditem = Column(Integer,primary_key=True)
    nombre = Column(String(160))
    estado = Column(String(45))
    idtipoitem = Column(Integer, ForeignKey('tipoitem.idtipoitem'))
    idfase = Column(Integer, ForeignKey('fase.idfase'))        
    fase = relationship("Fase")
    atributos = relationship("AtributoItemPorTipo")
    idlineabase = Column (Integer,ForeignKey ('lineabase.idlineabase'))
    tipoitem = relationship("TipoItem")
    archivos = relationship("Archivo", secondary=ArchivoItem)
    versiones = relationship("VersionItem")
    lineabase = relationship("LineaBase", backref=backref("item", uselist=False))
    
    
    def __init__(self, iditem, nombre, estado, idtipoitem,idfase,idlineabase=None):
        self.iditem = iditem
        self.nombre = nombre 
        self.estado = estado
        self.idtipoitem = idtipoitem
        self.idfase = idfase
        self.idlineabase = idlineabase     
 
 
    def __repr__(self):
        return "<Item '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idtipoitem, self.nombre,self.estado, self.idtipoitem, self.idfase, self.idlineabase
        
"""------------------------VERSION DEL ITEM---------------------------------------"""
class VersionItem(Base):
    __tablename__ = 'versionitem'
    idversionitem = Column(Integer, primary_key=True)   
    iditem = Column(Integer,ForeignKey('item.iditem')) 
    idusuario = Column (Integer, ForeignKey('usuario.idusuario'))
    descripcion = Column(String(160))
    complejidad = Column(Integer)
    prioridad = Column(Integer)
    costo = Column(Integer)                   
    version = Column(Integer)
    estado = Column(String(45))

    def __init__(self, idversionitem, iditem, idusuario,descripcion,complejidad,prioridad,costo,version,estado):
        self.idversionitem = idversionitem
        self.iditem = iditem
        self.idusuario = idusuario
        self.descripcion = descripcion
        self.complejidad = complejidad
        self.prioridad = prioridad
        self.costo = costo        
        self.version = version
        self.estado = estado
    def __repr__(self):
        return "<VersionItem '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'>" % self.idversionitem, self.iditem, self.idusuario, self.descripcion, self.complejidad, self.prioridad, self.costo, self.version, self.estado
    
"""------------------------RELACION ENTRE ITEMS---------------------------------------"""
class Relacion(Base):
    __tablename__ = 'relacion'
    delitem = Column(Integer,ForeignKey('item.iditem'), primary_key=True)   
    alitem = Column(Integer,ForeignKey('item.iditem'), primary_key=True)
    tipo = Column(String(45))

    def __init__(self, delitem, alitem,tipo):
        self.delitem = delitem
        self.alitem = alitem
        self.tipo = tipo

    def __repr__(self):
        return "<Item '%s' '%s' '%s'>" % self.delitem, self.alitem, self.tipo
 
"""------------------------LINEA BASE---------------------------------------"""
class LineaBase(Base):
    __tablename__ = 'lineabase'
    idlineabase = Column(Integer,primary_key=True)   
    idfase = Column(Integer,ForeignKey('fase.idfase'))
    estado = Column(String(45))
    numero = Column(Integer)
    
    
    def __init__(self, idlineabase, idfase, estado, numero):
        self.idlineabase = idlineabase
        self.idfase = idfase
        self.estado = estado
        self.numero = numero


    def __repr__(self):
        return "<LineaBase'%s' '%s' '%s' '%s'>" % self.idlineabase, self.idfase, self.estado, self.numero

"""------------------------ARCHIVO---------------------------------------"""
class Archivo(Base):
    __tablename__ = 'archivo'
    idarchivo = Column(Integer,primary_key = True)
    archivo = Column(LargeBinary)
    nombre = Column(String(45))
    items = relationship("Item", secondary=ArchivoItem)
     
    def __init__(self, idarchivo, archivo, nombre):
        self.idarchivo = idarchivo
        self.archivo =  archivo
        self.nombre = nombre

 
    def __repr__(self):
        return "<Archivo '%s' '%s' '%s' '%s' >" % self.idarchivo, self.archivo, self.nombre
    
"""------------------------SOLICITUD DE CAMBIO---------------------------------------"""
class SolicitudDeCambio(Base):
    __tablename__ = 'solicituddecambio'
    idsolicituddecambio = Column(Integer,primary_key = True)
    idusuariosolicitante = Column(Integer,ForeignKey('usuario.idusuario'))
    descripcion = Column(String(200))
    estado = Column(String(45))
    tipo = Column(String(45))
    costo = Column(String(45))
    impacto = Column(String(45))
    iditem = Column(Integer, ForeignKey('item.iditem'))
    item = relationship("Item", backref=backref("solicituddecambio", uselist=False))
    
    idversionitem = Column(Integer, ForeignKey('versionitem.idversionitem'))
    versionitem = relationship("VersionItem", backref=backref("solicituddecambio", uselist=False))
     
    def __init__(self, idsolicituddecambio, idusuariosolicitante, descripcion,tipo,iditem,idversionitem,estado,costo,impacto):
        self.idsolicituddecambio = idsolicituddecambio
        self.idusuariosolicitante =  idusuariosolicitante
        self.descripcion = descripcion
        self.tipo = tipo
        self.iditem = iditem
        self.idversionitem = idversionitem
        self.estado=estado
        self.costo=costo
        self.impacto=impacto
        
    def __repr__(self):
        return "<SolicitudDeCambio '%s' '%s' '%s' '%s' '%s' '%s' '%s' >" % self.idsolicituddecambio, self.idusuariosolicitante, self.descripcion, self.estado, self.tipo, self.iditem, self.idversionitem

"""------------------------Solicitud por Usuario de Comite de Cambios---------------------------------------"""
class SolicitudPorUsuarioCC(Base):
    __tablename__ = 'solicitudporusuariocc'
    idsolicituddecambio = Column(Integer,ForeignKey('solicituddecambio.idsolicituddecambio'), primary_key=True)   
    idusuariocc = Column(Integer,ForeignKey('usuario.idusuario'), primary_key=True)
    idproyectocc = Column(Integer,ForeignKey('proyecto.idproyecto'), primary_key=True)
    voto = Column(String(45))

    solicituddecambio = relationship("SolicitudDeCambio")
    

    def __init__(self, idsolicituddecambio, idusuariocc, idproyectocc,voto):
        self.idsolicituddecambio = idsolicituddecambio
        self.idusuariocc = idusuariocc
        self.idproyectocc = idproyectocc
        self.voto = voto


    def __repr__(self):
        return "<SolicitudPorUsuarioCC '%s' '%s' '%s'>" % self.idsolicituddecambio, self.idusuariocc, self.idproyectocc

"""-----------Metodos para crear y eliminar todas las tablas definidas---------------------------------------"""
def init_db():
    Base.metadata.create_all(engine)
    
def drop_db():
    _SessionClassMethods.close_all()
    Base.metadata.drop_all(engine)
    
#drop_db()   
init_db()
