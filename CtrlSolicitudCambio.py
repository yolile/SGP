from Modelo import engine, SolicitudDeCambio, SolicitudPorUsuarioCC
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.orm import sessionmaker, join
import sqlalchemy.exc

"""Controlador de Solicitudes de Cambio para el modulo de Gestion de Cambios"""  
__author__ = 'Grupo 5'
__date__ = '16-05-2013'
__version__ = '4.0'
__text__ = 'Este modulo contiene funciones que permiten el control de las Solicitudes de cambio en el modulo de Gestion de Cambios'
__file__ = 'CtrlSolicitudCambio.py'     

Session = sessionmaker(bind=engine)
session = Session()

def getSolicitudesbyCC(idusuario):
    lista = session.query(SolicitudDeCambio).join((SolicitudPorUsuarioCC.solicituddecambio,SolicitudDeCambio)).filter(SolicitudPorUsuarioCC.idusuariocc==idusuario).all()
    return lista

def getSolicitudDeCambio(idsolicituddecambio):
    solicitud = session.query(SolicitudDeCambio).filter(SolicitudDeCambio.idsolicituddecambio==idsolicituddecambio).first()
    return solicitud