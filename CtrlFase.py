from Modelo import *
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.orm import sessionmaker, join
from datetime import *

"""Controlador de Fases en el modulo de desarrollo"""  
__author__ = 'Grupo 5'
__date__ = '01-05-2013'
__version__ = '1.0'
__text__ = 'Este modulo contiene funciones que permiten el control de las fases en el modulo de desarrollo'
__file__ = 'CtrlFase.py'      
    
#engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgptest')
Session = sessionmaker(bind=engine)
session = Session() 
sumacosto=0
sumaimpacto=0
visitados=[]
    
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
     global session
     session1 = Session.object_session(item)
     if(session1!=None):
         session=session1
     #proyecto = session.query(Proyecto).join((Fase.proyecto,Proyecto)).filter(Fase.idfase==item.idfase).first()
     #proyecto.presupuesto = proyecto.presupuesto - versionitem.costo
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

def instanciarVersionItem(iditem,idusuario,descripcion,complejidad,prioridad,costo,version,estado):
    """Funcion que devuelve el objeto Version Item de acuerdo 
    con los atributos pasados como parametros"""
    idversionitem=getMaxIdVersionItem()+1
    nuevo = VersionItem(idversionitem, iditem, idusuario,descripcion,complejidad,prioridad,costo,version,estado)
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
    """Funcion para obtener la version actual de VersionItem"""
    versiones = session.query(VersionItem).filter(and_(VersionItem.iditem==iditem,
                                                     VersionItem.estado!='pendiente',
                                                     VersionItem.estado!='no-actual')).all()
    idversionmax = 0
    versionmax = None
    for version in versiones:
        if(version.idversionitem > idversionmax):
            idversionmax = version.idversionitem
            versionmax = version
    return versionmax

def finalizarFase(idfase):
    """Funcion utilizada para finalizar la fase. 
    Comprueba si los items pertenecen a alguna linea base y si es asi 
    comprueba que la linea base este cerrada"""
    listItem = getItemsFase(idfase)
    for i in listItem:
        if i.idlineabase == None:
            return False
        lb = session.query(LineaBase).filter(LineaBase.idlineabase==i.idlineabase).first()
        if lb.estado != 'cerrado':
            return False
    fase = session.query(Fase).filter(Fase.idfase==idfase).first()
    fase.estado='finalizado'
    session.commit()
    return True

def getArchivoList():
    """Funcion que retorna la lista de todos los archivos"""
    result = session.query(Archivo).all()
    return result

def getIdArchivosByItem(iditem):
    """Funcion que recibe un id de un item y retorna la lista de los 
    id de todos los archivos adjuntos al item"""
    item = session.query(Item).filter(Item.iditem==iditem).first()
    idarchivos = []
    for a in item.archivos:
        idarchivos.append(a.idarchivo)
    return idarchivos

def getMaxIdArchivo():
    """Funcion que retorna el maximo valor de la idVersion de un item"""
    lista = getArchivoList()
    idarchivomax = 0
    for archivo in lista:
        if idarchivomax < archivo.idarchivo:
            idarchivomax = archivo.idarchivo
    return idarchivomax

def subir(archivo):
    """Funcion que recibe un archivo y lo persiste en la base de datos"""
    nuevo = Archivo(getMaxIdArchivo()+1,archivo.read(),archivo.filename)
    session.add(nuevo)
    session.commit()
            
def descargar(idarchivo):
    """Funcion que recibe el id de un archivo y retorna el objeto archivo dado el id recibido"""
    archivo = session.query(Archivo).filter(Archivo.idarchivo==idarchivo).first()
    arc = open("archivo", 'w')
    arc.write(archivo.archivo)
    arc.close()
    return archivo

def adjuntar(iditem,idarchivos):
    """Funcion que recibe el item y la lista de los archivos, para asignarle archivos a un item """
    item = session.query(Item).filter(Item.iditem==iditem).first()
    listaArchivos = session.query(Archivo).filter(Archivo.idarchivo.in_(idarchivos)).all()
    item.archivos = listaArchivos
    session.commit()
    
def busquedaArchivo(parametro,atributo):
    """Funcion que recibe un parametro de busqueda, el atributo y retorna coincidencias"""
    if atributo == 'nombre':
        result = session.query(Archivo).filter(Archivo.nombre.like(parametro+'%')).all()
    return result

def eliminarItem(iditem):
    item = session.query(Item).filter(Item.iditem==iditem).first()
    item.estado='eliminado'
    item.idlineabase=None
    relaciones = session.query(Relacion).filter(or_(Relacion.alitem==iditem,Relacion.delitem==iditem)).all()
    for r in relaciones:
        session.delete(r)
    session.commit()

def getSolicitudCambioList():
    result = session.query(SolicitudDeCambio).all()
    return result

def getMaxIdSolicitudCambio():
    """Funcion que retorna el maximo valor de la idVersion de un item"""
    lista = getSolicitudCambioList()
    idsolicitudmax = 0
    for solicitud in lista:
        if idsolicitudmax < solicitud.idsolicituddecambio:
            idsolicitudmax = solicitud.idsolicituddecambio
    return idsolicitudmax
    
def enviarSolicitud(idusuariosolicitante,tipo,iditem,versionitem,costo,impacto):
    usuario = session.query(Usuario).filter(Usuario.idusuario==idusuariosolicitante).first()
    item = session.query(Item).filter(Item.iditem==iditem).first()
    fase = session.query(Fase).filter(Fase.idfase==item.idfase).first()
    lineabase = session.query(LineaBase).filter(LineaBase.idlineabase==item.idlineabase).first()
    proyecto = session.query(Proyecto).filter(Proyecto.idproyecto==fase.idproyecto).first()
    
    des_usuario = '-Usuario: '+usuario.username+'\n'
    des_fecha='-Fecha: '+date.today().strftime('%d/%m/%Y')+'\n'
    des_proyecto='-Proyecto: '+proyecto.nombre+'\n'
    des_fase='-Fase: '+fase.nombre+'\n'
    des_lineabase='-Linea Base: '+str(lineabase.numero)+'\n'
    des_item='-Item: '+item.nombre
    descripcion = des_usuario+des_fecha+des_proyecto+des_fase+des_lineabase+des_item

    if tipo == 'reversionar':    
        nuevo = SolicitudDeCambio(getMaxIdSolicitudCambio()+1, 
                                  idusuariosolicitante, 
                                  descripcion,
                                  tipo,
                                  iditem,
                                  versionitem.idversionitem,
                                  'en-proceso',
                                  costo+' Gs.',
                                  impacto)
    elif tipo == 'modificar':
        version = 0
        lista = getVersionItemList()
        for v in lista:
            if version < v.version and v.iditem==iditem:
                version = v.version
    
        nuevoVersion = VersionItem(getMaxIdVersionItem()+1, 
                                   iditem, 
                                   usuario.idusuario,
                                   versionitem.descripcion,
                                   versionitem.complejidad,
                                   versionitem.prioridad,
                                   versionitem.costo,
                                   version+1,
                                   'no-actual')

        session.add(nuevoVersion)
        session.commit()
        
        nuevo = SolicitudDeCambio(getMaxIdSolicitudCambio()+1, 
                                  idusuariosolicitante, 
                                  descripcion,
                                  tipo,
                                  iditem,
                                  nuevoVersion.idversionitem,
                                  'en-proceso',
                                  costo+' Gs',
                                  impacto)


    elif tipo == 'eliminar':
        nuevo = SolicitudDeCambio(getMaxIdSolicitudCambio()+1, 
                                  idusuariosolicitante, 
                                  descripcion,
                                  tipo,
                                  iditem,
                                  None,
                                  'en-proceso',
                                  costo+' Gs',
                                  impacto)
    solicitudCC = []
    for u in proyecto.comitecambios:
        solicitudCC.append(SolicitudPorUsuarioCC(nuevo.idsolicituddecambio,u.idusuario,proyecto.idproyecto,'Pendiente'))
    
    session.add(nuevo)
    session.commit()
    session.add_all(solicitudCC)
    session.commit()
    
def modificarItem(iditem,versionitem,idusuario):
    actual = getVersionActual(iditem)
    actual.estado='no-actual'
    session.commit()
    
    version = 0
    lista = getVersionItemList()
    for v in lista:
        if version < v.version and v.iditem==iditem:
            version = v.version
    
    nuevo = instanciarVersionItem(iditem,
                                  idusuario,
                                  versionitem.descripcion,
                                  versionitem.complejidad,
                                  versionitem.prioridad,
                                  versionitem.costo,
                                  version+1,
                                  'actual')
    
    session.add(nuevo)
    session.commit()
    
def existeSolicitudPendiente(iditem):
    listaSC = session.query(SolicitudDeCambio).filter(SolicitudDeCambio.iditem==iditem).all()
    for sc in listaSC:
        if sc.estado == 'en-proceso':
            return True 
    return False

def getListVersionbyIdItem(iditem):
    lista = session.query(VersionItem).filter(VersionItem.iditem==iditem).all()
    return lista

def getVersion(idversionitem):
    version = session.query(VersionItem).filter(VersionItem.idversionitem==idversionitem).first()
    return version

def reversionar(idversionitem,iduser):
    oldversion = getVersion(idversionitem)
    oldversion.estado = 'no-actual'
    idnuevaversion = getMaxIdVersionItem()+1
    nuevonroversion = getVersionActual(oldversion.iditem).version+1
    newversion = VersionItem(idnuevaversion, 
                             oldversion.iditem,
                             iduser,
                             oldversion.descripcion,
                             oldversion.complejidad,
                             oldversion.prioridad,
                             oldversion.costo,
                             nuevonroversion,
                             'actual')
    session.add(newversion)
    session.commit()

def copiarDatosItem(itemorigen,item,versionitem):
    """Funcion utilizada para importar item, que copia todos los datos de un item origen 
    con su ultima version a un item destino tambien en la ultima version. No se copian 
    las claves primarias"""
    item.nombre=itemorigen.nombre+'-copia'
    item.estado=itemorigen.estado
    item.idtipoitem=itemorigen.idtipoitem
    for atributo in itemorigen.atributos:
        newatributo=AtributoItemPorTipo(item.iditem,
                                        atributo.idatributo,
                                        atributo.valor)
        item.atributos.append(newatributo)
    return item

def copiarDatosVersion(versionorigen,versionitem):
    """Funcion utilizada para importar item. Copia los datos de una version especifica
    a la primera version de un nuevo item"""
    versionitem.descripcion=versionorigen.descripcion
    versionitem.complejidad=versionorigen.complejidad
    versionitem.prioridad=versionorigen.prioridad
    versionitem.costo=versionorigen.costo
    versionitem.version=1
    versionitem.estado='actual'
    return versionitem

def revivirItem(iditem):
    item = session.query(Item).filter(Item.iditem==iditem).first()
    item.estado = 'desarrollo'
    session.commit()    
    
def recorridoEnProfundidad(item):
    """Funcion que llama a la funcion que recorre el grafo en profundidad para hallar
    el total de los costos y las complejidades de un item. Retorna un vector en el 
    que el primer elemento es el costo y el segundo es el impacto"""
    #proyecto = getItem(iditem).fase.proyecto
    proyecto=item.fase.proyecto
    listaitems = getItemsProyecto(proyecto.idproyecto)
    maxiditem = getMaxIdItemEnLista(listaitems)
    global sumacosto, sumaimpacto,visitados
    visitados = [0]*(maxiditem+1)
    sumacosto=0
    sumaimpacto=0
    recorrer(item.iditem)
    ret = [sumacosto,sumaimpacto]
    return ret

def recorrer(iditem):
    """Funcion recursiva que calcula sumas de los items recorriendo el grafo en profundidad"""
    global sumacosto, sumaimpacto, visitados
    visitados[iditem]=1
    #print ('Visite  el item '+str(iditem))
    version=getVersionActual(iditem)
    sumacosto = sumacosto + version.costo
    sumaimpacto = sumaimpacto + version.complejidad
    relaciones = getRelaciones(iditem)
    for relacion in relaciones:
        if(visitados[relacion.alitem]==0):
            recorrer(relacion.alitem)
    
def getItemsProyecto(idproyecto):
    lista = []
    proyecto=session.query(Proyecto).filter(Proyecto.idproyecto==idproyecto).first()
    for fase in proyecto.fases:
        for item in fase.items:
            if (item.estado != 'eliminado'):
                lista.append(item)
    return lista

def getMaxIdItemEnLista(lista):   
    max=0
    for item in lista:
        if item.iditem>max:
            max=item.iditem
    return max
