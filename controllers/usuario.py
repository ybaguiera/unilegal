__author__ = 'Yoel'


# # otorgar permisos
# id_grupo = db.auth_group(db.auth_group.role == "Administrador").id
# auth.add_permission(id_grupo, 'read', db.auth_user)
# auth.add_permission(id_grupo, 'create', db.auth_user)
# auth.add_permission(id_grupo, 'select', db.auth_user)
# auth.add_permission(id_grupo, 'delete', db.auth_user)
# auth.add_permission(id_grupo, 'update', db.auth_user)


def login():
    form = auth.login()        
    return locals()

# @auth.requires_membership('Administrador')
def crear_usuario():
    # form = crud.create(db.auth_user, db.auth_membership)
    if auth.has_membership('Administrador'):
        formulario = SQLFORM.factory(db.auth_user,
                                    Field("grupo_seleccion", "reference auth_group", label=T("Rol del usuario"),
                                        requires=IS_IN_DB(db, 'auth_group.role', zero=T('Elige un rol'),
                                                            error_message=T("Valor incorrecto"))))
        
        if formulario.process().accepted:
            consulta = db.auth_user(db.auth_user.ci==formulario.vars.ci)
            if consulta:
                session.usuario_ci = 'Ya existe un usuario registrado con ese carnet de identidad.' 
                # response.flash = 'Ya existe un usuario con ese carnet'
                redirect(URL('usuario', 'crear_usuario'))
            else:
                response.flash = 'formulario aceptado'
                id_usuario = db.auth_user.insert(**db.auth_user._filter_fields(formulario.vars))
                grupo = formulario.vars.grupo_seleccion
                id_grupo = db.auth_group(db.auth_group.role == str(grupo)).id
                dict_membresia = {"user_id": id_usuario, "group_id": id_grupo}
                id_membresia = db.auth_membership.insert(**dict_membresia)
                redirect(URL('usuario', 'crear_usuario',  args="creado"))
        elif formulario.errors:
            response.flash = 'El formulario tiene errores'
    else:        
        formulario = SQLFORM.factory(db.auth_user)
              
        if formulario.process().accepted:
            consulta = db.auth_user(db.auth_user.ci==formulario.vars.ci)
            if consulta:
                session.usuario_ci = 'Ya existe un usuario registrado con ese carnet de identidad. Si usted no ha realizado ningún registro por favor pónganse en contacto con el administrador del sitio.' 
                # response.flash = 'Ya existe un usuario con ese carnet'
                redirect(URL('usuario', 'crear_usuario'))
            else:                    
                response.flash = 'formulario aceptado'
                id_usuario = db.auth_user.insert(**db.auth_user._filter_fields(formulario.vars))
                # grupo = formulario.vars.grupo_seleccion
                id_grupo = db.auth_group(db.auth_group.role == "Invitado")
                dict_membresia = {"user_id": id_usuario, "group_id": id_grupo}
                id_membresia = db.auth_membership.insert(**dict_membresia)
                redirect(URL('default', 'index',  args="creado"))
        elif formulario.errors:
            response.flash = 'El formulario tiene errores'
    return locals()


@auth.requires_membership('Administrador')
def administrar_usuario():
    contar=db(db.auth_user.id>1).count()
    return locals()


@auth.requires_membership('Administrador')
def cambiar_rol():
    db.auth_membership.id.readable=False
    lista = [db.auth_membership.user_id, db.auth_membership.group_id]
    dictHeaders = {'auth_membership.user_id': 'Nombre de usuario', 'auth_membership.group_id': 'Rol del usuario'}
    dictLinks = [dict(header='Editar', body=lambda row: A('Editar', _href=URL('usuario', 'editar_rol', args=[row.id],
                                                                              user_signature=True),
                                                          _class='btn btn-primary'))]
    grid = SQLFORM.grid(db.auth_membership.user_id != db.auth_user(db.auth_user.email == "admin@unica.cu").id, create=False,
                        deletable=False, details=False, editable=False, csv=False, fields=lista, headers=dictHeaders,
                        links=dictLinks, searchable=False, maxtextlength = 400)
    return locals()


@auth.requires_membership('Administrador')
def editar_rol():
    rol = db.auth_membership(request.args(0, cast=int)) or redirect(URL('default', 'index'))
    # fields = ['grupo_seleccion']
    # labels = {'grupo_seleccion': 'Rol del usuario'}
    formulario = SQLFORM.factory(Field("grupo_seleccion", "reference auth_group", label=T("Rol del usuario"),
                                       requires=IS_IN_DB(db, 'auth_group.role', zero=T('Elige un rol'),
                                                         error_message=T("Valor incorrecto"))))

    if formulario.process().accepted:
        grupo = formulario.vars.grupo_seleccion
        id_grupo = db.auth_group(db.auth_group.role == str(grupo)).id
        dict_membresia = {"group_id": id_grupo}
        db.auth_membership[rol.id] = dict_membresia
        redirect(URL('usuario', 'cambiar_rol'))
        
        # redirect(URL('mostrar_user', args=[rol.id], user_signature=True))
    return locals()


@auth.requires_membership('Administrador')
def mostrar_user():
    rol = db.auth_membership(request.args(0, cast=int)) or redirect(URL('default', 'index'))
    user_name = db.auth_user(db.auth_user.id == rol.user_id).username
    rol = db.auth_group(db.auth_group.id == rol.group_id).role
    return locals()


@auth.requires_membership('Administrador')
def asignar_responsable():
    formulario = SQLFORM.factory(
        Field("id_usuario", "reference auth_user", default=None, label="Usuario",
              requires=IS_IN_DB(db, 'auth_user.id', "%(username)s", zero=T('Elige un usuario'),
                                error_message=T("Valor incorrecto"))),
        Field("nombre_responsable", "reference responsable", default=None, label="Responsable",
              requires=IS_IN_DB(db, 'responsable.nombre', zero=T('Elige un responsable'),
                                error_message=T("Valor incorrecto"))),
    )

    # request_vars = request.post_vars.id_usuario
    if formulario.validate():
        id_usuario = formulario.vars.id_usuario
        nombre_responsable = formulario.vars.nombre_responsable

        row = db((db.usuario_responsable.id_usuario == id_usuario) & (
                db.usuario_responsable.nombre_responsable == nombre_responsable)).select()

        if row:
            response.flash = T("El usuario ya tiene asignado este responsable.")
        else:
            db.usuario_responsable.insert(id_usuario=id_usuario, nombre_responsable=nombre_responsable)
            response.flash = T("El responsable se ha asignado correctamente.")

    # lolo = request.post_vars
    return locals()


@auth.requires_membership('Administrador')
def admin_responsable():
    headers = {'usuario_responsable.id_usuario': 'Usuario', 'usuario_responsable.nombre_responsable': 'Responsable'}
    fields = [db.usuario_responsable.id_usuario, db.usuario_responsable.nombre_responsable]
    dictLinks = [dict(header='Editar', body=lambda row: A('Editar', _href=URL('editar_responsable', args=row.id,
                                                                              user_signature=True),
                                                          _class='btn btn-primary'))]
    grid = SQLFORM.grid(db.usuario_responsable, create=False, csv=False, fields=fields, searchable=False, details=False,
                        editable=False, headers=headers, links=dictLinks, maxtextlength=200)
    return locals()


@auth.requires_membership('Administrador')
def editar_responsable():
    id_user_resp = request.args(0) or redirect(URL('admin_responsable'))
    usuario_responsable = db.usuario_responsable(db.usuario_responsable.id == id_user_resp) or redirect(
        URL('admin_responsable'))

    formulario = SQLFORM.factory(
        Field("id_usuario", "reference auth_user", default=None, label="Usuario",
              requires=IS_IN_DB(db, 'auth_user.id', "%(username)s", zero=T('Elige un usuario'),
                                error_message=T("Valor incorrecto"))),
        Field("nombre_responsable", "reference responsable", default=None, label="Responsable",
              requires=IS_IN_DB(db, 'responsable.nombre', zero=T('Elige un responsable'),
                                error_message=T("Valor incorrecto"))),
    )

    if formulario.validate():
        id_usuario = formulario.vars.id_usuario
        nombre_responsable = formulario.vars.nombre_responsable
        #
        # row = db((db.usuario_responsable.id_usuario == id_usuario) & (
        #         db.usuario_responsable.nombre_responsable == nombre_responsable)).select()

        # if row:
        #     response.flash = T("El usuario ya tiene asignado este responsable.")
        # else:
        db(db.usuario_responsable.id == id_user_resp).update(id_usuario=id_usuario,
                                                             nombre_responsable=nombre_responsable)
        response.flash = T("El responsable se ha asignado correctamente.")
    return locals()


@auth.requires_login()
def no_autorizado():
    return locals()


@auth.requires_login()
def detalles():
    id_usuario = request.args(0) or redirect(URL('default', 'index'))
    usuario = db.auth_user[id_usuario] or redirect(URL('default', 'index'))
    rol = db.auth_membership(db.auth_membership.user_id == usuario.id).group_id.role
    return locals()
    
def modificar_password():
    formulario=auth.change_password()
    return locals()

@auth.requires_membership('Administrador')
def eliminar_usuario():
    # form = crud.create(db.auth_user, db.auth_membership)
    if not request.args(0):
        redirect(URL('administrar_usuario'))
    registro = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('administrar'))

    db(db.auth_user.id==registro.id).delete()
    session.modificar_usuario = None
    session.eliminar_usuario = 'Usuario eliminado correctamente'  
    
    redirect(URL('administrar_usuario'))
    return locals()

@auth.requires_membership('Administrador')
def modificar_usuario():
    # form = crud.create(db.auth_user, db.auth_membership)
    if not request.args(0):
        redirect(URL('administrar_usuario'))
    
    registro = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('administrar_usuario'))
    
    # consulta=db(db.graduado_pregrado.id==prueba)
    formulario = SQLFORM.factory(Field("first_name", label=T("Nombre"), default=registro.first_name, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("last_name", label=T("Apellido"), default=registro.last_name ),
                                Field("email", label=T("Correo"), default=registro.email, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                 Field("password", "password", label=T("Contraseña"), default=registro.password,  requires=[
                                       IS_NOT_EMPTY(T('El campo no puede estar vacío')), CRYPT()]),
                                Field("ci", label=T("No. Carnet"), default=registro.ci, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                 
                                )
    if formulario.validate():
        consulta2 = db.auth_user(db.auth_user.ci == formulario.vars.ci)
        if consulta2 is not None:            
            if registro.id == consulta2.id:
                session.eliminar_usuario = None
                session.modificar_usuario = 'Usuario actualizado correctamente'
                # response.flash = 'Graduado de pregrado actualizado correctamente'
                db(db.auth_user.id == registro.id).update(**formulario.vars)
                
                redirect(URL("administrar_usuario", args=registro.id))
            else:
                session.modificar_usuario = None
                session.usuario_ci = 'Ya existe un usuario registrado con ese carnet de identidad.'
                # response.flash = 'Ya existe un usuario con ese carnet'
                redirect(URL('modificar_usuario', args=registro.id))
        else:
            session.eliminar_usuario = None 
            session.modificar_usuario = 'Usuario actualizado correctamente'  
            # response.flash = 'Graduado de pregrado actualizado correctamente'        
            db(db.auth_user.id==registro.id).update(**formulario.vars) 
            print("Hola2")
            redirect(URL("administrar_usuario", args=registro.id)) 
    elif formulario.errors:
        session.error = True
        response.flash = 'El formulario tiene errores'      
            
    return locals()

@auth.requires_login()
def editar_usuario():

    # form = crud.create(db.auth_user, db.auth_membership)
    
    # registro = db.auth_user(auth.user.username == db.auth_user.username) or redirect(URL('administrar_usuario'))
    registro = db.auth_user(auth.user.email == db.auth_user.email) or redirect(
        URL('administrar_usuario'))

    
    # consulta=db(db.graduado_pregrado.id==prueba)
    formulario = SQLFORM.factory(Field("first_name", label=T("Nombre"), default=registro.first_name, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("last_name", label=T("Apellido"), default=registro.last_name ),
                                Field("email", label=T("Correo"), default=registro.email, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                 Field("password", "password", label=T("Contraseña"), default=registro.password,  requires=[
                                       IS_NOT_EMPTY(T('El campo no puede estar vacío')), CRYPT()]),
                                Field("ci", label=T("No. Carnet"), default=registro.ci, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                 
                                )
    if formulario.validate(): 
        
        consulta2 = db.auth_user(db.auth_user.ci == formulario.vars.ci) 
        if consulta2 is not None:       
            if auth.user.id == consulta2.id:
                session.usuario_ci = None
                session.eliminar_usuario = None
                session.modificar_usuario = 'Perfil actualizado correctamente'
                # response.flash = 'Graduado de pregrado actualizado correctamente'
                db(db.auth_user.id == auth.user.id).update(**formulario.vars)
                redirect(URL('usuario', 'editar_usuario'))
            else:            
                session.modificar_usuario = None
                session.usuario_ci = 'Ya existe un usuario registrado con ese carnet de identidad.'
                # response.flash = 'Ya existe un usuario con ese carnet'
                redirect(URL('usuario', 'editar_usuario'))           
        else:
            session.usuario_ci = None
            session.eliminar_usuario = None
            session.modificar_usuario = 'Perfil actualizado correctamente'
            # response.flash = 'Graduado de pregrado actualizado correctamente'
            db(db.auth_user.id == auth.user.id).update(**formulario.vars)
            auth.user.ci = formulario.vars.ci
            graduadospre = db(db.graduado_pregrado.ci ==
                              auth.user.ci).select().first()
            session.graduadopre = graduadospre
            redirect(URL('usuario', 'editar_usuario'))
    elif formulario.errors:
        session.error = True
        response.flash = 'El formulario tiene errores'      
            
    return locals()

@request.restful()
def pluvs():    
    """Return asynchronous graduado data for Datatable"""
    response.view = 'generic.json'

    def GET(*args, **kwargs):
        start = int(request.vars.start)
        limit = int(request.vars.limit)
        search = request.vars.search
        order_column = request.vars.order_column
        order_dir = request.vars.order_dir

        pluviometers = []
        count = 0
        try:
            pluviometers = db((db.auth_user.id > 1) &
                              (db.auth_user.ci.contains(search))|(db.auth_user.first_name.contains(search))|(db.auth_user.last_name.contains(search))|(db.auth_user.email.contains(search))).select(
                        orderby=f'{db.auth_user[order_column]} {order_dir}',
                        limitby=(start, start+limit)).as_list()

            count_query = db.auth_user.id.count()
            count = db((db.auth_user.id > 0) &
                        (db.auth_user.ci.contains(search))|(db.auth_user.first_name.contains(search))|(db.auth_user.last_name.contains(search))|(db.auth_user.email.contains(search))).select(count_query,
                                                                       cache=(cache.ram, None),cacheable=True).first()[count_query]
            
        except Exception as e:
            print(e)

        data = {
            'length': count,
            'pluvs': pluviometers
        }

        return data

    return locals()

@request.restful()
def pluvs_rol():    
    """Return asynchronous graduado data for Datatable"""
    response.view = 'generic.json'

    def GET(*args, **kwargs):
        start = int(request.vars.start)
        limit = int(request.vars.limit)
        search = request.vars.search
        order_column = request.vars.order_column
        order_dir = request.vars.order_dir

        pluviometers = []
        count = 0
        try:
            pluviometers = db((db.auth_user.id > 0) &
                              (db.auth_user.ci.contains(search))).select(
                        orderby=f'{db.auth_user[order_column]} {order_dir}',
                        limitby=(start, start+limit)).as_list()

            count_query = db.auth_user.id.count()
            count = db((db.auth_user.id > 0) &
                        (db.auth_user.ci.contains(search))).select(count_query,
                                                                       cache=(cache.ram, None),cacheable=True).first()[count_query]
            
        except Exception as e:
            print(e)

        data = {
            'length': count,
            'pluvs': pluviometers
        }

        return data

    return locals()