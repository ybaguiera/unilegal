@auth.requires_membership('Administrador')
def admin_secretaria_general():
    db.secretaria_general.id.readable=False
    grid = SQLFORM.smartgrid(db.secretaria_general,
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

@auth.requires_membership('Administrador')
def crear_secretaria_general():
    # form = crud.create(db.auth_user, db.auth_membership)

    formulario = SQLFORM(db.secretaria_general)    

    if formulario.process().accepted:
        response.flash = 'Se ha registrado la secretaría general'     
        
        
    elif formulario.errors:
        response.flash = 'Error en el formulario'
    return locals()


