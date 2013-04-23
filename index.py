from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
import CtrlAdmUsr
import CtrlAdmRol
import CtrlAdmProy

"""Modulo de ejecucion principal de SGP"""  
__author__ = 'Grupo 5'
__date__ = '03/04/13'
__version__ = '1.0'
__credits__ = 'none'
__text__ = 'indice principal que conmuta con las diferentes funcionalidades de SGP'
__file__ = 'index.py' 

app = Flask(__name__)
app.debug = True
app.secret_key = 'secreto'
app.config.from_object(__name__)
app.config.from_envvar('SGP_SETTINGS', silent=True)

owner=""
proyectoRoy=0
"""fases creadas es una variable global que ayuda a saber si fueron creadas
nuevas fases dentro de la llamada defFases"""
fasesCreadas=0

@app.route('/')
def index():
    """Funcion principal."""  
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Funcion de logueo con los metodos GET y Post."""  
    if request.method == 'GET':
        return render_template('login.html')        
    if request.method == 'POST':
        valido = CtrlAdmUsr.validarUsuario(request.form['username'], request.form['password'])
        if valido:
            global owner 
            owner = request.form['username']
            session['logged_in'] = True
            flash('Estas logueado')
            return redirect(url_for('menu'))
        return render_template('login.html', error='Username invalido o Password invalido')

@app.route('/logout')
def logout():
    """Funcion de deslogueo."""  
    session.pop('logged_in', None)
    flash('Estas deslogueado')
    return redirect(url_for('login'))

@app.route('/menu', methods=['GET','POST'])
def menu():
    """Funcion que presenta el menu principal."""  
    if request.method == 'GET':
        return render_template('main.html') 
    
"""------------------------MODIFICAR CUENTA---------------------------------------"""    
@app.route('/conCnt', methods=['GET','POST'])
def conCnt():
    if request.method == 'GET':
            idusuario = CtrlAdmUsr.getIdByUsername(owner)        
            usr = CtrlAdmUsr.usr(idusuario) 
            return render_template('conCnt.html', usr=usr)  
    if request.method == 'POST':
        if(request.form['opcion'] == "Modificar"):
            CtrlAdmUsr.modUsr(int(request.form['idusuario']), 
                              request.form['username'], 
                              request.form['passwrd'], 
                              request.form['nombre'],
                              request.form['apellido'],
                              request.form['telefono'],
                              int(request.form['ci']))
            flash('Cuenta Modificada')
        return redirect(url_for('menu'))           
"""------------------------USUARIOS---------------------------------------"""    
@app.route('/admUsr', methods=['GET','POST'])
def admUsr():
    """Funcion que presenta el menu para administrar usuarios."""  
    if request.method == 'GET':
         if CtrlAdmUsr.havePermission(owner,200):
             listUser = CtrlAdmUsr.getUsuarioList()
             return render_template('admUsr.html', listUser=listUser, owner=owner)
         else:
             flash('No tiene permisos para realizar esta operacion ')
             return redirect(url_for('menu')) 
    if request.method == 'POST':
        if request.form['opcion'] == "Crear":
            return render_template('crearUsr.html')
        if request.form['opcion'] == "Modificar":
            usr = CtrlAdmUsr.usr(int(request.form['select']))        
            return render_template('modUsr.html', usr=usr) 
        if request.form['opcion'] == "Eliminar":
            CtrlAdmUsr.elimUsr(int(request.form['select']))   
            listUser = CtrlAdmUsr.getUsuarioList()
            flash('Usuario eliminado')
            return render_template('admUsr.html', listUser=listUser) 
        if request.form['opcion'] == "Consultar":
            usr = CtrlAdmUsr.usr(int(request.form['select'])) 
            idroles = CtrlAdmUsr.idRolList(int(usr.idusuario))  
            listRol = CtrlAdmRol.getRolList()     
            return render_template('conUsr.html',usr=usr,
                                                idroles=idroles,
                                                listRol=listRol)
        if request.form['opcion'] == "AsignarRoles":
            usr = CtrlAdmUsr.usr(int(request.form['select']))    
            listRol = CtrlAdmRol.getRolList()     
            idroles = CtrlAdmUsr.idRolList(int(request.form['select']))
            return render_template('asigRoles.html',usr=usr,listRol = listRol, idroles=idroles)                  
        if request.form['opcion'] == "Buscar":
            listUser = CtrlAdmUsr.busquedaUsr(request.form['buscar'],
                                         request.form['atributo'])
            flash('Resultado de la busqueda')
            return render_template('admUsr.html', listUser=listUser)
        if request.form['opcion'] == "Home":
            return render_template('main.html')    
       
@app.route('/crearUsr', methods=['GET','POST'])
def crearUsr():
    """Funcion que presenta el menu para crear usuario."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Crear"):        
            CtrlAdmUsr.crearUsr(request.form['username'], 
                                request.form['passwrd'], 
                                request.form['nombre'],
                                request.form['apellido'],
                                request.form['telefono'],
                                request.form['ci'])
            flash('Usuario creado')
        return redirect(url_for('admUsr')) 

@app.route('/modUsr', methods=['GET','POST'])    
def modUsr():
    """Funcion que presenta el menu para modificar usuario."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Modificar"):
            CtrlAdmUsr.modUsr(int(request.form['idusuario']), 
                              request.form['username'], 
                              request.form['passwrd'], 
                              request.form['nombre'],
                              request.form['apellido'],
                              request.form['telefono'],
                              int(request.form['ci']))
            flash('Usuario modificado')
        return redirect(url_for('admUsr'))
          
@app.route('/asigRoles', methods=['GET','POST'])
def asigRoles():
    """Funcion que presenta el menu para asignar Roles a los usuarios."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Aceptar"): 
            CtrlAdmUsr.asigRoles(int(request.form['idusuario']),
                                 request.form.getlist('roles'))
            flash('Roles asignados al usuario')
    return redirect(url_for('admUsr'))       
"""------------------------ROLES---------------------------------------"""         
@app.route('/admRol', methods=['GET','POST'])
def admRol():
    """Funcion que presenta el menu para administrar Roles."""  
    if request.method == 'GET':
        if CtrlAdmUsr.havePermission(owner,201):
            listRol = CtrlAdmRol.getRolList()
            return render_template('admRol.html', listRol = listRol)
        else:
             flash('No tiene permisos para realizar esta operacion ')
             return redirect(url_for('menu'))           
    if request.method == 'POST':
        if request.form['opcion'] == "Crear":
            listPermiso = CtrlAdmRol.getPermisoList()   
            return render_template('crearRol.html',listPermiso = listPermiso)
        if request.form['opcion'] == "Modificar":
            rol = CtrlAdmRol.rol(int(request.form['select']))        
            idpermisos = CtrlAdmRol.idPermisoList(int(rol.idrol))   
            listPermiso = CtrlAdmRol.getPermisoList()               
            return render_template('modRol.html', rol=rol,
                                                 idpermisos=idpermisos,
                                                 listPermiso=listPermiso) 
        if request.form['opcion'] == "Eliminar":
            CtrlAdmRol.elimRol(int(request.form['select']))   
            listRol = CtrlAdmRol.getRolList()
            flash('Rol eliminado')
            return render_template('admRol.html', listRol=listRol)
        if request.form['opcion'] == "Consultar":
            rol = CtrlAdmRol.rol(int(request.form['select']))        
            idpermisos = CtrlAdmRol.idPermisoList(int(rol.idrol))   
            listPermiso = CtrlAdmRol.getPermisoList()               
            return render_template('conRol.html', rol=rol,
                                                    idpermisos=idpermisos,
                                                    listPermiso=listPermiso)
        if request.form['opcion'] == "Home":
            return render_template('main.html') 
        
@app.route('/crearRol', methods=['GET','POST'])
def crearRol():
    """Funcion que presenta el menu para crear Rol."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Crear"): 
            CtrlAdmRol.crearRol(request.form['nombre'],
                                request.form['descripcion'],
                                request.form.getlist('permisos') )
            flash('Rol creado')
        return redirect(url_for('admRol'))          

@app.route('/modRol', methods=['GET','POST'])    
def modRol():
    """Funcion que presenta el menu para modificar rol."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Modificar"):
            CtrlAdmRol.modRol(int(request.form['idrol']), 
                              request.form['nombre'],
                              request.form['descripcion'], 
                              request.form.getlist('idpermisos'))
            flash('Rol modificado')
        return redirect(url_for('admRol')) 
    
"""------------------------Permisos---------------------------------------"""
@app.route('/conPerm', methods=['GET','POST'])
def conPerm():
    """Funcion que presenta visualiza los permisos del sistema"""  
    if request.method == 'GET':
        listPermiso = CtrlAdmRol.getPermisoList()   
        return render_template('conPerm.html',listPermiso = listPermiso)
    if request.method == 'POST':
        if request.form['opcion'] == "Home":
            return render_template('main.html')  
         
"""------------------------PROYECTOS---------------------------------------"""       
@app.route('/admProy', methods=['GET','POST'])
def admProy():
    """Funcion que presenta el menu para administrar Proyectos."""  
    if request.method == 'GET':
        if CtrlAdmUsr.havePermission(owner,202):
            listaProy = CtrlAdmProy.getProyectoList()
            return render_template('admProy.html',listProy=listaProy)
        else:
            flash('No tiene permisos para realizar esta operacion ')
            return redirect(url_for('menu')) 
    if request.method == 'POST':
        if request.form['opcion'] == "Crear":
            return render_template('crearProy.html')
        if request.form['opcion'] == "Definir Fases":
            global proyectoRoy
            global fasesCreadas
            fasesCreadas=0
            proyectoRoy = int(request.form['select'])
            return redirect(url_for('defFases'))
        if request.form['opcion'] == "Home":
            return render_template('main.html')
        return redirect(url_for('admProy'))                 

@app.route('/crearProy', methods=['GET','POST'])
def crearProy():
    """Funcion que permite crear proyectos"""
    if request.method == 'POST':
        if request.form['opcion'] == "Crear":
            CtrlAdmProy.crearProy(request.form['nombre'], 
                                request.form['descripcion'], 
                                request.form['presupuesto'],
                                owner,
                                )
            flash('Proyecto creado')
        return redirect(url_for('admProy'))
    
@app.route('/defFases', methods=['GET','POST'])
def defFases():
    """Funcion que permite definir fases dentro de un proyecto"""
    if request.method == 'GET':
        listaFases = CtrlAdmProy.getFasesListByProy(proyectoRoy)
        return render_template('defFases.html',listFases=listaFases,proyecto=proyectoRoy)
    if request.method == 'POST':
        proy=request.form['proyecto']
        if (request.form['opcion']=="Definir"):
            if(CtrlAdmProy.getProyEstado(proy)=='no-iniciado'):
               return render_template('crearFase.html',idproyecto=proy)
            else:
                 flash('Proyecto Iniciado, imposible definir mas fases')
                 return redirect(url_for('defFases'))
        if (request.form['opcion']=="Volver a ADM Proyectos"):
             global fasesCreadas
             if(fasesCreadas != 0):
                 CtrlAdmProy.setProyIniciado(proy)
                 fasesCreadas = 0
             return redirect(url_for('admProy'))
        return redirect(url_for('defFases'))

@app.route('/crearFase', methods=['GET','POST'])
def crearFase():
    """Funcion que permite crear una fase de un proyecto"""
    if request.method == 'POST':
        project=int(request.form['idproyecto'])
        if request.form['opcion']=="Crear":
            CtrlAdmProy.crearFase(request.form['nombre'],
                                  request.form['descripcion'],
                                  project)
            flash('Fase creada')
            global fasesCreadas
            fasesCreadas=fasesCreadas+1
        listaFases = CtrlAdmProy.getFasesListByProy(project)
        return render_template('defFases.html',listFases=listaFases,proyecto=project) 
                         
"""------------------------Tipos de Items---------------------------------------"""
@app.route('/tipoItem', methods=['GET','POST'])
def tipoItem():
    """Funcion que presenta la administracion de los tipos de Items del sistema"""  
    if request.method == 'GET':
        return render_template('tipoItem.html')
    if request.method == 'POST':
        if request.form['opcion'] == "Home":
            return render_template('main.html') 

if __name__=='__main__':
    app.run()
