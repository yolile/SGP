from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
import CtrlAdmUsr

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

@app.route('/admUsr', methods=['GET','POST'])
def admUsr():
    """Funcion que presenta el menu para administrar usuarios."""  
    if request.method == 'GET':
        listUser = CtrlAdmUsr.getUsuarioList()
        return render_template('admUsr.html', listUser=listUser)   
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
            return render_template('conUsr.html', usr=usr) 
        if request.form['opcion'] == "Buscar":
            listUser = CtrlAdmUsr.busUsr(request.form['buscar'],
                                         request.form['atributo'])
            flash('Usuarios con'+request.form['atributo']+" igual a "+request.form['buscar'])
            return render_template('admUsr.html', listUser=listUser)               
if __name__=='__main__':
    app.run()