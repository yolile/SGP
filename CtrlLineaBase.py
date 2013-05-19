from Modelo import LineaBase, Fase, Proyecto, Item, Relacion, engine
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

def getLB(idlineabase):
    """Funcion que recibe el id de una fase y retorna el objeto Fase"""
    lineabase = session.query(LineaBase).filter(LineaBase.idlineabase==idlineabase).first()
    return fase

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
    return nueva_lineabase.idlineabase

def getMaxSeqLB(idfase):
    """Funcion que recibe el ID de una y devuelve el numero maximo
    de secuencia de sus lineas bases"""
    lista= getLBFase(idfase)
    result=0
    for row in lista:
        if result < row.numero:
            result = row.numero
    return result

def getListItemsEnLB(idlineabase):
    """Funcion que recibe una id de linea base y retorna la lista de los id 
    de los items que se encuentran en la misma"""
    result = session.query(Item).filter(Item.idlineabase==idlineabase).all()
    return result

def getLB(idlineabase):
    """Retorna el objeto LineaBase con el mismo idlieabase recibido como parametro"""
    result = session.query(LineaBase).filter(LineaBase.idlineabase==idlineabase).first()
    return result
    
def getItemsFaseNotLB(idfase):
    """Retorna los items de la fase con el id pasado como parametro y los items que no esten en 
    ninguna linea base"""
    result = session.query(Item).filter(and_(Item.idfase==idfase,Item.idlineabase==None)).all()
    return result

def agregarItems(listItemEnLB,idlineabase):
    """Funcion que recibe la lista de los id de los items elegidos a ser agregados a una linea Base seleccionada"""
    """La funcion es agrega en Item el id de la linea base """
    listDesagregados = session.query(Item).filter(Item.idlineabase==idlineabase).all()
    for item in listDesagregados:
        item.idlineabase=None
    session.commit()
    listItem = session.query(Item).filter(Item.iditem.in_(listItemEnLB)).all()
    for item in listItem:
        item.idlineabase = idlineabase
    session.commit()

def eliminarLB(idlineabase):
    """Elimina logicamente una linea base dado el id de una linea base y quita 
    los items de tal linea base"""
    listItems = session.query(Item).filter(Item.idlineabase==idlineabase).all()
    for item in listItems:
        item.idlineabase=None
    LB = getLB(idlineabase)
    LB.numero=0
    LB.estado='eliminado'
    session.commit()
    
def cerrarLB(idlineabase):
    """Funcion de cerrar linea base, primero determina a que fase pertenece la linea base a cerrar.
    Si es que pertenece a la primera solo la cierra en caso contrario ve si todos sus items tienen
    algun otro item apuntandolo en alguna relacion"""
    lineabase = session.query(LineaBase).filter(LineaBase.idlineabase==idlineabase).first()
    fase = session.query(Fase).filter(Fase.idfase==lineabase.idfase).first()
    if fase.posicionfase > 1:
        listItem = getListItemsEnLB(idlineabase)
        for i in listItem:
            result = session.query(Relacion).filter(Relacion.alitem==i.iditem).first()
            if result==None:
                return False
    listItem = getListItemsEnLB(idlineabase)
    for i in listItem:
        i.estado='bloqueado'
    lineabase.estado='cerrado'
    session.commit()
    return True

def busquedaLineaBase(parametro,atributo,idfase):
    """Funcion que recibe un parametro de busqueda, el atributo y el id de la fase por el cual buscar y retorna coincidencias"""
    if atributo == 'estado':
        result = session.query(LineaBase).filter(and_(LineaBase.estado.like(parametro+'%'),
                                                 LineaBase.idfase==idfase)).all()
    return result
