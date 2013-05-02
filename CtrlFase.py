from Modelo import Item, VersionItem, Relacion, AtributoItemPorTipo, Fase, Proyecto, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""Controlador de Fases en el modulo de desarrollo"""  
__author__ = 'Grupo 5'
__date__ = '01-05-2013'
__version__ = '1.0'
__text__ = 'Este modulo contiene funciones que permiten el control de las fases en el modulo de desarrollo'
__file__ = 'CtrlFase.py'      
    
#engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgptest')
Session = sessionmaker(bind=engine)
session = Session()
  
def getItemList(): 
    """Funcion que retorna la lista de todos los items de una fase."""
    # ver como hacer para que traiga solo lo de una fase
    result = session.query(Item).all()
    return result

def getMaxIdItem():
    """Funcion que retorna el maximo valor items en la base de datos"""
    lista = getItemList()
    iditemmax =0
    for item in lista:
        if iditemmax < item.iditem:
            iditemmax = item.iditem
    return iditemmax

def getVersionItemList():
    result = session.query(VersionItem).all()
    return result     
 
def getMaxIdVersionItem():
    lista = getVersionItemList()
    idversionitemmax =0
    for versionitem in lista:
        if idversionitemmax < versionitem.idversionitem:
            idversionitemmax = versionitem.idversionitem
    return idversionitemmax
 
def crearItem(item,versionitem,listaAtributoItemPorTipo):
     """Funcion que crea un item y devuelve el iditem"""
     proyecto = session.query(Proyecto).join((Fase.proyecto,Proyecto)).filter(Fase.idfase==item.idfase).first()
     proyecto.presupuesto = proyecto.presupuesto - versionitem.costo
     session.add(item)
     session.commit()
     session.add_all(listaAtributoItemPorTipo)
     session.add(versionitem)
     session.commit()
     
def instanciarItem(nombre,estado,idtipoitem,idfase):
    iditem=getMaxIdItem()+1
    nuevo=Item(iditem,nombre,estado,idtipoitem,idfase)
    return nuevo

def instanciarAtributoItemPorTipo(iditem,idatributo,valor):
    nuevo = AtributoItemPorTipo(iditem,idatributo,valor)
    return nuevo

def getItemsFase(idfase):
    result = session.query(Item).filter(Item.idfase==idfase).all()
    return result

def instanciarVersionItem(iditem,idusuario,descripcion,complejidad,prioridad,costo,version):
    idversionitem=getMaxIdVersionItem()+1
    nuevo = VersionItem(idversionitem, iditem, idusuario,descripcion,complejidad,prioridad,costo,version)
    return nuevo