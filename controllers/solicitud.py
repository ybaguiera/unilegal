@auth.requires_login()
def index():
    db.solicitud.id.readable=False
    grid = SQLFORM.smartgrid(db.solicitud,
                            linked_tables = [],
                            searchable=False,
                            paginate=False,
                            csv=False,
                            sortable = False,
                            maxtextlength = 50,
                            showbuttontext=False,
                             )
    return dict(grid=grid)
@auth.requires_login()
def index2():
    db.solicitud_pregrado.id.readable=False
    grid = SQLFORM.smartgrid(db.solicitud,
                            linked_tables = [],
                            searchable=False,
                            paginate=False,
                            csv=False,
                            sortable = False,
                            maxtextlength = 50,
                            showbuttontext=False,
                             )
    return dict(grid=grid)
