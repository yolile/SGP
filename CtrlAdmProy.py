from Modelo import Fase, Proyecto, Usuario, engine, TipoItemFase, TipoItem, Rol
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from datetime import *
import sqlalchemy.exc
import CtrlAdmTipoItem
import CtrlAdmUsr

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
    usuariolider = CtrlAdmUsr.getIdByUsername(liderusername)
    fechaactual = date.today()
    proy_nuevo = Proyecto(idproyectomax+1,nombre,descripcion,fechaactual,0,'no-iniciado',usuariolider,presupuesto)
    lider = session.query(Usuario).filter(Usuario.idusuario==usuariolider).first()
    proy_nuevo.comitecambios.append(lider)
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
    estado='no-iniciada'
    maxidfase = getMaxIdFase()
    nueva_fase = Fase(maxidfase+1,idproyecto,maxsecuencia+1,nombre,descripcion,estado)
    session.add(nueva_fase)
    session.commit()
    
def setProyIniciado(idproyecto):
    """Funcion que establece el estado de un proyecto como
    'iniciado' y el estado de su primera fase como 'desarrollo'"""
    proyecto = proy(idproyecto)
    proyecto.estado = 'iniciado'
    fase=getFase(getIdPrimeraFase(idproyecto))
    fase.estado= 'desarrollo'
    session.commit() 
                    
def getProyEstado(idproyecto):
    proyecto = proy(idproyecto)
    return proyecto.estado

def asigComiteCamb(idproyecto, idusuarioList):
    proyecto = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    listausuario = session.query(Usuario).filter(Usuario.idusuario.in_(idusuarioList)).all()
    lider = proyecto.usuario
    listausuario.append(lider)
    proyecto.comitecambios=listausuario
    session.commit()
    
def busquedaProy(parametro,atributo):
    if atributo == 'nombre':
        result = session.query(Proyecto).filter(Proyecto.nombre.like('%'+parametro+'%')).all()
    if atributo == 'fechaCreacion':
        try:
            result = session.query(Proyecto).filter(Proyecto.fechacreacion.like(parametro+'%')).all()
        except sqlalchemy.exc.ProgrammingError:
            result=[]
    if atributo == 'lider':
        result = session.query(Proyecto).join((Usuario,Proyecto.usuario)).filter(Usuario.username.like('%'+parametro+'%')).all()
    return result

def elimProy(idproyecto):
    """Funcion que recibe el Id de un Proyecto y elimina de la base de datos"""
    res = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    session.delete(res)
    session.commit()

def modProy(idproyecto,nombre,descripcion,presupuesto):
    """Funcion que recibe los atributos de un proyecto y lo modifica en la base de datos"""
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    proy.nombre = nombre
    proy.descripcion = descripcion
    proy.presupuesto = presupuesto
    session.commit()

def getidMiembrosList(idproyecto):
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    listidmiembros=[]
    for usr in proy.comitecambios:
        listidmiembros.append(usr.idusuario)
    return listidmiembros

def getMiembrosList(idproyecto):
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    return proy.comitecambios

def getliderProyecto(idproyecto):
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    return proy.usuariolider

def desasignarTiposFase(fase):
    """Funcion que recibe una fase y desasigna todos
    los tipos de item que estaban asignados a la fase"""
    tiposasignados=fase.tipositems
    for tipo in tiposasignados:
        fase.tipositems.remove(tipo)

def asignarTiposAFase(idfase,idtiposdeitem):
    """Funcion que recibe un idfase y una lista de 
    id de tipos de item. Primero desasigna los tipos
    de item que estaban asignados a esa fase
    y luego asigna los tipos que pertenecen a la
    lista recibida"""
    fase = getFase(idfase)
    desasignarTiposFase(fase) 
    tiposdeitem = session.query(TipoItem).filter(TipoItem.idtipoitem.in_(idtiposdeitem)).all()
    fase.tipositems = tiposdeitem
    session.commit()

def faseTieneTipoItem(idfase):
    fase=getFase(idfase)
    if(len(fase.tipositems)>0):
        return True
    return False

def getIdPrimeraFase(idproyecto):
    fase=session.query(Fase).filter(and_(Fase.idproyecto==idproyecto, Fase.posicionfase==1)).first()
    return fase.idfase

def asignarRolesFase(idroles,idfase):
    """Funcion que recibe un idfase y una lista de id de roles.
    Primero desasigna los roles que estaban asignados a esa fase
    y luego asigna los roles que pertenecen a la lista recibida"""
    fase = getFase(idfase)
    desasignarRolesFase(fase) 
    roles = session.query(Rol).filter(Rol.idrol.in_(idroles)).all()
    fase.roles = roles
    session.commit()
    
def desasignarRolesFase(fase):
    """Funcion que recibe una fase y desasigna todos
    los roles que estaban asignados a la fase"""
    rolesasignados=fase.roles
    for rol in rolesasignados:
        fase.roles.remove(rol)
