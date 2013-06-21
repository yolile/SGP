from Modelo import *
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.orm import sessionmaker, join
import sqlalchemy.exc
import CtrlFase
import CtrlLineaBase
from Modelo import path
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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

def existeSolicitudPendienteUsuario(idusuario):
    lista=getSolicitudesbyCC(idusuario)
    for solicitud in lista:
        if (solicitud.estado=='en-proceso'):
            return True
    return False
      
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
    elif solicitud.tipo == 'reversionar' or solicitud.tipo == 'modificar':
        versionAnt = CtrlFase.getVersionActual(solicitud.iditem)
        versionNva = session.query(VersionItem).filter(VersionItem.idversionitem==solicitud.idversionitem).first()
        versionNva.estado = 'actual'
        session.commit()
        
def genReport(idproyecto):
    solicitudes = session.query(SolicitudDeCambio).join((Item,SolicitudDeCambio.item)).join((Fase, Item.fase)).join((Proyecto, Fase.proyecto)).filter(Proyecto.idproyecto==idproyecto).all()
    proyecto = session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    doc = SimpleDocTemplate(path+"/reporte_"+proyecto.nombre+".pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
        
    Story=[]
    logo = path+"/static/img/sgplogo.jpg"
 
    formatted_time = time.ctime()

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=10, fontSize=16))
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=14, alignment=0, spaceAfter=10, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=14))
    
    titulo="<b>Reporte de Solicitudes de cambio</b>"
    Story.append(Paragraph(titulo,styles['Principal']))
    
    im = Image(logo, width=250,height=169)
    Story.append(im)

    ptext = '<font size=12>Fecha y hora: %s</font>' % formatted_time 
    Story.append(Paragraph("<br/><br/>"+ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    
    for s in solicitudes:
        voto = session.query(SolicitudPorUsuarioCC).filter(and_(s.idsolicituddecambio==SolicitudPorUsuarioCC.idsolicituddecambio,s.idusuariosolicitante==proyecto.usuariolider)).first()
         
        ptext = s.descripcion
        ptext = ptext+"\n-Estado de la solicitud: "+s.estado
        ptext = ptext+"\n-Voto del usuario lider: "+voto.voto

        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

    doc.build(Story)
    return path+"/reporte_"+proyecto.nombre+".pdf"