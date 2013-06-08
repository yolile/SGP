from Modelo import *
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.orm import sessionmaker, join
import sqlalchemy.exc
import CtrlFase
import CtrlLineaBase

"""Controlador de Solicitudes de Cambio para el modulo de Gestion de Cambios"""  
__author__ = 'Grupo 5'
__date__ = '08-06-2013'
__version__ = '6.0'
__text__ = 'Este modulo contiene funciones que permiten el control de las Solicitudes de cambio en el modulo de Gestion de Cambios'
__file__ = 'CtrlSolicitudCambio.py'     

Session = sessionmaker(bind=engine)
session = Session()

def getSolicitudesbyCC(idusuario):
    """Funcion que obtiene las solicitudes de Cambio segun el usuario este en los CC de los proyectos"""
    lista = session.query(SolicitudDeCambio).join((SolicitudPorUsuarioCC.solicituddecambio,SolicitudDeCambio)).filter(SolicitudPorUsuarioCC.idusuariocc==idusuario).all()
    return lista

def getSolicitudDeCambio(idsolicituddecambio):
    """Funcion que obtiene una solicitud de cambio"""
    solicitud = session.query(SolicitudDeCambio).filter(SolicitudDeCambio.idsolicituddecambio==idsolicituddecambio).first()
    return solicitud

def votarSolicitud(idsolicituddecambio,idintegrante,voto):
    """Funcion que recibe una solicitud de cambio, quien fue el votante y el voto para
    para guardarlo en el sistema"""
    solicitud=session.query(SolicitudPorUsuarioCC).filter(and_(SolicitudPorUsuarioCC.idsolicituddecambio==idsolicituddecambio,
                                                               SolicitudPorUsuarioCC.idusuariocc==idintegrante)).first()
    solicitud.voto = voto
    session.commit()
    
def getVotobyCC(idusuario):
    """Funcion que recibe el el id del usuario del comite de cambio
    y retorna el objeto de la solicitud"""
    solicitud=session.query(SolicitudPorUsuarioCC).filter(SolicitudPorUsuarioCC.idusuariocc==idusuario).all()
    return solicitud

def getestadoVoto(idsolicituddecambio,idintegrante):
    """Funcion que recibe el id solicitud y el integrante y retorna cual fue su voto"""
    solicitud=session.query(SolicitudPorUsuarioCC).filter(and_(SolicitudPorUsuarioCC.idsolicituddecambio==idsolicituddecambio,
                                                               SolicitudPorUsuarioCC.idusuariocc==idintegrante)).first()
    return solicitud.voto
    
def contarVotos(idsolicituddecambio):
    """Funcion que se encarga de contar los votos de una solicitud"""
    votos=session.query(SolicitudPorUsuarioCC).filter(SolicitudPorUsuarioCC.idsolicituddecambio==idsolicituddecambio).all()
    total = len(votos)
    aceptados=0
    rechazados=0
    for v in votos:
        if v.voto == 'Aceptado':
            aceptados = aceptados + 1
        if v.voto == 'Rechazado':
            rechazados = rechazados + 1
    if total == (aceptados + rechazados):
        solicitud = getSolicitudDeCambio(idsolicituddecambio)
        if aceptados > rechazados:
            aplicarCambios(idsolicituddecambio)
            solicitud.estado = 'Aceptado'
        if aceptados < rechazados:
            solicitud.estado = 'Rechazado'
        session.commit()  
      
def revisionLineaBase(idlineabase):
    """Funcion que recibe el id de linea base y pone en estado de revision sus items""" 
    itemList = session.query(Item).filter(Item.idlineabase==idlineabase).all()
    for i in itemList:
        i.estado = 'revision'
        session.commit()
    lb = session.query(LineaBase).filter(LineaBase.idlineabase==idlineabase).first()
    lb.estado = 'abierto'
    session.commit()  
        
        
def aplicarCambios(idsolicituddecambio):
    """Funcion que aplica cambios segun el tipo de solicitud cuando ya 
    todos los miembros han votado"""
    solicitud = getSolicitudDeCambio(idsolicituddecambio)
    item = CtrlFase.getItem(solicitud.iditem)
    idlineabase = item.idlineabase
    lb = CtrlLineaBase.getLB(idlineabase)
    faseactual=lb.idfase
    fase = session.query(Fase).filter(Fase.idfase==lb.idfase).first()
    faseList = session.query(Fase).filter(and_(Fase.posicionfase >= fase.posicionfase,Fase.idproyecto == fase.idproyecto)).all()
    idfaseList = []
    for f in faseList:
        idfaseList.append(f.idfase)
        
    lineabaseList = session.query(LineaBase).filter(and_(LineaBase.estado=='cerrado',LineaBase.idfase.in_(idfaseList))).all()
        
    for lb in lineabaseList:
        revisionLineaBase(lb.idlineabase)
        
    if solicitud.tipo == 'eliminar':
        CtrlFase.eliminarItem(solicitud.iditem)
    elif solicitud.tipo == 'reversionar':
        """Preguntar a Thelma"""
        versionAnt = session.query(VersionItem).filter(VersionItem.estado=='actual').first()
        versionAnt.estado = 'no-actual'
        solicitud.versionitem.estado = 'actual'
        session.commit()
    elif solicitud.tipo == 'modificar':
        versionAnt = session.query(VersionItem).filter(VersionItem.estado=='actual').first()
        versionAnt.estado = 'no-actual'
        versionNva = session.query(VersionItem).filter(VersionItem.idversionitem==solicitud.idversionitem).first()
        versionNva.estado = 'actual'
        session.commit()