from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
import CtrlAdmUsr
import CtrlAdmRol
import CtrlAdmProy
import CtrlAdmTipoItem

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
proyecto=0
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
@app.route('/confCnt', methods=['GET','POST'])
def confCnt():
    if request.method == 'GET':
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
        if request.form['opcion'] == "Administrar Fases":
            global fasesCreadas
            fasesCreadas=0
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
        if (request.form['opcion']=="Asignar Roles"):
               return render_template('asigRolesFase.html')
        if (request.form['opcion']=="Asignar Tipo de Item"):
               return render_template('asigTipoItem.html')    
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

@app.route('/admCC', methods=['GET','POST'])
def admCC():
    """Funcion que presenta el menu para administrar usuarios."""  
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
    if request.method == 'POST':
        project=int(request.form['idproyecto'])
        if request.form['opcion']=="Aceptar":
            return render_template('defFases.html')
        
@app.route('/asigTipoItem', methods=['GET','POST'])
def asigTipoItem():
    if request.method == 'POST':
        project=int(request.form['idproyecto'])
        if request.form['opcion']=="Aceptar":
            return render_template('defFases.html')
        
"""-------------------------MODULO DE DESARROLLO---------------------------------------"""        
                                                           
"""------------------------Tipos de Items---------------------------------------"""
@app.route('/admTipoItem', methods=['GET','POST'])
def admTipoItem():
    """Funcion que presenta la administracion de los tipos de Items del sistema"""
    if request.method == 'GET':
        listaTiposItem=CtrlAdmTipoItem.getTipoItemList()
        return render_template('admTipoItem.html',listTipoItem=listaTiposItem)
    if request.method == 'POST':
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
    if request.method == 'POST':
        return redirect(url_for('admTipoItem'))

@app.route('/modTipoItem', methods=['GET','POST'])
def modTipoItem():
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



"""-----------------------Crear Items---------------------------------------"""
@app.route('/crearItem', methods=['GET','POST'])
def crearItem():
    """Funcion para crear los items"""  
    if request.method == 'GET':
        return render_template('crearItem.html')
    if request.method == 'POST':
        if request.form['opcion'] == "Home":
            return render_template('main.html')

"""-----------------------Relacion entre Items---------------------------------------"""
@app.route('/relacion', methods=['GET','POST'])
def relacion():
    """Funcion para relacionar los items"""  
    if request.method == 'GET':
        return render_template('relacion.html')
    if request.method == 'POST':
        if request.form['opcion'] == "Home":
            return render_template('main.html')
                                
"""---------------------Abrir Proyecto-----------------------------------"""
@app.route('/abrirProyecto', methods=['GET','POST'])
def abrirProyecto():
    """Funcion para seleccionar el proyecto a ser utilizado en el modo de desarrollo"""  
    if request.method == 'GET':
        if CtrlAdmUsr.havePermission(owner,202):
            listaProy = CtrlAdmProy.getProyectoList()
            return render_template('abrirProyecto.html',listProy=listaProy)
        else:
            flash('No tiene permisos para realizar esta operacion ')
            return redirect(url_for('menu')) 
    if request.method == 'POST':
        if request.form['opcion'] == "Abrir":
            return render_template('main.html')
        if request.form['opcion'] == "Home":
            return render_template('main.html')
        return redirect(url_for('abrirProyecto'))     
if __name__=='__main__':
    app.run()