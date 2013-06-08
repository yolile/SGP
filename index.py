from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash, _app_ctx_stack, send_file
import os
import CtrlAdmUsr
import CtrlAdmRol
import CtrlAdmProy
import CtrlAdmTipoItem
import CtrlFase
import CtrlLineaBase
import CtrlSolicitudCambio
from flask.exceptions import BadRequest

"""Modulo de ejecucion principal de SGP"""  
__author__ = 'Grupo 5'
__date__ = '04/05/13'
__version__ = '3.0'
__credits__ = 'none'
__text__ = 'indice principal que conmuta con las diferentes funcionalidades de SGP'
__file__ = 'index.py' 

app = Flask(__name__,template_folder='/home/thelma/git/SGP/templates')
app.debug = True
app.secret_key = 'secreto'
app.config.from_object(__name__)
app.config.from_envvar('SGP_SETTINGS', silent=True)
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

owner=""
proyecto=0
item=None
versionitem=None
listaAtributoItemPorTipo=[]

idfase=0
iditem=0
tipo=''
importar=0
idsolicituddecambio=0


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
@app.route('/confCnt', methods=['GET','POST'])
def confCnt():
    if request.method == 'GET':
            global owner
            idusuario = CtrlAdmUsr.getIdByUsername(owner)        
            usr = CtrlAdmUsr.usr(idusuario) 
            return render_template('confCnt.html', usr=usr)  
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
         global owner
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
        global owner
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
        if request.form['opcion'] == "Buscar":
            listRol = CtrlAdmRol.busquedaRol(request.form['buscar'],
                                         request.form['atributo'])
            flash('Resultado de la busqueda')
            return render_template('admRol.html', listRol=listRol)
        
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
        if request.form['opcion'] == "Buscar":
            listPermiso = CtrlAdmRol.buscarPermiso(request.form['buscar'])
            flash('Resultado de la busqueda')
            return render_template('conPerm.html',listPermiso=listPermiso)        
        if request.form['opcion'] == "Home":
            return render_template('main.html')  
         
"""------------------------PROYECTOS---------------------------------------"""       
@app.route('/admProy', methods=['GET','POST'])
def admProy():
    """Funcion que presenta el menu para administrar Proyectos."""
    if request.method == 'GET':
        global owner
        if CtrlAdmUsr.havePermission(owner,202):
            listaProy = CtrlAdmProy.getProyectoList()
            return render_template('admProy.html',listProy=listaProy)
        else:
            flash('No tiene permisos para realizar esta operacion ')
            return redirect(url_for('menu')) 
    if request.method == 'POST':
        global proyecto
        if request.form['opcion'] == "Crear":
            return render_template('crearProy.html')
        if request.form['opcion'] == "Definicion de Fases":
            proyecto=int(request.form['select'])
            proy = CtrlAdmProy.proy(proyecto)  
            if proy.estado == 'iniciado':
                flash("Proyecto iniciado, imposible definir mas fases")
                return redirect(url_for('admProy'))
            return redirect(url_for('defFases'))
        if request.form['opcion'] == "Comite de Cambios":
            proyecto = int(request.form['select'])
            return redirect(url_for('admCC'))            
#             listMiembros = CtrlAdmProy.getMiembrosList(int(request.form['select']))
#             return render_template('admCC.html', 
#                                    listUser=listMiembros, 
#                                    idproyecto=request.form['select'])
        if request.form['opcion'] == "Buscar":
            listProy = CtrlAdmProy.busquedaProy(request.form['buscar'],
                                         request.form['atributo'])            
            flash('Resultado de la busqueda')
            return render_template('admProy.html',listProy=listProy)
        if request.form['opcion'] == "Eliminar":
            CtrlAdmProy.elimProy(int(request.form['select']))   
            listaProy = CtrlAdmProy.getProyectoList()
            flash('Proyecto eliminado')
            return render_template('admProy.html',listProy=listaProy)
        if request.form['opcion'] == "Modificar":
            proyecto=int(request.form['select'])
            proy = CtrlAdmProy.proy(proyecto)  
            return render_template('modProy.html', proyecto=proy) 
        if request.form['opcion'] == "Home":
            return render_template('main.html')
        if request.form['opcion'] == "Consultar":
            proyecto=int(request.form['select'])
            return redirect(url_for('conProy'))
        if request.form['opcion'] == "Importar":
            proyecto=int(request.form['select'])
            proy = CtrlAdmProy.proy(proyecto) 
            return render_template('importarProy.html',proyecto=proy)
        if request.form['opcion'] == "Calcular costo total":
            proyecto=int(request.form['select'])
            costototal=CtrlFase.calcularCostoTotal(proyecto)
            listaProy = CtrlAdmProy.getProyectoList()
            return render_template('admProy.html',listProy=listaProy, costototal=costototal)
            #return render_template('costoTotal.html',costototal=costototal)
        if request.form['opcion'] == "Finalizar":
            proyecto=int(request.form['select'])
            if (CtrlAdmProy.finalizarProyecto(proyecto)):
                flash('El proyecto ha sido finalizado exitosamente')
            else:
                flash('El proyecto no se puede finalizar, existen fases en desarrollo')
        return redirect(url_for('admProy'))                 

@app.route('/crearProy', methods=['GET','POST'])
def crearProy():
    """Funcion que permite crear proyectos"""
    if request.method == 'POST':
        global owner
        if request.form['opcion'] == "Crear":
            CtrlAdmProy.crearProy(request.form['nombre'], 
                                request.form['descripcion'], 
                                request.form['presupuesto'],
                                owner,
                                )
            flash('Proyecto creado')
        return redirect(url_for('admProy'))
    
@app.route('/modProy', methods=['GET','POST'])    
def modProy():
    """Funcion que presenta el menu para modificar proyecto."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Modificar"):
            CtrlAdmProy.modProy(int(request.form['idproyecto']), 
                              request.form['nombre'],
                              request.form['descripcion'],
                              int(request.form['presupuesto']))
            flash('Proyecto modificado')
        return redirect(url_for('admProy'))

@app.route('/conProy', methods=['GET','POST'])    
def conProy():
    """Funcion que presenta los datos de un proyecto."""
    global proyecto
    if request.method == 'GET':
        return render_template('conProy.html',proyecto=CtrlAdmProy.proy(proyecto))
    if request.method == 'POST':
        if (request.form['opcion']=='Atras'):
            return redirect(url_for('admProy'))
        if(request.form['opcion'] == "Consultar Tipos de Item"):
            try:
                fase=CtrlAdmProy.getFase(int(request.form['select']))
                return render_template("conTipoItemFase.html",fase=fase)
            except BadRequest:
                flash('Ninguna fase seleccionada')
                return redirect(url_for('conProy'))
        if(request.form['opcion'] == "Consultar Roles"):
            try:
                fase=CtrlAdmProy.getFase(int(request.form['select']))
                return render_template("conRolFase.html",fase=fase)
            except BadRequest:
                flash('Ninguna fase seleccionada')
                return redirect(url_for('conProy'))
            
@app.route('/importarProy', methods=['GET','POST'])    
def importarProy():
    """Funcion que presenta el menu permitiendo importar un proyecto."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Aceptar"):
            global owner
            idproyecto=CtrlAdmProy.importarProy(request.form['idproyecto'],
                                                owner)
            CtrlAdmProy.modProy(idproyecto,
                                request.form['nombre'],
                                request.form['descripcion'],
                                int(request.form['presupuesto']))
            flash('Proyecto importado')
        return redirect(url_for('admProy'))
    
@app.route('/defFases', methods=['GET','POST'])
def defFases():
    """Funcion que permite administrar fases dentro de un proyecto"""
    if request.method == 'GET':
        global proyecto
        listaFases = CtrlAdmProy.getFasesListByProy(proyecto)
        return render_template('defFases.html',listFases=listaFases,proyecto=proyecto)
    if request.method == 'POST':
        global owner
        proy=request.form['proyecto']
        if (request.form['opcion']=="Nueva Fase"):
            if(CtrlAdmProy.getProyEstado(proy)=='no-iniciado'):
               return render_template('crearFase.html',idproyecto=proy)
            else:
                 flash('Proyecto Iniciado, imposible definir mas fases')
                 return redirect(url_for('defFases'))
        if (request.form['opcion']=="Iniciar Proyecto"):
            listadefases=CtrlAdmProy.getFasesListByProy(proyecto)
            if(len(listadefases)==0):
                flash('Debe definirse al menos una fase para iniciar un proyecto')
                return redirect(url_for('defFases'))
            if not(CtrlAdmProy.fasesTotalmenteDefinidas(listadefases)):
                flash('No se puede iniciar el proyecto. Algunas fases aun no poseen tipos de item o roles asociados')
                return redirect(url_for('defFases'))
            CtrlAdmProy.setProyIniciado(proy)
            flash('Proyecto iniciado')
            return redirect(url_for('admProy'))
        if (request.form['opcion']=="Atras"):
            return redirect(url_for('admProy'))
        idfase=int(request.form['select'])
        if (request.form['opcion']=="Asignar Roles"):
            if(CtrlAdmUsr.tienePermisoEnFase(idfase,owner,205)==False):
                flash('No tiene permisos para realizar esta operacion')
                return redirect(url_for('defFases'))
            if(CtrlAdmProy.getFase(idfase).estado !='no-iniciada'):
                flash('No se permite asignar roles a una fase que ha iniciado')
                return redirect(url_for('defFases'))
            listaRoles=CtrlAdmRol.getRolList()
            idRolesEnFase=[]
            rolesEnFase=CtrlAdmProy.getFase(idfase).roles
            for rol in rolesEnFase:
                idRolesEnFase.append(rol.idrol)
            return render_template('asigRolesFase.html',
                                   listRol=listaRoles,
                                   idroles=idRolesEnFase,
                                   idfase=idfase)
        if (request.form['opcion']=="Asignar Tipo de Item"):
            if(CtrlAdmUsr.tienePermisoEnFase(idfase,owner,204)==False):
                flash('No tiene permisos para realizar esta operacion')
                return redirect(url_for('defFases'))
            if(CtrlAdmProy.getFase(idfase).estado !='no-iniciada'):
                flash('No se permite asignar tipos de item a una fase que ha iniciado')
                return redirect(url_for('defFases'))
            listaTipos=CtrlAdmTipoItem.getTipoItemList()
            idTiposEnFase=[]
            tiposEnFase=CtrlAdmProy.getFase(idfase).tipositems
            for tipo in tiposEnFase:
                idTiposEnFase.append(tipo.idtipoitem)
            return render_template('asigTipoItem.html',
                                   listTipoItem=listaTipos,
                                   idtipos=idTiposEnFase,
                                   idfase=idfase)
        if (request.form['opcion']=="Eliminar"):
            fase=CtrlAdmProy.getFase(idfase)
            if(fase.estado=='desarrollo'):
                flash('Imposible eliminar. Fase en desarrollo')
                return redirect(url_for('defFases'))
            CtrlAdmProy.elimFase(idfase)
            flash('Fase eliminada')
            return redirect(url_for('defFases'))
        if (request.form['opcion']=='Modificar'):
            fase=CtrlAdmProy.getFase(idfase)
            if(fase.estado=='desarrollo'):
                flash('Imposible modificar. Fase en desarrollo')
                return redirect(url_for('defFases'))
            return render_template('modFase.html',fase=fase)
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
        listaFases = CtrlAdmProy.getFasesListByProy(project)
        return render_template('defFases.html',listFases=listaFases,proyecto=project) 

@app.route('/admCC', methods=['GET','POST'])
def admCC():
    """Funcion que presenta el menu para administrar los usuarios de un comite de cambio para un proyecto"""  
    if request.method == 'GET':
        global proyecto
        listMiembros = CtrlAdmProy.getMiembrosList(proyecto)
        return render_template('admCC.html', 
                                   listUser=listMiembros)
    if request.method == 'POST':
        if request.form['opcion'] == "Consultar Miembros":
            usr = CtrlAdmUsr.usr(int(request.form['select'])) 
            idroles = CtrlAdmUsr.idRolList(int(usr.idusuario))  
            listRol = CtrlAdmRol.getRolList()     
            return render_template('conMiembro.html',
                                   usr=usr,
                                   idroles=idroles,
                                   listRol=listRol)
        if request.form['opcion'] == "Modificar Comite de Cambios":
            listUser = CtrlAdmUsr.getUsuarioList()
            listidMiembros = CtrlAdmProy.getidMiembrosList(proyecto)
            usuariolider = CtrlAdmProy.getliderProyecto(proyecto)
            return render_template('modCC.html', 
                                   listUser=listUser, 
                                   listidMiembros=listidMiembros,
                                   usuariolider=usuariolider) 
        if request.form['opcion'] == "Administracion de Proyectos":
            return redirect(url_for('admProy')) 
        if request.form['opcion'] == "Home":
            return render_template('main.html')    
        return redirect(url_for('admProy')) 


@app.route('/modCC', methods=['GET','POST'])
def modCC():
    """Funcion que presenta la opcion de asignar/desasignar miembros de un comite de cambio"""
    if request.method == 'POST':
        if request.form['opcion']=="Modificar":
            listSeleccionados = []
            for i in request.form.getlist('idusuarioList'):
                listSeleccionados.append(int(i))
            if (len(listSeleccionados) % 2 == 0):
                CtrlAdmProy.asigComiteCamb(proyecto,
                                 listSeleccionados)
            else:
                listUser = CtrlAdmUsr.getUsuarioList()
                usuariolider = CtrlAdmProy.getliderProyecto(proyecto)
                return render_template('modCC.html', 
                                       listUser=listUser, 
                                       listidMiembros=listSeleccionados,
                                       usuariolider=usuariolider,
                                       error="El numero de miembros debe ser impar")
        return redirect(url_for('admCC'))
        
@app.route('/asigRolesFase', methods=['GET','POST'])
def asigRolesFase():
    """Funcion que presenta la opcion para asignar roles a las fases de un proyecto dado"""
    if request.method == 'POST':
        idfase=int(request.form['idfase'])
        idproyecto=CtrlAdmProy.getFase(idfase).idproyecto
        if request.form['opcion']=="Aceptar":
            idroles=request.form.getlist('roles')
            idroles.append('100')#Para agregar el rol de administrador
            CtrlAdmProy.asignarRolesFase(idroles,idfase)
        listaFases = CtrlAdmProy.getFasesListByProy(idproyecto)
        return render_template('defFases.html',listFases=listaFases,proyecto=idproyecto)    
                
@app.route('/asigTipoItem', methods=['GET','POST'])
def asigTipoItem():
    """Funcion que presenta la opcion para asignar los tipos de items que podran se utilizados en la fase de un proyecto dado"""
    if request.method == 'POST':
        idfase=int(request.form['idfase'])
        idproyecto=CtrlAdmProy.getFase(idfase).idproyecto
        if request.form['opcion']=="Aceptar":
            idtiposdeitem=request.form.getlist('tipos')
            CtrlAdmProy.asignarTiposAFase(idfase,idtiposdeitem)
            if(CtrlAdmProy.faseTieneTipoItem==False):
                flash("Se debe asignar al menos un tipo de item a la fase")
                listaTipos=CtrlAdmTipoItem.getTipoItemList()
                return render_template('asigTipoItem.html',
                                       listTipoItem=listaTipos,
                                       idfase=idfase)
        listaFases = CtrlAdmProy.getFasesListByProy(idproyecto)
        return render_template('defFases.html',listFases=listaFases,proyecto=idproyecto)

@app.route('/modFase', methods=['GET','POST'])    
def modFase():
    """Funcion que presenta el menu para modificar una fase."""  
    if request.method == 'POST':
        if(request.form['opcion'] == "Guardar"):
            CtrlAdmProy.modFase(int(request.form['idfase']), 
                              request.form['nombre'], 
                              request.form['descripcion'])
            flash('Fase modificada')
        return redirect(url_for('defFases'))
"""-------------------------MODULO DE DESARROLLO---------------------------------------"""        
                                                           
"""------------------------Tipos de Items---------------------------------------"""
@app.route('/admTipoItem', methods=['GET','POST'])
def admTipoItem():
    """Funcion que presenta la administracion de los tipos de Items del sistema"""
    if request.method == 'GET':
        listaTiposItem=CtrlAdmTipoItem.getTipoItemList()
        return render_template('admTipoItem.html',listTipoItem=listaTiposItem)
    if request.method == 'POST':
        if request.form['opcion'] == "Buscar":
            listTipo = CtrlAdmTipoItem.busquedaTipo(request.form['buscar'])
            flash('Resultado de la busqueda')
            return render_template('admTipoItem.html',listTipoItem=listTipo)
        if request.form['opcion'] == "Crear":
            #se crea un tipo de item para poder crearle atributos,
            #al cancelar la operacion el item sera eliminado
            #y sus atributos seran eliminados en cascada
            idtipoitem=CtrlAdmTipoItem.crearTipoItem('','')
            return render_template('crearTipoItem.html',idtipoitemtemp=idtipoitem)
        if request.form['opcion'] == "Consultar":
            idtipo=int(request.form['select'])
            listaAtributosTipo=CtrlAdmTipoItem.getAtributosTipo(idtipo)
            nombre=CtrlAdmTipoItem.getNombre(idtipo)
            descripcion=CtrlAdmTipoItem.getDescripcion(idtipo)
            return render_template('conTipoItem.html',idtipoitem=idtipo,
                                   listAtribTipoItem=listaAtributosTipo,
                                   nombre=nombre, descripcion=descripcion)
        if request.form['opcion']=="Redefinir":
            idtipoitem=int(request.form['select'])
            if(CtrlAdmTipoItem.tipoDeItemNoInstanciado(idtipoitem)==False):
                flash('Tipo de Item instanciado, imposible redefinir')
                return redirect(url_for('admTipoItem'))
            listaAtributosTipo=CtrlAdmTipoItem.getAtributosTipo(idtipoitem)
            nombre=CtrlAdmTipoItem.getNombre(idtipoitem)
            descripcion=CtrlAdmTipoItem.getDescripcion(idtipoitem)
            return render_template('modTipoItem.html',idtipoitem=idtipoitem,
                                   listAtribTipoItem=listaAtributosTipo,
                                   nombre=nombre,descripcion=descripcion)
        if request.form['opcion'] == "Home":
            return redirect(url_for('menu'))
        
@app.route('/crearTipoItem', methods=['GET','POST'])
def crearTipoItem():
    """Funcion que permite la creacion de un nuevo tipo de item en el sistema"""
    if request.method == 'GET':
        idtipoitem=request.form['idtipoitemtemp']
        listaAtributosTipo=CtrlAdmTipoItem.getAtributosTipo(idtipoitem)
        nombre=CtrlAdmTipoItem.getNombre(idtipoitem)
        descripcion=CtrlAdmTipoItem.getDescripcion(idtipoitem)
        return render_template('crearTipoItem.html',listAtribTipoItem=listaAtributosTipo,
                               idtipoitemtemp=idtipoitem,nombre=nombre,descripcion=descripcion)
    if request.method == 'POST':
        nombre=request.form['nombre']
        descripcion=request.form['descripcion']
        idtipoitem=int(request.form['idtipoitemtemp'])
        if (request.form['opcion']=="AgregarAtributo"):
            CtrlAdmTipoItem.modTipoItem(idtipoitem,nombre,descripcion)
            return render_template('addAtribTipoItem.html',idtipoitem=idtipoitem,
                                   operacion='crear')
        if(request.form['opcion']=="Crear"):
            CtrlAdmTipoItem.modTipoItem(idtipoitem,nombre,descripcion)
            flash('Tipo de Item Creado')            
            return redirect(url_for('admTipoItem'))
        if(request.form['opcion']=="Cancelar"):
            CtrlAdmTipoItem.borrarTipoItem(idtipoitem)
            return redirect(url_for('admTipoItem'))
        #y si eligio eliminar uno de los atributos...
        CtrlAdmTipoItem.borrarAtributo(int(request.form['opcion']))
        listaAtributosTipo=CtrlAdmTipoItem.getAtributosTipo(idtipoitem)
        return render_template('crearTipoItem.html',idtipoitemtemp=idtipoitem,
                               listAtribTipoItem=listaAtributosTipo,
                               nombre=nombre,descripcion=descripcion)

@app.route('/addAtribTipoItem', methods=['GET','POST'])
def addAtribTipoItem():
    """Funcion que permite dentro de la creacion de un tipo de item ir agregando nuevos atributos para un tipo de item a ser creado"""
    if request.method == 'POST':
        idtipoitem=int(request.form['idtipoitem'])
        operacion=request.form['operacion']
        if request.form['opcion']=="Agregar":
            nombre=request.form['nombre']
            tipo=request.form['datatype']
            bydefault=request.form['bydefault']
            if(CtrlAdmTipoItem.valorPorDefectoValido(tipo,bydefault)==True):
                if(operacion=='crear'):
                    CtrlAdmTipoItem.agregarAtributo(idtipoitem,nombre,tipo,bydefault)
                else:
                    CtrlAdmTipoItem.agregarAtributoSession(idtipoitem,nombre,tipo,bydefault)
            else:
                flash("El valor por defecto no es valido para el tipo de dato")
                return render_template('addAtribTipoItem.html',idtipoitem=idtipoitem)
        listaAtributosTipo=CtrlAdmTipoItem.getAtributosTipo(idtipoitem)
        nombre=CtrlAdmTipoItem.getNombre(idtipoitem)
        descripcion=CtrlAdmTipoItem.getDescripcion(idtipoitem)
        if(operacion=='crear'):
            return render_template('crearTipoItem.html',listAtribTipoItem=listaAtributosTipo,
                                   idtipoitemtemp=idtipoitem,nombre=nombre,descripcion=descripcion)
        else:
            return render_template('modTipoItem.html',listAtribTipoItem=listaAtributosTipo,
                                   idtipoitem=idtipoitem,nombre=nombre,descripcion=descripcion)
            
@app.route('/conTipoItem', methods=['GET','POST'])
def conTipoItem():
    """Funcion que presenta la opcion de consultar un tipo de item ya creado"""
    if request.method == 'POST':
        return redirect(url_for('admTipoItem'))

@app.route('/modTipoItem', methods=['GET','POST'])
def modTipoItem():
    """Funcion que presenta la opcion de modificar un tipo de item ya creado"""
    if request.method == 'GET':
        idtipoitem=request.form['idtipoitem']
        listaAtributosTipo=CtrlAdmTipoItem.getAtributosTipo(idtipoitem)
        nombre=CtrlAdmTipoItem.getNombre(idtipoitem)
        descripcion=CtrlAdmTipoItem.getDescripcion(idtipoitem)
        return render_template('modTipoItem.html',listAtribTipoItem=listaAtributosTipo,
                               idtipoitem=idtipoitem,nombre=nombre,descripcion=descripcion)
    if request.method == 'POST':
        nombre=request.form['nombre']
        descripcion=request.form['descripcion']
        idtipoitem=int(request.form['idtipoitem'])
        if (request.form['opcion']=="AgregarAtributo"):
            CtrlAdmTipoItem.modTipoItemSession(idtipoitem,nombre,descripcion)
            return render_template('addAtribTipoItem.html',idtipoitem=idtipoitem,
                                   operacion='modificar')
        if(request.form['opcion']=="Guardar"):
            CtrlAdmTipoItem.modTipoItemSession(idtipoitem,nombre,descripcion)
            CtrlAdmTipoItem.guardarCambios()
            return redirect(url_for('admTipoItem'))
        if(request.form['opcion']=="Cancelar"):
            CtrlAdmTipoItem.descartarCambios()
            return redirect(url_for('admTipoItem'))
        #y si eligio eliminar uno de los atributos...
        CtrlAdmTipoItem.borrarAtributoSession(int(request.form['opcion']))
        listaAtributosTipo=CtrlAdmTipoItem.getAtributosTipo(idtipoitem)
        return render_template('modTipoItem.html',idtipoitem=idtipoitem,
                               listAtribTipoItem=listaAtributosTipo,
                               nombre=nombre,descripcion=descripcion)

"""---------------------Abrir Proyecto en modo de desarrollo--------------------------------"""
@app.route('/abrirProyecto', methods=['GET','POST'])
def abrirProyecto():
    """Funcion que presenta el menu para abrir proyectos en modo de desarrollo"""  
    if request.method == 'GET':
        global owner
        if CtrlAdmUsr.havePermission(owner,206):
            listaProy = CtrlAdmProy.getProyectoList()
            return render_template('abrirProyecto.html',listProy=listaProy)
        else:
            flash('No tiene permisos para realizar esta operacion ')
            return redirect(url_for('menu')) 
    if request.method == 'POST':
        if request.form['opcion'] == "Abrir":
            global proyecto
            proyecto = int(request.form['select'])
            return redirect(url_for('proyectoX'))
        if request.form['opcion'] == "Buscar":
            listProy = CtrlAdmProy.busquedaProy(request.form['buscar'],
                                         request.form['atributo'])
            
            flash('Resultado de la busqueda')
            return render_template('abrirProyecto.html',listProy=listProy)        
        if request.form['opcion'] == "Home":
            return redirect(url_for('menu'))     
   
"""Funcion que abre un proyecto seleccionado en Modo de Desarrollo y muestra las fases y opciones acerca de items"""
@app.route('/proyectoX', methods=['GET','POST'])
def proyectoX():
    """Funcion que muestra las fases de un proyecto Elegido donde se pueden acceder a las diferentes opciones del modulo de desarrollo como crear consultar items y relacionarlos"""
    if request.method == 'GET':
        global proyecto
        global owner
        listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
        return render_template('proyectoX.html',listFases=listaFases)
    if request.method == 'POST':
        if (request.form['opcion']=="Crear Item"):
            idfase = int(request.form['fase'])
            if(CtrlAdmProy.getFase(idfase).estado!='finalizado'):
                global item
                global versionitem
                item = CtrlFase.instanciarItem("","desarrollo",0,idfase)
                versionitem = CtrlFase.instanciarVersionItem(item.iditem,
                                                            CtrlAdmUsr.getIdByUsername(owner),
                                                            "", 
                                                            0,
                                                            0,
                                                            0,
                                                            1,
                                                            'actual')
                global listaAtributoItemPorTipo
                listaAtributoItemPorTipo = []
                return redirect(url_for('crearItem'))
            else:
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada,
                                       error='Fase finalizada no se pueden agregar items')
        if (request.form['opcion']=="Relacionar"):
            idfase = int(request.form['fase'])
            if(CtrlAdmProy.getFase(idfase).estado!='finalizado'):
                global iditem
                iditem = int(request.form['iditem'])
                i = CtrlFase.getItem(iditem)
                if i.estado == 'bloqueado':
                    faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                    listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                    return render_template('proyectoX.html',
                                           listFases=listaFases,
                                           faseSeleccionada=faseSeleccionada,
                                           error='El item que escogio se encuentra bloqueado y no se pueden relacionar con otros items')                    
                else:
                    return redirect(url_for('relacion'))
            else:
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada,
                                       error='Fase finalizada no se pueden relacionar items')
        if (request.form['opcion']=="Mostrar Items"):
            listItem = CtrlFase.getItemsFase(int(request.form['fase']))
            faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
            listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
            return render_template('proyectoX.html',
                                   listFases=listaFases,
                                   listItem=listItem,
                                   faseSeleccionada=faseSeleccionada)
        if request.form['opcion'] == "Buscar":
            faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
            listItem = CtrlFase.busquedaItem(request.form['buscar'],
                                             request.form['atributo'],
                                             faseSeleccionada.idfase)
            listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
            return render_template('proyectoX.html',
                                   listFases=listaFases,
                                   listItem = listItem,
                                   faseSeleccionada=faseSeleccionada)
        if request.form['opcion'] == "Consultar Item":
            iditem=int(request.form['iditem'])
            item=CtrlFase.getItem(iditem)
            versionitem=CtrlFase.getVersionActual(item.iditem)
            listaValores=item.atributos
            listaAtributos = CtrlAdmTipoItem.getAtributosTipo(item.idtipoitem)            
            return render_template('conItem.html',
                                   item=item,
                                   versionitem=versionitem,
                                   listaValores=listaValores,
                                   listaAtributos=listaAtributos)
        if request.form['opcion'] == "Finalizar Fase":
            if(CtrlFase.finalizarFase(int(request.form['fase']))):
                flash('Fase finalizada')
                return redirect(url_for('proyectoX'))
            else:
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                return render_template('proyectoX.html',
                                       listaFases,
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada,
                                       error='Imposible finalizar la fase. Existe items que no estan en lineas bases cerradas')
        if (request.form['opcion']=="Adjuntar Archivo"):
            idfase = int(request.form['fase'])
            if(CtrlAdmProy.getFase(idfase).estado!='finalizado'):
                iditem = int(request.form['iditem'])
                i = CtrlFase.getItem(iditem)
                if i.estado == 'bloqueado':
                    faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                    listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                    return render_template('proyectoX.html',
                                           listFases=listaFases,
                                           faseSeleccionada=faseSeleccionada,
                                           error='El item que escogio se encuentra bloqueado y no se le puede adjuntar archivos')                    
                else:
                    return redirect(url_for('gestionarArchivos'))
            else:
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada,
                                       error='Fase finalizada no se le puede adjuntar archivos al item')
        if (request.form['opcion']=="Eliminar"):
            idfase = int(request.form['fase'])
            if(CtrlAdmProy.getFase(idfase).estado!='finalizado'):
                iditem = int(request.form['iditem'])
                i = CtrlFase.getItem(iditem)
                if i.estado == 'bloqueado':
                    if not CtrlFase.existeSolicitudPendiente(iditem):
                        versionitem = None
                        global tipo
                        tipo = 'eliminar'
                        return redirect(url_for('enviarSolicitud'))
                    else:
                        faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                        listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                        return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada,
                                       error='Existe una solicitud pendiente sobre este item')
                elif i.estado == 'desarrollo':
                    iditem = int(request.form['iditem'])
                    CtrlFase.eliminarItem(iditem)
                    
                    faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                    listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                    flash('Item eliminado')
                    return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada)
            else:
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada,
                                       error='Fase finalizada no se pueden eliminar items')
        if request.form['opcion'] == "Modificar Item":
            idfase = int(request.form['fase'])
            if(CtrlAdmProy.getFase(idfase).estado!='finalizado'):
                iditem = int(request.form['iditem'])
                if not CtrlFase.existeSolicitudPendiente(iditem):
                    return redirect(url_for('modItem')) 
                else:
                    faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                    listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                    return render_template('proyectoX.html',
                                           listFases=listaFases,
                                           faseSeleccionada=faseSeleccionada,
                                           error='Existe una solicitud pendiente sobre este item')
            else:
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada,
                                       error='Fase finalizada no se pueden modificar items')
        if request.form['opcion'] == "Administrar Historial":
            idfase = int(request.form['fase'])
            if(CtrlAdmProy.getFase(idfase).estado!='finalizado'):
                iditem = int(request.form['iditem'])
                if not CtrlFase.existeSolicitudPendiente(iditem):
                    return redirect(url_for('admHistorial')) 
                else:
                    faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                    listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                    return render_template('proyectoX.html',
                                           listFases=listaFases,
                                           faseSeleccionada=faseSeleccionada,
                                           error='Existe una solicitud pendiente sobre este item')
            else:
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada,
                                       error='Fase finalizada no se puede reversionar items')

        if request.form['opcion'] == "Revivir":
            global idfase
            idfase = int(request.form['fase'])
            if(CtrlAdmProy.getFase(idfase).estado!='finalizado'):
                    return redirect(url_for('revivirItem')) 
            else:
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       faseSeleccionada=faseSeleccionada,
                                       error='Fase finalizada no se pueden revivir items')
            
            
            
        if request.form['opcion'] == "Cerrar Proyecto":
            return redirect(url_for('abrirProyecto')) 


"""-----------------------Revivir Items---------------------------------------"""
@app.route('/revivirItem', methods=['GET','POST'])
def revivirItem():
    """Funcion para revivir los items para una fase dada, dentro de un proyecto elegido""" 
    if request.method == 'GET': 
        global idfase
        listItem = CtrlFase.getItemsFase(idfase)
        for i in listItem:
            flash(i.estado)
        return render_template('revivirItem.html',
                                listItem=listItem)
    if request.method == 'POST':
        if request.form['opcion'] == "Revivir":
            iditem = int(request.form['iditem'])
            CtrlFase.revivirItem(iditem)
            flash('El item fue revivido satisfactoriamente')
        return redirect(url_for('proyectoX'))


"""-----------------------Administrar Historial Items---------------------------------------"""
@app.route('/admHistorial', methods=['GET','POST'])
def admHistorial():
    """Funcion para volver a un a version antigua de un item""" 
    global iditem
    if request.method == 'GET':
        
        listVersion = CtrlFase.getListVersionbyIdItem(iditem)
        return render_template('admHistorial.html',
                                listVersion=listVersion)     
    if request.method == 'POST':
        if request.form['opcion'] == "Reversionar":
            if int(request.form['idversionitem'])==CtrlFase.getVersionActual(iditem).idversionitem:
                flash('No se puede reversionar a la version actual')
                return redirect(url_for('admHistorial'))
            global versionitem
            versionitem = CtrlFase.getVersion(int(request.form['idversionitem']))
            
            i = CtrlFase.getItem(iditem)
            if i.estado == 'bloqueado':
                    global tipo
                    tipo = 'modificar'
                    return redirect(url_for('enviarSolicitud')) 
            elif i.estado == 'desarrollo':
                    global owner
                    iduser = CtrlAdmUsr.getIdByUsername(owner)
                    CtrlFase.reversionar(int(request.form['idversionitem']),iduser)
                    flash('Item reversionado')
                    return redirect(url_for('admHistorial'))
        return redirect(url_for('proyectoX'))

"""-----------------------Modificar Items---------------------------------------"""
@app.route('/modItem', methods=['GET','POST'])
def modItem():
    """Funcion para modificar los items para una fase dada, dentro de un proyecto elegido""" 
    if request.method == 'GET':
        global iditem
        global versionitem
        item = CtrlFase.getItem(iditem)
        versionitem=CtrlFase.getVersionActual(item.iditem)
        listaValores=item.atributos
        listaAtributos = CtrlAdmTipoItem.getAtributosTipo(item.idtipoitem)    
        return render_template('modItem.html',
                                item=item,
                                versionitem=versionitem,
                                listaValores=listaValores,
                                listaAtributos=listaAtributos)     
    if request.method == 'POST':
        if request.form['opcion'] == "Modificar":
            versionitem = CtrlFase.instanciarVersionItem(versionitem.iditem,
                                    versionitem.idusuario,
                                    request.form['descripcion'],
                                    int(request.form['complejidad']),
                                    int(request.form['prioridad']),
                                    int(request.form['costo']),
                                    versionitem.version+1,
                                    'no-actual')
            i = CtrlFase.getItem(iditem)
            if i.estado == 'bloqueado':
                    global tipo
                    tipo = 'modificar'
                    return redirect(url_for('enviarSolicitud')) 
            elif i.estado == 'desarrollo':
                    CtrlFase.modificarItem(iditem,versionitem,CtrlAdmUsr.getIdByUsername(owner))
                    flash('Item modificado')
        return redirect(url_for('proyectoX'))


"""-----------------------Crear Items---------------------------------------"""
@app.route('/crearItem', methods=['GET','POST'])
def crearItem():
    """Funcion para crear los items para una fase dada, dentro de un proyecto elegido""" 
    if request.method == 'GET':
        global item
        global versionitem
        tiposEnFase=CtrlAdmProy.getFase(item.idfase).tipositems
        return render_template('crearItem.html',
                               listTipoItem=tiposEnFase,
                               item=item,
                               versionitem=versionitem)
    if request.method == 'POST':
        if request.form['opcion'] == "Cargar Atributos":
            item.nombre = request.form['nombre']
            item.idtipoitem = int(request.form['tipoItem'])
            versionitem.descripcion = request.form['descripcion']
            versionitem.costo = int(request.form['costo'])
            versionitem.prioridad = int(request.form['prioridad'])
            versionitem.complejidad = int(request.form['complejidad'])
            listaAtributos = CtrlAdmTipoItem.getAtributosTipo(item.idtipoitem)
            global listaAtributoItemPorTipo
            global importar
            if importar == 1:
                return render_template('cargarAtributos.html',listaAtributos=listaAtributos,
                                   listAtribItem=listaAtributoItemPorTipo)
            else:
                return render_template('cargarAtributos.html',listaAtributos=listaAtributos,)
        if request.form['opcion'] == "Crear":
            item.nombre = request.form['nombre']
            versionitem.descripcion = request.form['descripcion']
            versionitem.costo = int(request.form['costo'])
            versionitem.prioridad = int(request.form['prioridad'])
            versionitem.complejidad = int(request.form['complejidad'])
            global importar
            global listaAtributoItemPorTipo
            if ((listaAtributoItemPorTipo!=[])or(importar==1)):
                if(versionitem.costo <= CtrlAdmProy.proy(proyecto).presupuesto):
                    CtrlFase.crearItem(item,versionitem,listaAtributoItemPorTipo)
                    flash("Item Creado")
                    importar=0
                else:
                    tiposEnFase=CtrlAdmProy.getFase(item.idfase).tipositems
                    return render_template('crearItem.html',
                                           listTipoItem=tiposEnFase,
                                           item=item,
                                           versionitem=versionitem,
                                           error="El costo del item sobrepasa el presupuesto de "+
                                           str(CtrlAdmProy.proy(proyecto).presupuesto))
            else:
                tiposEnFase=CtrlAdmProy.getFase(item.idfase).tipositems
                return render_template('crearItem.html',
                               listTipoItem=tiposEnFase,
                               item=item,
                               versionitem=versionitem,
                               error="Debe Cargar Valores a los Atributos de Tipo de Item")
        if request.form['opcion']=="Importar":
            importar=1
            return redirect(url_for('importarItem'))
        return redirect(url_for('proyectoX'))

"""----------------------Importar Item-------------------"""        
@app.route('/importarItem', methods=['GET','POST'])
def importarItem():
    """Funcion que permite al usuario elegir un item de otro proyecto para importarlo"""
    global item
    global versionitem
    if request.method == 'GET':
        global proyecto
        proyactual = CtrlAdmProy.proy(proyecto)
        idproyactual=proyactual.idproyecto
        proyectos=CtrlAdmProy.getProyectoList()
        return render_template('importarItem.html',
                               idproyactual=idproyactual,
                               listProyectos=proyectos)
    if request.method == 'POST':
        if request.form['opcion']=='Mostrar Items':
            proyectosel=CtrlAdmProy.proy(int(request.form['proyecto']))
            lista=[]
            for fase in proyectosel.fases:
                for curitem in fase.items:
                    lista.append(curitem)
            proyactual = CtrlAdmProy.proy(proyecto)
            idproyactual=proyactual.idproyecto
            proyectos=CtrlAdmProy.getProyectoList()
            return render_template('importarItem.html',
                                   idproyactual=idproyactual,
                                   listProyectos=proyectos,
                                   listItem=lista)
        if request.form['opcion']=='Aceptar':
            itemsel=CtrlFase.getItem(int(request.form['iditem']))
            item = CtrlFase.copiarDatosItem(itemsel,item,versionitem)
            versionorigen = CtrlFase.getVersionActual(itemsel.iditem)
            versionitem = CtrlFase.copiarDatosVersion(versionorigen,versionitem)
            versionitem.iditem=item.iditem
            global listaAtributoItemPorTipo
            listaAtributoItemPorTipo=item.atributos
        if request.form['opcion']=='Cancelar':
            importar=0
        flash('Item importado para crearse')
        return redirect(url_for('crearItem'))
    
"""----------------------Agregar Atributos de Tipo de Item por Item-------------------"""        
@app.route('/cargarAtributos', methods=['GET','POST'])
def cargarAtributos():
    "Funcion que carga los valores de los atributos segun el tipo de item elegido para cierto item a ser creado"
    if request.method == 'POST':
        if request.form['opcion'] == "Aceptar": 
            global item
            global listaAtributoItemPorTipo
            global importar
            listaAtributos = CtrlAdmTipoItem.getAtributosTipo(item.idtipoitem)
            for atributo in listaAtributos:
                if importar==0:
                    nuevo = CtrlFase.instanciarAtributoItemPorTipo(item.iditem,
                                                                   atributo.idatributo,
                                                                   request.form[atributo.nombre])
                    listaAtributoItemPorTipo.append(nuevo)
                else:
                    atributo.valor=request.form[atributo.nombre]
        return redirect(url_for('crearItem'))
        
"""-----------------------Relacion entre Items---------------------------------------"""
@app.route('/relacion', methods=['GET','POST'])
def relacion():
    """Funcion para relacionar los items"""  
    if request.method == 'GET':
        return render_template('relacion.html')
    if request.method == 'POST':
        if request.form['opcion'] == "Mostrar Item":
            if request.form['tipo']== "padre-hijo":
                global iditem
                item = CtrlFase.getItem(iditem)
                listItem = CtrlFase.getItemsFase(item.idfase)
                relacionadoList = CtrlFase.getListPadreHijo(iditem)
                return render_template('relacion.html',
                                       bool = True,
                                       listItem=listItem,
                                       iditem=iditem,
                                       relacionadoList = relacionadoList)
            if request.form['tipo']== "sucesor-antecesor":
                item = CtrlFase.getItem(iditem)
                listItem = CtrlFase.getItemsFaseAnterior(item.idfase)
                relacionadoList = CtrlFase.getListAntecesorSucesor(iditem)
                return render_template('relacion.html',
                                       bool = False,
                                       listItem=listItem,
                                       iditem=iditem,
                                       relacionadoList = relacionadoList)
        if request.form['opcion'] == "Guardar":
            if request.form['tipo']== "padre-hijo":
                for idItemB in request.form.getlist('iditemList'):
                    if CtrlFase.ciclo(int(idItemB),iditem):
                        item = CtrlFase.getItem(iditem)
                        listItem = CtrlFase.getItemsFase(item.idfase)
                        itemB = CtrlFase.getItem(idItemB)
                        relacionadoList = [int(r) for r in request.form.getlist('iditemList')]
                        return render_template('relacion.html',
                                               bool = True,
                                               listItem=listItem,
                                               iditem=iditem,
                                               relacionadoList = relacionadoList,
                                               error='Imposible crear relacion Padre-Hijo entre '+
                                               itemB.nombre+
                                               " - "+
                                               item.nombre)
            CtrlFase.relacionar(iditem,
                                request.form.getlist('iditemList'),
                                request.form['tipo'])
            flash("Se han guardado los cambios exitosamente")
        if request.form['opcion'] == "Home":
            return render_template('main.html')
    return redirect(url_for('proyectoX'))

"""-----------------------Gestionar Archivos---------------------------------------"""
@app.route('/gestionarArchivos', methods=['GET','POST'])
def gestionarArchivos():
    """Funcion para gestionar archivos"""  
    if request.method == 'GET':
        listArchivo = CtrlFase.getArchivoList()
        global iditem
        idarchivos = CtrlFase.getIdArchivosByItem(iditem)
        return render_template('gestionarArchivos.html',
                               listArchivo=listArchivo,
                               idarchivos=idarchivos)
    if request.method == 'POST':
        if (request.form['opcion']=="Subir"):
            archivo = request.files['file']
            CtrlFase.subir(archivo)
            flash("Archivo Subido")
            return redirect(url_for('gestionarArchivos'))
        if (request.form['opcion']=="Adjuntar"):
            idarchivos = request.form.getlist('idarchivos')
            CtrlFase.adjuntar(iditem,idarchivos)
            flash("Archivos adjuntados")
            return redirect(url_for('proyectoX'))
        if (request.form['opcion']=="Cancelar"):
            return redirect(url_for('proyectoX'))
        if (request.form['opcion']=="Buscar"):
            listArchivo = CtrlFase.busquedaArchivo(request.form['buscar'],
                                                request.form['atributo'])
            idarchivos = CtrlFase.getIdArchivosByItem(iditem)
            flash('Resultado de la busqueda')
            return render_template('gestionarArchivos.html',
                                   listArchivo=listArchivo,
                                   idarchivos=idarchivos)
        return send_file("archivo",
                     attachment_filename=CtrlFase.descargar(int(request.form['opcion'])).nombre,
                     as_attachment=True)
        os.remove('archivo')
        return redirect(url_for('gestionarArchivos'))
        
"""-----------------------Enviar Solicitud de Cambio---------------------------------------"""
@app.route('/enviarSolicitud', methods=['GET','POST'])
def enviarSolicitud():
    """Funcion para enviar solicitud de cambio""" 
    global iditem 
    if request.method == 'GET':
        item=CtrlFase.getItem(iditem)
        global versionitem
        global tipo
        if tipo=='eliminar':
            versionitem=CtrlFase.getVersionActual(item.iditem)
        listaValores=item.atributos
        listaAtributos = CtrlAdmTipoItem.getAtributosTipo(item.idtipoitem)            
        return render_template('enviarSolicitud.html',
                                   tipo=tipo,
                                   item=item,
                                   versionitem=versionitem,
                                   listaValores=listaValores,
                                   listaAtributos=listaAtributos)
    if request.method == 'POST':
        item=CtrlFase.getItem(iditem)
        if (request.form['opcion']=="Enviar"):
            costoeimpacto=[]
            costoeimpacto=CtrlFase.recorridoEnProfundidad(item)
            CtrlFase.enviarSolicitud(CtrlAdmUsr.getIdByUsername(owner),
                                     tipo,
                                     iditem,
                                     versionitem,
                                     str(costoeimpacto[0]),
                                     str(costoeimpacto[1]))
            flash('Solicitud enviada')
            return redirect(url_for('proyectoX'))
        if (request.form['opcion']=="Cancelar"):
            return redirect(url_for('proyectoX'))


"""-------------------------MODULO DE GESTION DE CAMBIOS--------------------------------------"""

"""---------------------Abrir Proyecto en modo de desarrollo--------------------------------"""
@app.route('/abrirProyectoEnGC', methods=['GET','POST'])
def abrirProyectoEnGC():
    """Funcion que presenta el menu para abrir proyectos en modo de desarrollo"""  
    if request.method == 'GET':
        global owner
        if CtrlAdmUsr.havePermission(owner,207):
            #agregar permiso para Linea Base!!!!!!!!!!!!!!!!!!!!!!
            listaProy = CtrlAdmProy.getProyectoList()
            return render_template('abrirProyectoEnGC.html',listProy=listaProy)
        else:
            flash('No tiene permisos para realizar esta operacion ')
            return redirect(url_for('menu')) 
    if request.method == 'POST':
        if request.form['opcion'] == "Abrir":
            global proyecto
            proyecto = int(request.form['select'])
            return redirect(url_for('proyectoXenGC'))
        if request.form['opcion'] == "Buscar":
            listProy = CtrlAdmProy.busquedaProy(request.form['buscar'],
                                         request.form['atributo'])
            
            flash('Resultado de la busqueda')
            return render_template('abrirProyectoEnGC.html',listProy=listProy)        
        if request.form['opcion'] == "Home":
            return redirect(url_for('menu'))   

@app.route('/proyectoXenGC', methods=['GET','POST'])
def proyectoXenGC():
    """Funcion que abre un proyecto seleccionado en Modo de Gestion de Cambios y muestra las lineas bases de una fase seleccionada"""    
    if request.method == 'GET':
        global proyecto
        global owner
        listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
        return render_template('proyectoXenGC.html',listFases=listaFases)
    if request.method == 'POST':
        if request.form['opcion'] == "Mostrar Lineas Bases":
            listLB = CtrlLineaBase.getLBFase(int(request.form['fase']))
            faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
            listaFases = CtrlAdmProy.getFasesListByProy(proyecto)
            return render_template('proyectoXenGC.html',
                                   listFases=listaFases,
                                   listLB=listLB,
                                   faseSeleccionada=faseSeleccionada)     
            return render_template('proyectoXenGC.html')         
        if request.form['opcion'] == "Nueva Linea Base":
            global idfase
            idfase = int(request.form['fase'])
            if(CtrlAdmProy.getFase(idfase).estado != 'finalizado'):
                CtrlLineaBase.crearLB(idfase)
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listLB = CtrlLineaBase.getLBFase(int(request.form['fase']))
                flash('Linea Base Creada')
                return render_template('proyectoXenGC.html',
                                        listLB=listLB,
                                        faseSeleccionada=faseSeleccionada,
                                        listFases=listaFases)
            else:
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listLB = CtrlLineaBase.getLBFase(int(request.form['fase']))
                return render_template('proyectoXenGC.html',
                                        listLB=listLB,
                                        faseSeleccionada=faseSeleccionada,
                                        listFases=listaFases,
                                        error='Fase finalizada imposible crear linea base')        
        if request.form['opcion'] == "Eliminar Linea Base":
            idfase = int(request.form['fase'])
            global idlineabase
            idlineabase = int(request.form['idlineabase'])
            if((CtrlLineaBase.getLB(idlineabase)).estado=='cerrado'):
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listLB = CtrlLineaBase.getLBFase(int(request.form['fase']))
                return render_template('proyectoXenGC.html',
                                       listLB=listLB,
                                       faseSeleccionada=faseSeleccionada,
                                       listFases=listaFases,
                                       error='Linea Base cerrada imposible eliminar Linea Base')
            else:
                CtrlLineaBase.eliminarLB(idlineabase)
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listLB = CtrlLineaBase.getLBFase(int(request.form['fase']))
                flash('Linea Base Eliminada')
                return render_template('proyectoXenGC.html',
                                       listLB=listLB,
                                       faseSeleccionada=faseSeleccionada,
                                       listFases=listaFases)
                                         
        if request.form['opcion'] == "Add/Quitar Items":
            idfase = int(request.form['fase'])
            idlineabase = int(request.form['idlineabase'])
            if((CtrlLineaBase.getLB(idlineabase)).estado=='cerrado'):
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listLB = CtrlLineaBase.getLBFase(int(request.form['fase']))
                return render_template('proyectoXenGC.html',
                                       listLB=listLB,
                                       faseSeleccionada=faseSeleccionada,
                                       listFases=listaFases,
                                       error='Linea Base cerrada imposible agregar items')
            else:
                return redirect(url_for('asigItemsEnLB'))
        if request.form['opcion'] == "Consultar":
            idlineabase = int(request.form['idlineabase'])
            listItem = CtrlLineaBase.getListItemsEnLB(idlineabase) #lista de los items que estan en la linea base             
            return render_template('conLB.html',listItem=listItem) 
        if request.form['opcion'] == "Cerrar Linea Base":
            idlineabase = int(request.form['idlineabase'])
            if(CtrlLineaBase.cerrarLB(idlineabase)):
                flash('Linea Base Cerrada')
                return redirect(url_for('proyectoXenGC'))
            else:                
                listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
                faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
                listLB = CtrlLineaBase.getLBFase(int(request.form['fase']))
                return render_template('proyectoXenGC.html',
                                       listLB=listLB,
                                       faseSeleccionada=faseSeleccionada,
                                       listFases=listaFases,
                                       error='Imposible cerrar Linea Base, hay Items sin relaciones')
        if request.form['opcion'] == "Buscar":
            faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
            listLB = CtrlLineaBase.busquedaLineaBase(request.form['buscar'],
                                             request.form['atributo'],
                                             faseSeleccionada.idfase)
            listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)
            return render_template('proyectoXenGC.html',
                                   listFases=listaFases,
                                   listLB = listLB,
                                   faseSeleccionada=faseSeleccionada)
        if request.form['opcion'] == "Cerrar Proyecto":
            return redirect(url_for('abrirProyectoEnGC')) 

@app.route('/asigItemsEnLB', methods=['GET','POST'])
def asigItemsEnLB():                                    
    """Funcion que asigna y desasigna items a una linea base abierta en una fase seleccionada"""
    if request.method == 'GET':
        listItem = CtrlLineaBase.getItemsFaseNotLB(idfase) #lista de todos los items de la fase
        listItemEnLB = CtrlLineaBase.getListItemsEnLB(idlineabase) #lista de los items que estan en la linea base 
        return render_template('asigItemsEnLB.html',
                                listItem =listItem,
                                listItemEnLB = listItemEnLB)
    if request.method == 'POST':
        if request.form['opcion'] == "Guardar":
            listItemEnLB = request.form.getlist('iditem')
            CtrlLineaBase.agregarItems(listItemEnLB,idlineabase)        
    return redirect(url_for('proyectoXenGC'))

@app.route('/bandejaEntrada', methods=['GET','POST'])
def bandejaEntrada():                                    
    """Funcion que muestra todas las solicitudes de cambio del usuario"""
    if request.method == 'GET':
        idusuario = CtrlAdmUsr.getIdByUsername(owner)
        listsolicitudes = CtrlSolicitudCambio.getSolicitudesbyCC(idusuario)
        return render_template('bandejaDeEntrada.html',
                                listsolicitudes =listsolicitudes)
    if request.method == 'POST':
        if request.form['opcion'] == "Ver":
            idsolicituddecambio = int(request.form['idsolicituddecambio'])
            solicituddecambio = CtrlSolicitudCambio.getSolicitudDeCambio(idsolicituddecambio)
            return render_template('solicitudCambio.html',
                                solicituddecambio =solicituddecambio)            
        if request.form['opcion'] == "Home":
            return redirect(url_for('menu'))   
        
@app.route('/bandejaEntrada', methods=['GET','POST'])
def bandejaEntrada():                                    
    """Funcion que muestra todas las solicitudes de cambio del usuario"""
    if request.method == 'GET':
        idusuario = CtrlAdmUsr.getIdByUsername(owner)
        listsolicitudes = CtrlSolicitudCambio.getSolicitudesbyCC(idusuario)
        listVotos = CtrlSolicitudCambio.getVotobyCC(idusuario)
        return render_template('bandejaDeEntrada.html',
                                listsolicitudes =listsolicitudes,
                                listVotos=listVotos)
    if request.method == 'POST':
        if request.form['opcion'] == "Ver":
            global idsolicituddecambio
            idsolicituddecambio = int(request.form['idsolicituddecambio'])
            return redirect(url_for('votarSolicitud')) 
        if request.form['opcion'] == "Home":
            return redirect(url_for('menu'))  

@app.route('/votarSolicitud', methods=['GET','POST'])
def votarSolicitud():                                    
    """Funcion que muestra todas las solicitudes de cambio del usuario"""
    if request.method == 'GET':
        global idsolicituddecambio
        solicituddecambio = CtrlSolicitudCambio.getSolicitudDeCambio(idsolicituddecambio)
        voto = CtrlSolicitudCambio.getestadoVoto(idsolicituddecambio,CtrlAdmUsr.getIdByUsername(owner))
        return render_template('solicitudCambio.html',
                               voto=voto,
                               solicituddecambio = solicituddecambio)
                
    if request.method == 'POST':
        if request.form['opcion'] == "Aceptar Solicitud":
            CtrlSolicitudCambio.votarSolicitud(idsolicituddecambio,CtrlAdmUsr.getIdByUsername(owner),'Aceptado')
            CtrlSolicitudCambio.contarVotos(idsolicituddecambio)
            flash('Su voto a sido registrado')
        if request.form['opcion'] == "Rechazar Solicitud":
            CtrlSolicitudCambio.votarSolicitud(idsolicituddecambio,CtrlAdmUsr.getIdByUsername(owner),'Rechazado')
            CtrlSolicitudCambio.contarVotos(idsolicituddecambio)
            flash('Su voto a sido registrado')
        return redirect(url_for('bandejaEntrada'))  
        
if __name__=='__main__':
    app.run()             