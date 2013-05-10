from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash, _app_ctx_stack
import CtrlAdmUsr
import CtrlAdmRol
import CtrlAdmProy
import CtrlAdmTipoItem
import CtrlFase
import CtrlLineaBase

"""Modulo de ejecucion principal de SGP"""  
__author__ = 'Grupo 5'
__date__ = '04/05/13'
__version__ = '3.0'
__credits__ = 'none'
__text__ = 'indice principal que conmuta con las diferentes funcionalidades de SGP'
__file__ = 'index.py' 

app = Flask(__name__,template_folder='/home/divina/git/SGP/templates')
app.debug = True
app.secret_key = 'secreto'
app.config.from_object(__name__)
app.config.from_envvar('SGP_SETTINGS', silent=True)

owner=""
proyecto=0
item=None
versionitem=None
listaAtributoItemPorTipo=[]

iditem=0

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
        if request.form['opcion'] == "Crear":
            return render_template('crearProy.html')
        if request.form['opcion'] == "Administrar Fases":
            global proyecto
            proyecto = int(request.form['select'])
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
            proy = CtrlAdmProy.proy(int(request.form['select']))        
            return render_template('modProy.html', proyecto=proy) 
        if request.form['opcion'] == "Home":
            return render_template('main.html')
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
        if (request.form['opcion']=="Definir"):
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
            return redirect(url_for('defFases'))
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
        if (request.form['opcion']=='Atras'):
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
            global item
            global versionitem
            item = CtrlFase.instanciarItem("","desarrollo",0,idfase)
            versionitem = CtrlFase.instanciarVersionItem(item.iditem,
                                                            CtrlAdmUsr.getIdByUsername(owner),
                                                            "", 
                                                            0,
                                                            0,
                                                            0,
                                                            1)
            global listaAtributoItemPorTipo
            listaAtributoItemPorTipo = []
            return redirect(url_for('crearItem'))
        if (request.form['opcion']=="Relacionar"):
            global iditem
            iditem = int(request.form['iditem'])
            return redirect(url_for('relacion'))
        if (request.form['opcion']=="Mostrar Items"):
            listItem = CtrlFase.getItemsFase(int(request.form['fase']))
            faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
            listaFases = CtrlAdmProy.getFasesListByProy(proyecto)
            return render_template('proyectoX.html',
                                   listFases=listaFases,
                                   listItem=listItem,
                                   faseSeleccionada=faseSeleccionada)
        if request.form['opcion'] == "Buscar":
            faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
            listItem = CtrlFase.busquedaItem(request.form['buscar'],
                                             request.form['atributo'],
                                             faseSeleccionada.idfase)
            return render_template('proyectoX.html',
                                   listItem = listItem,
                                   faseSeleccionada=faseSeleccionada)
        if request.form['opcion'] == "Consultar Item":
            if request.form['iditem']=="":
                listaFases = CtrlAdmProy.getFasesListByProy(proyecto)
                return render_template('proyectoX.html',
                                       listFases=listaFases,
                                       error='Debe escoger un item')
            #print request.form['iditem']
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
        if request.form['opcion'] == "Cerrar Proyecto":
            return redirect(url_for('abrirProyecto')) 

"""-----------------------Crear Items---------------------------------------"""
@app.route('/crearItem', methods=['GET','POST'])
def crearItem():
    """Funcion para crear los items para una fase dada, dentro de un proyecto elejido""" 
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
            return render_template('cargarAtributos.html',listaAtributos=listaAtributos)
        if request.form['opcion'] == "Crear":
            item.nombre = request.form['nombre']
            versionitem.descripcion = request.form['descripcion']
            versionitem.costo = int(request.form['costo'])
            versionitem.prioridad = int(request.form['prioridad'])
            versionitem.complejidad = int(request.form['complejidad'])
            global listaAtributoItemPorTipo
            if listaAtributoItemPorTipo:
                if(versionitem.costo <= CtrlAdmProy.proy(proyecto).presupuesto):
                    CtrlFase.crearItem(item,versionitem,listaAtributoItemPorTipo)
                    flash("Item Creado")
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
        return redirect(url_for('proyectoX'))
        
"""----------------------Agregar Atributos de Tipo de Item por Item-------------------"""        
@app.route('/cargarAtributos', methods=['GET','POST'])
def cargarAtributos():
    "Funcion que carga los valores de los atributos segun el tipo de item elegido para cierto item a ser creado"
    if request.method == 'POST':
        if request.form['opcion'] == "Aceptar": 
            global item
            global listaAtributoItemPorTipo
            listaAtributoItemPorTipo = []
            listaAtributos = CtrlAdmTipoItem.getAtributosTipo(item.idtipoitem)
            for atributo in listaAtributos:
                nuevo = CtrlFase.instanciarAtributoItemPorTipo(item.iditem,
                                                               atributo.idatributo,
                                                               request.form[atributo.nombre])
                listaAtributoItemPorTipo.append(nuevo)
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

"""-------------------------MODULO DE GESTION DE CAMBIOS--------------------------------------"""

"""---------------------Abrir Proyecto en modo de desarrollo--------------------------------"""
@app.route('/abrirProyectoEnGC', methods=['GET','POST'])
def abrirProyectoEnGC():
    """Funcion que presenta el menu para abrir proyectos en modo de desarrollo"""  
    if request.method == 'GET':
        global owner
        if CtrlAdmUsr.havePermission(owner,206):
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
            idfase = int(request.form['fase'])
            CtrlLineaBase.crearLB(idfase)
            faseSeleccionada = CtrlAdmProy.getFase(int(request.form['fase']))
            listaFases = CtrlAdmProy.getFasesListByProyAndUser(proyecto,owner)   
            return render_template('proyectoXenGC.html',listFases=listaFases)         
        if request.form['opcion'] == "Add/Quitar Items":
            global idfase
            idfase = int(request.form['fase'])
            global idlineabase
            idlineabase = int(request.form['idlineabase'])
            return redirect(url_for('asigItemsEnLB'))
        if request.form['opcion'] == "Buscar":
            return render_template('proyectoXenGC.html')
        if request.form['opcion'] == "Consultar":            
            return render_template('conLB.html')       
        if request.form['opcion'] == "Cerrar Proyecto":
            return redirect(url_for('abrirProyectoEnGC')) 

@app.route('/asigItemsEnLB', methods=['GET','POST'])
def asigItemsEnLB():                                    
    """Funcion que asigna y desasigna items a una linea base abierta en una fase seleccionada"""
    if request.method == 'GET':
        listItem = CtrlFase.getItemsFase(idfase) #lista de todos los items de la fase
        listItemEnLB = CtrlLineaBase.getListItemsEnLB(idlineabase) #lista de los items que estan en la linea base 
        return render_template('asigItemsEnLB.html',
                                bool = True,
                                listItem =listItem,
                                listItemEnLB = listItemEnLB,
                                idlineabase=idlineabase)
    if request.method == 'POST':
        if request.form['opcion'] == "Guardar":
            listItemEnLB=request.form.getlist('iditem')
            CtrlLineaBase.agregarItems(listItemEnLB,idlineabase)
        return render_template('proyectoXenGC.html')         
        if request.form['opcion'] == "Cancelar":
            return redirect(url_for('proyectoXenGC.html'))       

if __name__=='__main__':
    app.run()             