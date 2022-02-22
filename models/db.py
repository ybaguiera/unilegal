# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth





# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL("sqlite://dbSecretaria.db")

    # base de datos para las tareas programadas
    dbTask = DAL("sqlite://dbTask.db")
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------



auth.settings.extra_fields['auth_user'] = [
    Field('ci',
              'string',
              unique=True,
              required=True,
              label=T('No. Carnet'),
              requires=[IS_NOT_EMPTY(T('Este campo no puede estar vacío')),IS_CORRECT_CI()])
 ]
auth.define_tables(username=False, signature=False,migrate=True)

auth.settings.login_url = URL('default', 'user/login')
auth.settings.login_next = URL('default', 'index')
auth.settings.on_failed_authentication = URL('default', 'user/login')
auth.settings.logout_next = URL('default', 'index')


auth.messages.invalid_login = T('Falló la autenticación. Usuario o contraseña incorrecto.')
auth.messages.invalid_user = T('El usuario especificado no es válido.')
auth.messages.is_empty = T("No puede ser vacío.")
auth.messages.logged_out = T('Se ha cerrado la sesión.')







# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#


solicitud1 = '%(tomo_secretaria)s'
# tipo = ('Desconocido', 'Masculino', 'Femenino')
solicitud= db.Table(db,'solicitud',
                Field('id_usuario',
                      "reference auth_user",
                      default=auth.user_id,
                      writable=False, readable=False
                      ),
                Field('ci',
                       'string',
                        unique=True,
                        required=True,
                        label=T('No. Carnet'),
                        requires=[IS_NOT_EMPTY(T('Este campo no puede estar vacío')),IS_CORRECT_CI()]),
                Field('tomo_secretaria',
                      'integer',
                      required=True,
                      label=T('Tomo en la SG'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('folio_secretaria',
                      'string',
                      required=True,
                      label=T('Folio en la SG'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('numero_secretaria',
                      'string',
                      required=True,
                      label=T('Número en la SG'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
               Field('graduacionyear',
                      'string',
                      required=True,
                      label=T('Año Graduado'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),                
               Field('entidad',
                      'string',
                      required=True,
                      label=T('Entidad que autoriza'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                      
              Field('motivo',
                      'text',
                      required=True,
                      label=T('Motivo de la solicitud'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                      

                Field('fotocopia',
                      'upload',default="",
                      
                       required=True,
                       label=T('Fotocopia del título'),
                       requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))],
                       uploadfolder='./applications/unilegal/static/titulos',
                  #      uploadseparate=True
                       ),
                  
                 Field('estado',
                      'string',
                      required=False,
                      label=T('Estado'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                  #     requires=IS_IN_SET([T('Aceptada'),T('Denegada'),T('En proceso'),T('Lista'),T('Recogida')],zero=T('Elija el estado'), error_message=T('Debe elegir una'))),
              format=solicitud1)
# db.solicitud._singular = T('Solicitud')
# db.solicitud._plural = T('Solicitudes')

db.define_table('graduado_pregrado',
                Field('nombre1',
                      'string',
                      required=True,
                      label=T('1er Nombre'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('nombre2',
                      'string',
                      required=False,
                      label=T('2do Nombre')
                      ),
                Field('apellido1',
                      'string',
                      required=True,
                      label=T('1er Apellido'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('apellido2',
                      'string',
                      required=True,
                      label=T('2do Apellido'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('ci',
                        'string',                        
                        required=True,
                        label=T('No. Carnet'),
                        requires=[IS_NOT_EMPTY(T('Este campo no puede estar vacío')),IS_CORRECT_CI()]),
                Field('tomo_secretaria',
                      'integer',
                      required=True,
                      label=T('Tomo SG'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('fecha_graduado',
                      'string',
                      required=True,
                      label=T('Fecha de graduado'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('folio_secretaria',
                      'string',
                      required=True,
                      label=T('Folio SG'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('numero_secretaria',
                      'string',
                      required=True,
                      label=T('Número SG'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('pais',
                      'string',
                      required=True,
                      label=T('País'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('modalidad',
                      'string',
                      required=True,
                      label=T('Modalidad'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                Field('carrera',
                      'string',
                      required=True,
                      label=T('Carrera'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
                      format='%(nombre1)s',  migrate=True      
                   
             )
# db.solicitud._singular = T('Solicitud')
# db.solicitud._plural = T('Solicitudes')
sg = '%(centro)s'
db.define_table('secretaria_general',                 
                  Field('centro',
                      'string',
                      required=True,
                      label=T('Centro'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),                     

                Field('firma',
                      'upload',
                       required=True,
                       label=T('Firma Digital'),
                       requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))],
                       default=None),
                  Field('url',
                      'string',
                      required=True,
                      label=T('URL'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),   
            migrate=True,
                   format=sg)

solicitudPregrado = '%(tomo_facultad)s'
db.define_table('solicitud_pregrado',solicitud,            
              
            #   Field('tomo_facultad',
            #           'integer',
            #           required=True,
            #           label=T('Tomo en la Facultad'),
            #           requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
            #   Field('folio_facultad',
            #           'integer',
            #           required=True,
            #           label=T('Folio en la Facultad'),
            #           requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
            migrate=True,
            format=solicitud1)

db.define_table('codigo_pregrado',
              Field('codigo',
                      'string',
                      unique=True,              
                      required=True,
                      label=T('Codigo'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
            Field('fecha',
                      'string',
                      required=True,
                      label=T('Fecha generado'),
                      requires=[IS_NOT_EMPTY(T('El campo no puede estar vacío'))]),
              Field("id_solicitud_pregrado", "reference solicitud_pregrado", label=T("Solicitud de pregrado"), unique=True,
                      requires=IS_IN_DB(db, 'solicitud_pregrado.id', db.solicitud_pregrado._format,
                                        zero=T('Elige una solicitud pregrado'),
                                        error_message=T("¡Valor inválido!"))), format='%(codigo)s', migrate=True 
                   
                   )
db.solicitud_pregrado._singular = T('Solicitud de pregrado')
db.solicitud_pregrado._plural = T('Solicitudes de pregrado')








# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
