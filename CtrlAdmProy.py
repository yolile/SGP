from Modelo import Fase, Proyecto, Usuario, engine, TipoItemFase, TipoItem, Rol
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, join
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
    """Funcion que recibe como parametro los atributos ingresados por el usuario y id del usuario que crea el proyecto"""
    """Guarda en la Base de Datos y coloca el proyecto como no iniciado"""
    idproyectomax = getMayorIdProyecto()
    usuariolider = CtrlAdmUsr.getIdByUsername(liderusername)
    fechaactual = date.today()
    proy_nuevo = Proyecto(idproyectomax+1,nombre,descripcion,fechaactual,0,'no-iniciado',usuariolider,presupuesto)
    lider = session.query(Usuario).filter(Usuario.idusuario==usuariolider).first()
    proy_nuevo.comitecambios.append(lider)
    session.add(proy_nuevo)
    session.commit()
    return proy_nuevo.idproyecto
    
def proy(idproyecto):
    """Funcion que recibe el Id de un Proyecto y retorna el objeto proyecto"""
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    return proy

def getFasesList():
    """Funcion que retorna la lista de todas las fases dentro del sistema"""
    result = session.query(Fase).all()
    return result

def getFasesListByProy(idproyecto):
    faseList = session.query(Fase).filter(and_(Fase.idproyecto==idproyecto,Fase.estado!='eliminada')).all()
    return faseList

def getFasesListByProyAndUser(idproyecto,username):
    """Funcion que recibe el Id de un Proyecto y el username de un Usuario y 
    retorna su lista de fases segun el rol del Usuario"""
    idroles = []
    user = session.query(Usuario).filter(Usuario.username==username).first()
    for r in user.roles:
        idroles.append(r.idrol)    
    faseRol = session.query(Fase).join(Rol,Fase.roles).filter(Rol.idrol.in_(idroles)).all()
    faseList = []
    for f in faseRol:
        if f.idproyecto == idproyecto and f.estado!='eliminada':
            faseList.append(f)
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
    """Funcion que recibe el id de una fase y retorna el objeto Fase"""
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
    """Funcion que recibe los datos introducidos por el usuario genera un id 
    y secuencia y luego pone el estado de la fase en no iniciado y guarda el objeto"""
    maxsecuencia = getMaxSeqProy(idproyecto)
    estado='no-iniciada'
    maxidfase = getMaxIdFase()
    nueva_fase = Fase(maxidfase+1,idproyecto,maxsecuencia+1,nombre,descripcion,estado)
    session.add(nueva_fase)
    session.commit()
    return nueva_fase.idfase
    
def setProyIniciado(idproyecto):
    """Funcion que establece el estado de un proyecto como
    'iniciado' y el de todas sus fases como 'desarrollo'"""
    proyecto = proy(idproyecto)
    proyecto.estado = 'iniciado'
    setFasesIniciadas(getFasesListByProy(idproyecto))
    session.commit()
    
def setFasesIniciadas(listafases):
    for fase in listafases:
        fase.estado= 'desarrollo'
    session.commit()
                    
def getProyEstado(idproyecto):
    """Funcion que recibe un id proyecto y retorna el estado en que se encuentra el mismo"""
    proyecto = proy(idproyecto)
    return proyecto.estado

def asigComiteCamb(idproyecto, idusuarioList):
    """Funcion que recibe el id proyecto y la lista de usuarios asignados para ser miembro de 
    comite de cambio para luego guardar y generar el nuevo comite de cambios"""
    proyecto = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    listausuario = session.query(Usuario).filter(Usuario.idusuario.in_(idusuarioList)).all()
    lider = proyecto.usuario
    listausuario.append(lider)
    proyecto.comitecambios=listausuario
    session.commit()
    
def busquedaProy(parametro,atributo):
    """Funcion que recibe el parametro a buscar y cual es el atributo a ser buscado"""
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
    """Funcion que establece el estado de un proyecto como 'eliminado''
    para que este ya no sea mostrado en el sistema y solo exista a nivel de BD"""
    proyecto = proy(idproyecto)
    proyecto.estado = 'eliminado'
    session.commit() 

def modProy(idproyecto,nombre,descripcion,presupuesto):
    """Funcion que recibe los atributos de un proyecto y lo modifica en la base de datos"""
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    proy.nombre = nombre
    proy.descripcion = descripcion
    proy.presupuesto = presupuesto
    session.commit()

def getidMiembrosList(idproyecto):
    """Funcion que recibe el idproyecto y retorna la lista de identificadores de los
    diferentes miembros del comite"""
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    listidmiembros=[]
    for usr in proy.comitecambios:
        listidmiembros.append(usr.idusuario)
    return listidmiembros

def getMiembrosList(idproyecto):
    """Funcion que recibe el idproyecto y retorna la lista de los
    diferentes miembros del comite"""
    proy = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    return proy.comitecambios

def getliderProyecto(idproyecto):
    """Funcion que recibe el idproyecto y retorna el usuario lider de dicho proyecto"""
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
    """Funcion que verifica si la fase posee un tipo de item asignado"""
    fase=getFase(idfase)
    if(len(fase.tipositems)>0):
        return True
    return False

def getIdPrimeraFase(idproyecto):
    """Funcion que retorna la primera fase de un proyecto"""
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

def elimFase(idfase):
    """Funcion que recibe un idfase y elimina logicamente la fase correspondiente.
    Luego arregla las secuencias de las fases siguientes"""
    fase=getFase(idfase)
    fase.estado='eliminada'
    arreglarSecuencia(fase)
    session.commit()
    
def arreglarSecuencia(fase):  
    """Funcion que recibe una fase, extrae su posicion y actualiza las posiciones
    de todas las fases siguientes, considerando que la fase recibida ha sido eliminada"""
    listafases=getFasesListByProy(fase.idproyecto)
    poseliminada=fase.posicionfase
    fase.posicionfase=0
    for row in listafases:
        if(row.posicionfase>poseliminada):
            row.posicionfase=row.posicionfase-1
            
def modFase(idfase,nombre,descripcion):
    """Funcion que recibe un idfase y valores para sus atributos y modifica la fase
    con esos valores"""
    fase=getFase(idfase)
    fase.nombre=nombre
    fase.descripcion=descripcion
    session.commit()

def faseTieneRol(idfase):
    """Funcion que recibe una fase y retorna True si tiene al menos un rol asociado"""
    fase=getFase(idfase)
    if(len(fase.roles)>0):
        return True
    return False    

def fasesTotalmenteDefinidas(listaFases):
    """Funcion que recibe una lista de fases y retorna True
    en el caso de que todas tengan tipos de item y roles asociados,
    False en caso contrario"""
    for fase in listaFases:
        if fase.estado != 'eliminada':
            if not(faseTieneTipoItem(fase.idfase)):
                return False
            if not(faseTieneRol(fase.idfase)):
                return False
    return True