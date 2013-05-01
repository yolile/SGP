from Modelo import Item, VersionItem, Relacion, AtributoItemPorTipo, Fase, engine
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
 
def crearItem (nombre, estado,idtipoitem,idfase):
    """Funcion que crea un item y devuelve el iditem"""
    session1=Session()
    iditem=getMaxIdItem()+1
    nuevo=Item(iditem,nombre,estado,idtipoitem,idfase)
    session1.add(nuevo)
    session1.commit()
    return nuevo.iditem