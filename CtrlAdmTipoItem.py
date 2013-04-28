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
    idtipoitem=getMaxIdTipoItem()+1
    nuevo=TipoItem(idtipoitem,nombre,descripcion)
    session.add(nuevo)
    session.commit()
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
    idatributo=getMaxIdAtributo()+1
    nuevo = AtributoTipo(idatributo,tipoitem,nombre,tipodato,bydefault)
    session.add(nuevo)
    session.commit()
    
def getAtributosTipo(idtipoitem):
    """Funcion que retorna la lista de todos los atributos de un
    tipo de item dado presentes en la sesion."""
    result = session.query(AtributoTipo).filter(AtributoTipo.idtipoitem==idtipoitem).all()
    return result

def borrarTipoItem(idtipoitem):
    """Funcion que recibe el Id de un tipo de item y lo elimina de la base de datos"""
    res = session.query(TipoItem).filter(TipoItem.idtipoitem==idtipoitem).first()
    session.delete(res)
    session.commit()

def modTipoItem(idtipoitem,nombre,descripcion):
    """Funcion que recibe un id de tipo de item y
    modifica el tipo de item correspondiente"""
    tipoitem = session.query(TipoItem).filter(TipoItem.idtipoitem==idtipoitem).first()
    tipoitem.nombre = nombre
    tipoitem.descripcion = descripcion
    session.commit()
    
def getNombre(idtipoitem):
    """Devuelve el nombre de un tipo de item dado su id"""
    result = session.query(TipoItem).filter(TipoItem.idtipoitem==idtipoitem).first()
    return result.nombre

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
