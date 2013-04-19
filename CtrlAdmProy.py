from CtrlAdmUsr import getIdByUsername
import RolUsuario
import RolPermiso
import Proyecto
import Fase
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.sql import select
from datetime import *

"""Controlador de Administrador de Proyectos."""  
__author__ = 'Grupo 5'
__date__ = '17-04-2013'
__version__ = '1.0'
__text__ = 'Este modulo contiene funciones que permiten el control de administracion de proyectos'
__file__ = 'CtrlAdmProy.py'      
    
engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgp')
metadata = MetaData(bind=engine)
proyecto_table = Proyecto.get_table(metadata)
mapper(Proyecto.Proyecto, proyecto_table)
conn = engine.connect()

fase_table = Fase.get_table(metadata)
mapper(Fase.Fase, fase_table)
connfase = engine.connect()

def getProyectoList(): 
    """Funcion que retorna la lista de todos los proyectos en la base de datos."""
    s = select([proyecto_table])
    result = s.execute()
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
    result = proyecto_table.insert().execute(idproyecto=idproyectomax+1,
                                             nombre=nombre, 
                                             descripcion=descripcion,
                                             fechacreacion=fechaactual, 
                                             complejidad=0, 
                                             estado='no-iniciado', 
                                             usuariolider=usuariolider,
                                             presupuesto=presupuesto
                                             )

def proy(idproyecto):
    """Funcion que recibe el Id de un Proyecto y retorna el objeto proyecto"""
    lista = getProyectoList()
    for project in lista:
        if idproyecto == project.idproyecto:
            return project

def getFasesList():
    """Funcion que retorna la lista de todas las fases dentro del sistema"""
    s = select([fase_table])
    result=connfase.execute(s)
    return result

def getFasesListByProy(idproyecto):
    """Funcion que recibe el Id de un Proyecto y retorna su lista de fases"""
    s = select([fase_table],fase_table.c.idproyecto==idproyecto).order_by(fase_table.c.posicionfase)
    result = connfase.execute(s)
    return result

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
    lista = getFasesList()
    for fase in lista:
        if idfase == fase.idfase:
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
    result = fase_table.insert().execute(idfase=maxidfase+1,
                                             idproyecto=idproyecto, 
                                             posicionfase=maxsecuencia+1,
                                             nombre=nombre, 
                                             descripcion=descripcion
                                             )
