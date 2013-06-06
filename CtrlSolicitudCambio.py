from Modelo import engine, SolicitudDeCambio, SolicitudPorUsuarioCC
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.orm import sessionmaker, join
import sqlalchemy.exc

"""Controlador de Solicitudes de Cambio para el modulo de Gestion de Cambios"""  
__author__ = 'Grupo 5'
__date__ = '25-05-2013'
__version__ = '5.0'
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
    solicitud=session.query(SolicitudPorUsuarioCC).filter(and_(SolicitudPorUsuarioCC.idsolicituddecambio==idsolicituddecambio,
                                                               SolicitudPorUsuarioCC.idusuariocc==idintegrante)).first()
    solicitud.voto = voto
    session.commit()
    
def getVotobyCC(idusuario):
    solicitud=session.query(SolicitudPorUsuarioCC).filter(SolicitudPorUsuarioCC.idusuariocc==idusuario).all()
    return solicitud

def getestadoVoto(idsolicituddecambio,idintegrante):
    solicitud=session.query(SolicitudPorUsuarioCC).filter(and_(SolicitudPorUsuarioCC.idsolicituddecambio==idsolicituddecambio,
                                                               SolicitudPorUsuarioCC.idusuariocc==idintegrante)).first()
    return solicitud.voto
    
def contarVotos(idsolicituddecambio):
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
            solicitud.estado = 'Aceptado'
        if aceptados < rechazados:
            solicitud.estado = 'Rechazado'
        session.commit()  