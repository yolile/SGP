from Modelo import LineaBase,Fase,Proyecto,engine
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.orm import sessionmaker, join
import sqlalchemy.exc

"""Controlador de Lineas bases para el modulo de Gestion de Cambios"""  
__author__ = 'Grupo 5'
__date__ = '16-05-2013'
__version__ = '4.0'
__text__ = 'Este modulo contiene funciones que permiten el control de las Lineas Bases en el modulo de Gestion de Cambios'
__file__ = 'CtrlLineaBase.py'     

Session = sessionmaker(bind=engine)
session = Session()

def getLBList():
    """Funcion que retorna la lista de las lineas bases de la base de datos."""
    result = session.query(LineaBase).all()
    return result

def getMaxIdLineaBase():
    """Funcion que retorna el maximo valor de lineas bases en la base de datos"""
    lista = getLBList()
    idlineabasemax =0
    for lineabase in lista:
        if idlineabasemax < lineabase.idlineabase:
            idlineabasemax = lineabase.idlineabase
    return idlineabasemax

def getLBFase(idfase):
    """Funcion que recibe una fase y retorna la lista de lineas bases que esta posee"""
    result = session.query(LineaBase).filter(LineaBase.idfase==idfase).all()
    return result

def crearLB(idfase):
    """Funcion que crea una linea base sin items abierta"""
    maxsecuencia = getMaxSeqLB(idfase)
    estado='abierto'
    maxidlineabase = getMaxIdLineaBase()
    nueva_lineabase = LineaBase(maxidlineabase+1,idfase,estado,maxsecuencia+1)
    session.add(nueva_lineabase)
    session.commit()

def getMaxSeqLB(idfase):
    """Funcion que recibe el ID de una fase y retorna en numero maximo de secuencia de id"""
    listLB = getLBFase(idfase)
    max = 0
    for row in listLB:
        if max < row.numero:
            max = row.numero
    return max
            