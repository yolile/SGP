from Modelo import TipoItem, AtributoTipo, engine
from sqlalchemy.orm import sessionmaker, join
import time
Session = sessionmaker(bind=engine)

session = Session()

def getTipoItemList():
    """Funcion que retorna la lista de todos los tipos de item en la base de datos."""
    result = session.query(TipoItem).all()
    return result

def getMaxIdTipoItem():
    """Funcion que retorna el maximo valor de tipo de items en la base de datos"""
    lista = getTipoItemList()
    idtipomax =0
    for tipoitem in lista:
        if idtipomax < tipoitem.idtipoitem:
            idtipomax = tipoitem.idtipoitem
    return idtipomax  

def crearTipoItem(nombre,descripcion):
    """Funcion que crea un tipo de item y devuelve el idtipoitem generado"""
    session1=Session()
    idtipoitem=getMaxIdTipoItem()+1
    nuevo=TipoItem(idtipoitem,nombre,descripcion)
    session1.add(nuevo)
    session1.commit()
    return nuevo.idtipoitem
    
def getAtributosList():
    """Funcion que devuelve la lista de todos los atributos"""
    result = session.query(AtributoTipo).all()
    return result
    
def getMaxIdAtributo():
    """Funcion que devuelve el maximo valor de idatributo"""
    lista = getAtributosList()
    idatributomax =0
    for atributo in lista:
        if idatributomax < atributo.idatributo:
            idatributomax = atributo.idatributo
    return idatributomax

def agregarAtributo(tipoitem,nombre,tipodato,bydefault):
    """Funcion que agrega un atributo a un item dado"""
    session1=Session()
    idatributo=getMaxIdAtributo()+1
    if(tipoitem!=""):
        nuevo = AtributoTipo(idatributo,tipoitem,nombre,tipodato,bydefault)
        session1.add(nuevo)
        session1.commit()
    
def getAtributosTipo(idtipoitem):
    """Funcion que retorna la lista de todos los atributos de un
    tipo de item dado presentes en la sesion."""
    result = session.query(AtributoTipo).filter(AtributoTipo.idtipoitem==idtipoitem).all()
    return result

def borrarTipoItem(idtipoitem):
    """Funcion que recibe el Id de un tipo de item y lo elimina de la base de datos"""
    session1=Session()
    borrarAtributosTipo(idtipoitem)
    res = session1.query(TipoItem).filter(TipoItem.idtipoitem==idtipoitem).first()
    session1.delete(res)
    session1.commit()

def borrarAtributosTipo(idtipoitem):
    """Recibe un id de tipo de item y borra sus atributos"""
    lista=getAtributosTipo(idtipoitem)
    for atributo in lista:
        borrarAtributo(atributo.idatributo)

def modTipoItem(idtipoitem,nombre,descripcion):
    """Funcion que recibe un id de tipo de item y
    modifica el tipo de item correspondiente"""
    session1=Session()
    tipoitem = session1.query(TipoItem).filter(TipoItem.idtipoitem==idtipoitem).first()
    tipoitem.nombre = nombre
    tipoitem.descripcion = descripcion
    session1.commit()
    
def getNombre(idtipoitem):
    """Devuelve el nombre de un tipo de item dado su id"""
    result = session.query(TipoItem).filter(TipoItem.idtipoitem==idtipoitem).first()
    return result.nombre

def getTipoItem(idtipoitem):
    result = session.query(TipoItem).filter(TipoItem.idtipoitem==idtipoitem).first()
    return result

def getDescripcion(idtipoitem):
    """Devuelve la descripcion de un tipo de item dado su id"""
    result = session.query(TipoItem).filter(TipoItem.idtipoitem==idtipoitem).first()
    return result.descripcion

def valorPorDefectoValido(datatype,valor):
    if valor=="":
        return True
    if datatype=="DATE":
        try:
            valid_date = time.strptime(valor,'%Y-%m-%d')
        except ValueError:
            return False
        return True
    if datatype=="INT":
        return valor.isdigit()
    return True

def borrarAtributo(idatributo):
    """Funcion que recibe el Id de un atributo de tipo de item y lo elimina de la base de datos"""
    session1=Session()
    res = session1.query(AtributoTipo).filter(AtributoTipo.idatributo==idatributo).first()
    session1.delete(res)
    session1.commit()
    
def tipoDeItemNoInstanciado(idtipoitem):
    #Falta implementar. Funcion que retorna si un tipo de item
    #no fue utilizado en un proyecto, o sea si se puede redefinir
    return True

def busquedaTipo(texto):
    return session.query(TipoItem).filter(TipoItem.nombre.like(texto+'%')).all()

def descartarCambios():
    """Funcion que realiza un rollback a la sesion 'session' """
    session.rollback()
    
def guardarCambios():
    """Funcion que guarda los cambios que se realizaron sobre
    la sesion 'session' """
    session.commit()
#===============================================================================
# Las funciones de abajo solo se llevaran a cabo en la sesion global 'session'
# (Para redefinir tipos de item) 
#===============================================================================

def modTipoItemSession(idtipoitem,nombre,descripcion):
    """Funcion que recibe un id de tipo de item y
    modifica el tipo de item correspondiente"""
    tipoitem = session.query(TipoItem).filter(TipoItem.idtipoitem==idtipoitem).first()
    tipoitem.nombre = nombre
    tipoitem.descripcion = descripcion
    
def borrarAtributoSession(idatributo):
    """Funcion que recibe el Id de un atributo de tipo de item y lo elimina"""
    res = session.query(AtributoTipo).filter(AtributoTipo.idatributo==idatributo).first()
    session.delete(res)

def agregarAtributoSession(tipoitem,nombre,tipodato,bydefault):
    """Funcion que agrega un atributo a un item dado"""
    idatributo=getMaxIdAtributo()+1
    if(tipoitem!=""):
        nuevo = AtributoTipo(idatributo,tipoitem,nombre,tipodato,bydefault)
        session.add(nuevo)

