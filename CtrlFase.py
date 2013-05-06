from Modelo import Item, VersionItem, Relacion, AtributoItemPorTipo, Fase, Proyecto, engine
from sqlalchemy import create_engine, and_, or_, func
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
    """Funcion que retorna la version de un tipo de item"""
    result = session.query(VersionItem).all()
    return result     
 
def getMaxIdVersionItem():
    """Funcion que retorna el maximo valor de la idVersion de un item"""
    lista = getVersionItemList()
    idversionitemmax =0
    for versionitem in lista:
        if idversionitemmax < versionitem.idversionitem:
            idversionitemmax = versionitem.idversionitem
    return idversionitemmax
 
def crearItem(item,versionitem,listaAtributoItemPorTipo):
     """Funcion que crea un item, la version 1 y la 
     lista de sus atributos segun el tipo de item"""
     proyecto = session.query(Proyecto).join((Fase.proyecto,Proyecto)).filter(Fase.idfase==item.idfase).first()
     proyecto.presupuesto = proyecto.presupuesto - versionitem.costo
     session.add(item)
     session.commit()
     session.add_all(listaAtributoItemPorTipo)
     session.add(versionitem)
     session.commit()
     
def instanciarItem(nombre,estado,idtipoitem,idfase):
    """Funcion que devuelve el objeto Item de acuerdo 
    con los atributos pasados como parametros"""
    iditem=getMaxIdItem()+1
    nuevo=Item(iditem,nombre,estado,idtipoitem,idfase)
    return nuevo

def instanciarAtributoItemPorTipo(iditem,idatributo,valor):
    """Funcion que devuelve el objeto Atributo Item Por Tipo
     de acuerdo con los atributos pasados como parametros"""
    nuevo = AtributoItemPorTipo(iditem,idatributo,valor)
    return nuevo

def getItemsFase(idfase):
    """Funcion que retorna la lista de los Items dado el id de la fase"""
    result = session.query(Item).filter(Item.idfase==idfase).all()
    return result

def instanciarVersionItem(iditem,idusuario,descripcion,complejidad,prioridad,costo,version):
    """Funcion que devuelve el objeto Version Item de acuerdo 
    con los atributos pasados como parametros"""
    idversionitem=getMaxIdVersionItem()+1
    nuevo = VersionItem(idversionitem, iditem, idusuario,descripcion,complejidad,prioridad,costo,version)
    return nuevo

def getItem(iditem):
    """Funcion que recibe un iditem y retorna el objeto iditem"""
    item = session.query(Item).filter(Item.iditem==iditem).first()
    return item

def getItemsFaseAnterior(idfase):
    """Funcion que recibe una idfase y retorna los items de la  fase anterior"""
    fase_actual = session.query(Fase).filter(Fase.idfase==idfase).first()
    fase_anterior = session.query(Fase).filter(and_(Fase.posicionfase==fase_actual.posicionfase-1,
                                                Fase.idproyecto==fase_actual.idproyecto)).first()
    return getItemsFase(fase_anterior.idfase)

def relacionar(idItem, idItemList, tipo):
    """Funcion que guarda la relacion en la Base de datos"""
    relacioneliminarList = session.query(Relacion).filter(Relacion.alitem==idItem).all()
    for relacion in relacioneliminarList:
        session.delete(relacion)
    session.commit()
    relaciones = []    
    for id in idItemList:
        #Relacion(delitem,alitem)
        nuevo = Relacion(int(id),int(idItem),tipo)
        relaciones.append(nuevo)
    session.add_all(relaciones)
    session.commit()

def getRelaciones(idItem):
    """Funcion que retorna las relaciones de un Item segun su id"""
    result = session.query(Relacion).filter(Relacion.delitem==idItem).all()
    return result

def ciclo(idItemA,idItemB):
    """Funcion para determinar si al itroducir el vertice A---->B no se formara ningun ciclo"""
    #print '('+str(idItemA)+" "+str(idItemB)+')'
    if(idItemA == idItemB):
        #print True
        return True
    relacionList = getRelaciones(idItemB)
    for relacion in relacionList:
        if ciclo(idItemA,relacion.alitem):
            return True
    #print False
    return False

def getListPadreHijo(idItem):
    """Funcion que retorna la el idlist de los items que estan en relacion padre-hijo"""
    relacionList = session.query(Relacion).filter(and_(Relacion.alitem==idItem,Relacion.tipo=='padre-hijo')).all()
    idItemList = []
    for relacion in relacionList:
        idItemList.append(relacion.delitem)
    return idItemList


def getListAntecesorSucesor(idItem):
    """Funcion que retorna la el idlist de los items que estan en relacion sucesor-antecesor"""    
    item = session.query(Item).filter(Item.iditem==idItem).first()
    relacionList = session.query(Relacion).filter(and_(Relacion.alitem==idItem,Relacion.tipo=='sucesor-antecesor')).all()
    idItemList = []
    for relacion in relacionList:
        idItemList.append(relacion.delitem)
    return idItemList

def busquedaItem(parametro,atributo,idfase):
    """Funcion que recibe un parametro de busqueda, el atributo y el id de la fase por el cual buscar y retorna coincidencias"""
    if atributo == 'nombre':
        result = session.query(Item).filter(and_(Item.nombre.like(parametro+'%'),
                                                 Item.idfase==idfase)).all()
    return result
    
def getVersionActual(iditem):
    """Funcion para obtener la ultima version de VersionItem"""
    version = session.query(VersionItem).filter(and_(VersionItem.iditem==iditem,
                                                     VersionItem.version==session.query(func.max(VersionItem.version)))).first()
    return version
