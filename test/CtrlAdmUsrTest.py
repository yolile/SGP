from Usuario import Usuario, get_table 
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.sql import select, delete


engine = create_engine('postgresql+psycopg2://admin:admin@localhost/sgptest')
metadata = MetaData(bind=engine)
usuario_table = get_table(metadata)
mapper(Usuario, usuario_table)
conn = engine.connect() 

def getUsuarioList():
    s = select([usuario_table])
    result = s.execute()
    return result

def buscarUsuario(username):
    usuarioList = getUsuarioList()
    for user in usuarioList:
        if username == user.username:
            return True
    return False

def validarUsuario(username, password):
        usuarioList = getUsuarioList()
        for user in usuarioList:
            if username == user.username:
                if password == user.passwrd:
                    return True
        return False

def getMayorIdUsuario():
    lista = getUsuarioList()
    idusuariomax =0
    for user in lista:
        if idusuariomax < user.idusuario:
            idusuariomax = user.idusuario
    return idusuariomax   

def crearUsr(username,passwrd,nombre,apellido,telefono,ci):
    idusuariomax=getMayorIdUsuario()
    result = usuario_table.insert().execute(idusuario=idusuariomax+1,
                                             username=username, 
                                             passwrd=passwrd,
                                             nombre=nombre, 
                                             apellido=apellido, 
                                             telefono=telefono, 
                                             ci=ci)

def eliminarUsr(iduser):
    conn.execute(usuario_table.delete().where(usuario_table.c.idusuario==iduser)) 
    
    
def modificarUsr(iduser,username,passwrd,nombre,apellido,telefono,ci):
    conn.execute(usuario_table.update().
                    where(usuario_table.c.idusuario==iduser).
                    values(username=username,
                           passwrd=passwrd,
                           nombre=nombre,
                           apellido=apellido,
                           telefono=telefono,
                           ci=ci)
                ) 
def getId(iduser):
    s = select([usuario_table],usuario_table.c.idusuario==iduser)
    result = conn.execute(s)
    row = result.fetchone()
    return row['idusuario']
def getUsername(iduser):
    s = select([usuario_table],usuario_table.c.idusuario==iduser)
    result = conn.execute(s)
    row = result.fetchone()
    return row['username']
def getPasswrd(iduser):
    s = select([usuario_table],usuario_table.c.idusuario==iduser)
    result = conn.execute(s)
    row = result.fetchone()
    return row['passwrd']
def getNombre(iduser):
    s = select([usuario_table],usuario_table.c.idusuario==iduser)
    result = conn.execute(s)
    row = result.fetchone()
    return row['nombre']
def getApellido(iduser):
    s = select([usuario_table],usuario_table.c.idusuario==iduser)
    result = conn.execute(s)
    row = result.fetchone()
    return row['apellido']
def getTelefono(iduser):
    s = select([usuario_table],usuario_table.c.idusuario==iduser)
    result = conn.execute(s)
    row = result.fetchone()
    return row['telefono']
def getCi(iduser):
    s = select([usuario_table],usuario_table.c.idusuario==iduser)
    result = conn.execute(s)
    row = result.fetchone()
    return row['ci']
   

# crearUsr('dinog','secretito','diana','noguera','333333','222222')
# crearUsr('sheka','secretito','jesica','caceres','333333','222222')
# crearUsr('blopa','secretito','pablo','marmol','333333','222222')
# crearUsr('everruiz','secretito','ever','ruiz','333333','222222')
# crearUsr('mjara','secretito','marcelo','jara','333333','222222')
# modificarUsr(1,'dinog','secretote','diana','Noguera','333333','222222')

