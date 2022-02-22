import unittest
from name_utils import slug, abbreviate
import qrcode
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import io
import qrcode
from datetime import datetime
from datetime import date
import calendar
import locale
import time
import uuid

@auth.requires_login()
def denegadas():
    db.solicitud_pregrado.id.readable=False
    db.solicitud_pregrado.entidad.readable=False
    db.solicitud_pregrado.motivo.readable=False
    db.solicitud_pregrado.fotocopia.readable=False
    if auth.has_membership('Administrador') or auth.has_membership('Técnico'):
        
        redirect(URL('solictud_pregrado','solicitudadmin'))
    else:
        # lista = [db.solicitud_pregrado.id, db.solicitud_pregrado.ci, db.solicitud_pregrado.tomo_secretaria,db.solicitud_pregrado.folio_secretaria,db.solicitud_pregrado.numero_secretaria,db.solicitud_pregrado.estado]
        
        grid = SQLFORM.grid(((db.solicitud_pregrado.id_usuario==auth.user.id) | (db.solicitud_pregrado.ci==auth.user.ci))&(db.solicitud_pregrado.estado=="Denegada"), 
                            searchable=False,
                            paginate=False,
                            create=False,
                            csv=False,
                            sortable = False,
                            maxtextlength = 50,
                            showbuttontext=False)
        
    
    
    return dict(grid=grid)


def solicitudadmin():
    if auth.has_membership('Administrador') or auth.has_membership('Técnico'):
        contar=db(db.solicitud_pregrado).count()
        return locals()
    else:
        redirect(URL('default','index'))

def admin_solicitud_pregrado():
    db.solicitud_pregrado.id.readable=False
    db.solicitud_pregrado.entidad.readable=False
    db.solicitud_pregrado.motivo.readable=False
    db.solicitud_pregrado.fotocopia.readable=False  
    x=uuid.uuid4()
    str(x)
    # print(uuid.UUID(bytes=x.bytes))
    if auth.has_membership('Administrador'):        
         redirect(URL('solicitud_pregrado','solicitudadmin'))
    else:
        lista = [db.solicitud_pregrado.id, db.solicitud_pregrado.ci, db.solicitud_pregrado.tomo_secretaria,db.solicitud_pregrado.folio_secretaria,db.solicitud_pregrado.numero_secretaria]
        
      
        grid = SQLFORM.grid(((db.solicitud_pregrado.id_usuario==auth.user.id) | (db.solicitud_pregrado.ci==auth.user.ci))&(db.solicitud_pregrado.id==db.codigo_pregrado.id_solicitud_pregrado), fields=lista, create=False,
                        deletable=True, details=False, editable=False, paginate=False, csv=False, 
                        # links=dictLinks,
                         searchable=False)
    
    
    return dict(grid=grid)


@auth.requires_login()
def detalles():
    id_sol = request.args(0) or redirect(URL('default', 'index'))
    consulta = db.solicitud_pregrado[id_sol] or redirect(URL('default', 'index'))
    consultac= db(db.codigo_pregrado.id_solicitud_pregrado==consulta.id).select().first()
    if consultac is not None:
        session.codigos=consultac                
        consulta3=db(db.secretaria_general.id==consulta.id_secretaria_general).select().first()
        foto=consulta3.firma
        consulta2=db((consulta.tomo_secretaria==db.graduado_pregrado.tomo_secretaria)&(consulta.folio_secretaria==db.graduado_pregrado.folio_secretaria)&(consulta.numero_secretaria==db.graduado_pregrado.numero_secretaria)&(consulta.ci==db.graduado_pregrado.ci)).select().first()        
        listac=crearCodigo(consultac.codigo,foto)


    return locals()

@auth.requires_login()
def crear_solicitud_pregrado():
    if (not auth.has_membership('Técnico') ) & (not auth.has_membership('Administrador')):
        db.solicitud_pregrado.tomo_secretaria.writable=False
        db.solicitud_pregrado.folio_secretaria.writable=False
        db.solicitud_pregrado.numero_secretaria.writable=False
        db.solicitud_pregrado.graduacionyear.writable=False
    # form = crud.create(db.auth_user, db.auth_membership)
    db.solicitud_pregrado.estado.writable=False
    if (not auth.has_membership('Técnico'))& (not auth.has_membership('Administrador')):
        db.solicitud_pregrado.ci.writable=False
    formulario = SQLFORM.factory(db.solicitud_pregrado,table_name='solicitud_pregrado')    

    if formulario.process().accepted:
        if (("jpg" in formulario.vars["fotocopia"]) or ("JPG" in formulario.vars["fotocopia"]) or ("png" in formulario.vars["fotocopia"]) or ("PNG" in formulario.vars["fotocopia"]) or ("jpeg" in formulario.vars["fotocopia"]) or ("JPEG" in formulario.vars["fotocopia"])):
            
            if (not auth.has_membership('Técnico') )& (not auth.has_membership('Administrador')):
                ci=auth.user.ci
            else:
                ci= formulario.vars["ci"]
            
            consulta_ci=db((db.solicitud_pregrado.id_usuario==auth.user.id)&(db.solicitud_pregrado.ci==ci)).select().first()
            if consulta_ci is None:
                fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
                response.flash = 'formulario aceptado'
                mensage=""                
                graduado=db(db.graduado_pregrado.ci==auth.user.ci).select().first()
                
                
                if (not auth.has_membership('Técnico') )& (not auth.has_membership('Administrador')):
                    id_solicitud = db.solicitud_pregrado.insert(id_usuario=auth.user.id, ci=graduado.ci, tomo_secretaria=graduado.tomo_secretaria,folio_secretaria=graduado.folio_secretaria,numero_secretaria=graduado.numero_secretaria,graduacionyear=graduado.fecha_graduado,entidad=formulario.vars["entidad"],motivo=formulario.vars["motivo"],fotocopia=formulario.vars["fotocopia"])
                else:
                    id_solicitud = db.solicitud_pregrado.insert(id_usuario=auth.user.id, ci=ci, tomo_secretaria=formulario.vars["tomo_secretaria"],folio_secretaria=formulario.vars["folio_secretaria"],numero_secretaria=formulario.vars["numero_secretaria"],graduacionyear=formulario.vars["graduacionyear"],entidad=formulario.vars["entidad"],motivo=formulario.vars["motivo"],fotocopia=formulario.vars["fotocopia"])
                
              
                consulta=db((db.solicitud_pregrado.id_usuario==auth.user.id)&(db.solicitud_pregrado.id==id_solicitud)).select().first()
                
                # print(consulta.folio_secretaria)
                consulta2=db((consulta.tomo_secretaria==db.graduado_pregrado.tomo_secretaria)&(consulta.folio_secretaria==db.graduado_pregrado.folio_secretaria)&(consulta.numero_secretaria==db.graduado_pregrado.numero_secretaria)&(consulta.ci==db.graduado_pregrado.ci)).select().first()        
                if(consulta2 is not None):
                    db((db.solicitud_pregrado.id_usuario==auth.user.id)&(db.solicitud_pregrado.id==id_solicitud)).update(estado="Aceptada")
                    db.codigo_pregrado.insert(codigo=borrar_espacio(cipher_encrypt(str(consulta.numero_secretaria)+consulta2.nombre1,int(consulta.ci))),id_solicitud_pregrado=id_solicitud,fecha=fecha)
                    # redirect(URL('codigo_pregrado', 'codigos'))
                    session.codigo= " Se ha registrado la solicitud de pregrado. Sus datos han sido validados y son los correctos. Revise y descargue su código generado."
                
                    redirect(URL('codigo_pregrado', 'codigos'))
                else:
                    # db((db.solicitud_pregrado.id_usuario==auth.user.id)&(db.solicitud_pregrado.id==id_solicitud)).update(estado="Denegada")
                    db((db.solicitud_pregrado.id_usuario==auth.user.id)&(db.solicitud_pregrado.id==id_solicitud)).delete()
                    response.flash = mensage
                    redirect(URL('solicitud_pregrado', 'crear_solicitud_pregrado', args="denegada"))
                
            else:
                response.flash = 'Ya existe una solicitud registrada con ese carnet'
            
        else:
            response.flash = 'La fotocopia debe ser una imagen con extensión .jpg, .png o .jpeg'
    elif formulario.errors:
        response.flash = 'Error en el formulario'

    return locals()

@auth.requires_login()
def index2():
    db.solicitud_pregrado.id.readable=False
    if auth.has_membership('Administrador'):
        grid = SQLFORM.grid(db.solicitud_pregrado, editable=True, details=False, paginate=False, csv=False, user_signature=False, searchable=False, create=False)
    else:
        grid = SQLFORM.grid(db.solicitud_pregrado.id_usuario==auth.user.id, editable=True, details=False, paginate=False, csv=False, user_signature=False, searchable=False, create=False)
    
    return dict(grid=grid)
def cipher_encrypt(plain_text, key):    
    encrypted = ""
    for c in plain_text:
        if c.isupper(): 
            c_index = ord(c) - ord('A')
            c_shifted = (c_index + key) % 26 + ord('A')
            c_new=chr(c_shifted)
            encrypted+=c_new
        elif c.islower(): #check if its a lowecase character
            # subtract the unicode of 'a' to get index in [0-25) range
            c_index = ord(c) - ord('a') 
            c_shifted = (c_index + key) % 26 + ord('a')
            c_new = chr(c_shifted)
            encrypted += c_new
        elif c.isdigit():
            # if it's a number,shift its actual value 
            c_new = (int(c) + key) % 10
            encrypted += str(c_new)
        else:
            # if its neither alphabetical nor a number, just leave it like that
            encrypted += c
    return encrypted
def borrar_espacio(plain_text):    
    encrypted = ""
    if " " in plain_text:
        for c in plain_text:
            if c!=" ":
                encrypted += c
            pass
        pass
    else:
        encrypted = plain_text
    return encrypted
@auth.requires_membership('Administrador')
def eliminar_solicitud_pregrado():
    # form = crud.create(db.auth_user, db.auth_membership)
    if not request.args(0):
        redirect(URL('admin_graduado_pregrado'))
    registro = db.solicitud_pregrado(request.args(0, cast=int)
                            ) or redirect(URL('administrar'))

    db(db.solicitud_pregrado.id==registro.id).delete()
    session.status = True
    session.eliminar_solicitud_graduado = 'Solicitud de pregrado eliminada correctamente.'
    
    redirect(URL('admin_solicitud_pregrado'))
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
            pluviometers = db((db.solicitud_pregrado.id > 0) & 
                              (db.solicitud_pregrado.ci.contains(search))).select(
                        orderby=f'{db.solicitud_pregrado[order_column]} {order_dir}',
                        limitby=(start, start+limit)).as_list()

            count_query = db.solicitud_pregrado.ci.count()
            count = db((db.solicitud_pregrado.id > 0) &
                        (db.solicitud_pregrado.ci.contains(search))).select(count_query,
                                                                       cache=(cache.ram, None),cacheable=True).first()[count_query]
            
        except Exception as e:
            print(e)

        data = {
            'length': count,
            'pluvs': pluviometers
        }

        return data

    return locals()