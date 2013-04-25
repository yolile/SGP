from CtrlAdmUsr import getIdByUsername
from Modelo import Fase, Proyecto, Usuario, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import *

"""Controlador de Administrador de Proyectos."""  
__author__ = 'Grupo 5'
__date__ = '17-04-2013'
__version__ = '1.0'
__text__ = 'Este modulo contiene funciones que permiten el control de administracion de proyectos'
__file__ = 'CtrlAdmProy.py'      
    
#engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgptest')
Session = sessionmaker(bind=engine)
session = Session()     

def getProyectoList(): 
    """Funcion que retorna la lista de todos los proyectos en la base de datos."""
    result = session.query(Proyecto).all()
    return result

def getMayorIdProyecto():
    """Funcion que retorna el mayor idproyecto en la tabla proyecto"""
    lista = getProyectoList()
    idproyectomax = 0
    for proy in lista:
        if idproyectomax < proy.idproyecto:
            idproyectomax = proy.idproyecto
    return idproyectomax 

def crearProy (nombre,descripcion,presupuesto,liderusername):
    idproyectomax = getMayorIdProyecto()
    usuariolider = getIdByUsername(liderusername)
    fechaactual = date.today()
    proy_nuevo = Proyecto(idproyectomax+1,nombre,descripcion,fechaactual,0,'no-iniciado',usuariolider,presupuesto)
    session.add(proy_nuevo)
    session.commit()
    
def proy(idproyecto):
    """Funcion que recibe el Id de un Proyecto y retorna el objeto proyecto"""
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    return proy

def getFasesList():
    """Funcion que retorna la lista de todas las fases dentro del sistema"""
    result = session.query(Fase).all()
    return result

def getFasesListByProy(idproyecto):
    """Funcion que recibe el Id de un Proyecto y retorna su lista de fases"""
    faseList = session.query(Fase).filter(Fase.idproyecto==idproyecto).all()
    return faseList

def getMaxSeqProy(idproyecto):
    """Funcion que recibe el ID de un proyecto y devuelve el numero maximo
    de secuencia de sus fases"""
    lista= getFasesListByProy(idproyecto)
    result=0
    for row in lista:
        if result < row.posicionfase:
            result = row.posicionfase
    return result

def getFase(idfase):
    fase = session.query(Fase).filter(Fase.idfase==idfase).first()
    return fase
    
def getMaxIdFase():
    """Funcion que retorna el mayor idfase en la tabla fase"""
    lista = getFasesList()
    idfasemax = 0
    for fase in lista:
        if idfasemax < fase.idfase:
            idfasemax = fase.idfase
    return idfasemax 

def crearFase(nombre,descripcion,idproyecto):
    maxsecuencia = getMaxSeqProy(idproyecto)
    maxidfase = getMaxIdFase()
    nueva_fase = Fase(maxidfase+1,idproyecto,maxsecuencia+1,nombre,descripcion)
    session.add(nueva_fase)
    session.commit()
    
def setProyIniciado(idproyecto):
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    proy.estado = 'iniciado'
    session.commit() 
                    
def getProyEstado(idproyecto):
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    return proy.estado

def asigComiteCamb(idproyecto, idusuarioList):
    proyecto = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    listausuario = session.query(Usuario).filter(Usuario.idusuario.in_(idusuarioList)).all()
    proyecto.comitecambios=listausuario
    session.commit()
    
# def truncarProyecto():
#     trans = conn.begin()
#     try:
#         conn.execute('truncate table "public"."proyecto" cascade')
#         trans.commit()
#     except :
#         trans.rollback()
#         
# def truncarFase():
#     trans = connfase.begin()
#     try:
#         connfase.execute('truncate table "public"."fase" cascade')
#         trans.commit()
#     except :
#         trans.rollback()