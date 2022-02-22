@auth.requires_membership('Administrador')
def admina():
    db.graduado_pregrado.id.readable=False
    grid = SQLFORM.smartgrid(db.graduado_pregrado,
                            linked_tables = [],
                            searchable=False,
                            paginate=False,
                            create=False,
                            csv=False,
                            sortable = False,
                            maxtextlength = 400,
                            showbuttontext=False,
                             )
    return dict(grid=grid)
def admin_graduado_pregrado():    
    if auth.has_membership('Administrador') or auth.has_membership('Técnico'):
        contar=db(db.graduado_pregrado).count()
        return locals()
    else:
        redirect(URL('default','index'))
    
    return locals()

@auth.requires_membership('Administrador')
def crear_graduado_pregrado():
    # form = crud.create(db.auth_user, db.auth_membership)

    formulario = SQLFORM(db.graduado_pregrado)    

    if formulario.process().accepted:      
        # session.aceptado_graduado = 'Se ha registrado el graduado de pregrado'  
        response.flash = 'Se ha registrado el graduado de pregrado'     
        
        
    elif formulario.errors:
        response.flash = 'Error en el formulario'
    return locals()

@auth.requires_membership('Administrador')
def eliminar_graduado_pregrado():
    # form = crud.create(db.auth_user, db.auth_membership)
    if not request.args(0):
        redirect(URL('admin_graduado_pregrado'))
    registro = db.graduado_pregrado(request.args(0, cast=int)
                            ) or redirect(URL('administrar'))

    db(db.graduado_pregrado.id==registro.id).delete()
    session.modificar_graduado = None
    session.eliminar_graduado = 'Graduado de pregrado eliminado correctamente'  
    
    redirect(URL('admin_graduado_pregrado'))
    return locals()
@auth.requires_membership('Administrador')
def modificar_graduado_pregrado():
    # form = crud.create(db.auth_user, db.auth_membership)
    if not request.args(0):
        redirect(URL('admin_graduado_pregrado'))
 
    registro = db.graduado_pregrado(request.args(0, cast=int)
                            ) or redirect(URL('admin_graduado_pregrado'))
    # consulta=db(db.graduado_pregrado.id==prueba)
    formulario = SQLFORM.factory(Field("nombre1", label=T("Primer Nombre"), default=registro.nombre1, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("nombre2", label=T("Segundo Nombre"), default=registro.nombre2 ),
                                Field("apellido1", label=T("Primer Apellido"), default=registro.apellido1, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("apellido2", label=T("Segundo Apellido"), default=registro.apellido2, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("ci", label=T("No. Carnet"), default=registro.ci, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("tomo_secretaria", label=T("Tomo SG"), default=registro.tomo_secretaria, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("fecha_graduado", label=T("Fecha de Graduado"), default=registro.fecha_graduado, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("folio_secretaria", label=T("Folio SG"), default=registro.folio_secretaria, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("numero_secretaria", label=T("Número SG"), default=registro.numero_secretaria, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("pais", label=T("País"), default=registro.pais, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("modalidad", label=T("Modalidad"), default=registro.modalidad, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                Field("carrera", label=T("Carrera"), default=registro.carrera, requires=IS_NOT_EMPTY(T('El campo no puede estar vacío'))),
                                
                                )
    if formulario.validate():
        session.eliminar_graduado = None 
        session.modificar_graduado = 'Graduado de pregrado actualizado correctamente'  
        # response.flash = 'Graduado de pregrado actualizado correctamente'        
        db(db.graduado_pregrado.id==registro.id).update(**formulario.vars) 
        redirect(URL("admin_graduado_pregrado", args=registro.id)) 
    elif formulario.errors:
        session.error = True
        response.flash = 'El formulario tiene errores'      
            
   
    return locals()
#-----------------------------------------------
# APIS
#-----------------------------------------------
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

            pluviometers = db((db.graduado_pregrado.id > 0) &
                              ((db.graduado_pregrado.ci.contains(search)))|(db.graduado_pregrado.nombre1.contains(search))|(db.graduado_pregrado.fecha_graduado.contains(search))|(db.graduado_pregrado.folio_secretaria.contains(search))|(db.graduado_pregrado.numero_secretaria.contains(search))|(db.graduado_pregrado.pais.contains(search))|(db.graduado_pregrado.modalidad.contains(search))|(db.graduado_pregrado.carrera.contains(search))|(db.graduado_pregrado.nombre2.contains(search))|(db.graduado_pregrado.apellido1.contains(search))|(db.graduado_pregrado.apellido2.contains(search))).select(
                        orderby=f'{db.graduado_pregrado[order_column]} {order_dir}',
                        limitby=(start, start+limit)).as_list()

            count_query = db.graduado_pregrado.ci.count()
            
            count = db((db.graduado_pregrado.id > 0) &
                       ((db.graduado_pregrado.ci.contains(search)))|(db.graduado_pregrado.nombre1.contains(search))|(db.graduado_pregrado.fecha_graduado.contains(search))|(db.graduado_pregrado.folio_secretaria.contains(search))|(db.graduado_pregrado.numero_secretaria.contains(search))|(db.graduado_pregrado.pais.contains(search))|(db.graduado_pregrado.modalidad.contains(search))|(db.graduado_pregrado.carrera.contains(search))|(db.graduado_pregrado.nombre2.contains(search))|(db.graduado_pregrado.apellido1.contains(search))|(db.graduado_pregrado.apellido2.contains(search))).select(count_query,
                                                                       cache=(cache.ram, None),cacheable=True).first()[count_query]
            
        except Exception as e:
            print(e)

        data = {
            'length': count,
            'pluvs': pluviometers
        }

        return data

    return locals()

# request.args(0)