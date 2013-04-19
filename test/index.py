from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
import CtrlAdmUsrTestTest
import CtrlAdmRolTest
import CtrlAdmProyTest

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
        valido = CtrlAdmUsrTestTest.validarUsuario(request.form['username'], request.form['password'])
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
    
"""------------------------USUARIOS---------------------------------------"""    
@app.route('/admUsr', methods=['GET','POST'])
def admUsr():
    """Funcion que presenta el menu para administrar usuarios."""  
    if request.method == 'GET':
        listUser = CtrlAdmUsrTestTest.getUsuarioList()
        return render_template('admUsr.html', listUser=listUser, owner=owner)   
    if request.method == 'POST':
        if request.form['opcion'] == "Crear":
            return render_template('crearUsr.html')
        if request.form['opcion'] == "Modificar":
            usr = CtrlAdmUsrTestTest.usr(int(request.form['select']))        
            return render_template('modUsr.html', usr=usr) 
        if request.form['opcion'] == "Eliminar":
            CtrlAdmUsrTestTest.elimUsr(int(request.form['select']))   
            listUser = CtrlAdmUsrTestTest.getUsuarioList()
            flash('Usuario eliminado')
            return render_template('admUsr.html', listUser=listUser) 
        if request.form['opcion'] == "Consultar":
            usr = CtrlAdmUsrTestTest.usr(int(request.form['select']))        
            return render_template('conUsr.html', usr=usr)
        if request.form['opcion'] == "AsignarRoles":
            usr = CtrlAdmUsrTestTest.usr(int(request.form['select']))    
            listRol = CtrlAdmRolTest.getRolList()   
            return render_template('asigRoles.html',usr=usr,listRol = listRol)      
        if request.form['opcion'] == "Buscar":
            listUser = CtrlAdmUsrTestTest.busUsr(request.form['buscar'],
                                         request.form['atributo'])
            flash('Usuarios con'+request.form['atributo']+" igual a "+request.form['buscar'])
            return render_template('admUsr.html', listUser=listUser)
        if request.form['opcion'] == "Home":
            return render_template('main.html')    
       
@app.route('/crearUsr', methods=['GET','POST'])
def crearUsr():
    """Funcion que presenta el menu para crear usuario."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Crear"):        
            CtrlAdmUsrTestTest.crearUsr(request.form['username'], 
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
            CtrlAdmUsrTestTest.modUsr(int(request.form['idusuario']), 
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
            CtrlAdmUsrTestTest.asigRol(request.form.getlist('roles') )
            flash('Roles asignados al usuario')
        return redirect(url_for('admUsr'))       
"""------------------------ROLES---------------------------------------"""         
@app.route('/admRol', methods=['GET','POST'])
def admRol():
    """Funcion que presenta el menu para administrar Roles."""  
    if request.method == 'GET':
        listRol = CtrlAdmRolTest.getRolList()
        return render_template('admRol.html', listRol = listRol)   
    if request.method == 'POST':
        if request.form['opcion'] == "Crear":
            listPermiso = CtrlAdmRolTest.getPermisoList()   
            return render_template('crearRol.html',listPermiso = listPermiso)
        if request.form['opcion'] == "Modificar":
            rol = CtrlAdmRolTest.rol(int(request.form['select']))        
            idpermisos = CtrlAdmRolTest.idPermisoList(int(rol.idrol))   
            listPermiso = CtrlAdmRolTest.getPermisoList()               
            return render_template('modRol.html', rol=rol,
                                                 idpermisos=idpermisos,
                                                 listPermiso=listPermiso) 
        if request.form['opcion'] == "Eliminar":
            CtrlAdmRolTest.elimRol(int(request.form['select']))   
            listRol = CtrlAdmRolTest.getRolList()
            flash('Rol eliminado')
            return render_template('admRol.html', listRol=listRol)
        if request.form['opcion'] == "Consultar":
            rol = CtrlAdmRolTest.rol(int(request.form['select']))        
            idpermisos = CtrlAdmRolTest.idPermisoList(int(rol.idrol))   
            listPermiso = CtrlAdmRolTest.getPermisoList()               
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
            CtrlAdmRolTest.crearRol(request.form['nombre'],
                                request.form['descripcion'],
                                request.form.getlist('permisos') )
            flash('Rol creado')
        return redirect(url_for('admRol'))          

@app.route('/modRol', methods=['GET','POST'])    
def modRol():
    """Funcion que presenta el menu para modificar rol."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Modificar"):
            CtrlAdmRolTest.modRol(int(request.form['idrol']), 
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
        listPermiso = CtrlAdmRolTest.getPermisoList()   
        return render_template('conPerm.html',listPermiso = listPermiso)
    if request.method == 'POST':
        if request.form['opcion'] == "Home":
            return render_template('main.html')  
         
"""------------------------PROYECTOS---------------------------------------"""       
@app.route('/admProy', methods=['GET','POST'])
def admProy():
    """Funcion que presenta el menu para administrar Proyectos."""  
    if request.method == 'GET':
        listaProy = CtrlAdmProyTest.getProyectoList()
        return render_template('admProy.html',listProy=listaProy)
    if request.method == 'POST':
        if request.form['opcion'] == "Crear":
            return render_template('crearProy.html')
        if request.form['opcion'] == "Definir Fases":
            proy = int(request.form['select'])
            listaFases = CtrlAdmProyTest.getFasesListByProy(proy)
            return render_template('defFases.html',listFases=listaFases,proyecto=proy)
        if request.form['opcion'] == "Home":
            return render_template('main.html')                   

@app.route('/crearProy', methods=['GET','POST'])
def crearProy():
    """Funcion que permite crear proyectos"""
    if request.method == 'POST':
        if request.form['opcion'] == "Crear":
            CtrlAdmProyTest.crearProy(request.form['nombre'], 
                                request.form['descripcion'], 
                                request.form['presupuesto'],
                                owner,
                                )
            flash('Proyecto creado')
        return redirect(url_for('admProy'))
    return render_template('crearProy.html')
    
@app.route('/defFases', methods=['GET','POST'])
def defFases():
    """Funcion que permite definir fases dentro de un proyecto"""
    if request.method == 'POST':
        if (request.form['opcion']=="Definir"):
            proy=request.form['proyecto']
            return render_template('crearFase.html',proyecto=proy)

@app.route('/crearFase', methods=['GET','POST'])
def crearFase():
    """Funcion que permite crear una fase de un proyecto"""
    if request.method == 'POST':
        if request.form['opcion']=="Crear":
            CtrlAdmProyTest.crearFase(request.form['nombre'],request.form['descripcion'],request.form['idproyecto'])
            flash('Fase creada')
    return redirect(url_for('defFases'))


if __name__=='__main__':
    app.run()