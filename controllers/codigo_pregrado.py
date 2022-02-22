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
from gluon.contrib.pyfpdf import FPDF, HTMLMixin

@auth.requires_login()
def codigos():
    db.codigo_pregrado.id.readable=False
    db.codigo_pregrado.id_solicitud_pregrado.readable=False
    db.solicitud_pregrado.id.readable=False
    db.auth_user.id.readable=False    
    db.solicitud_pregrado.motivo.readable=False
    db.solicitud_pregrado.entidad.readable=False
    db.solicitud_pregrado.fotocopia.readable=False        
    if auth.has_membership('Administrador') or auth.has_membership('Técnico'):       
        redirect(URL('codigo_pregrado','codigosadmin'))
    else:       
        lista = [db.codigo_pregrado.id, db.codigo_pregrado.codigo, db.codigo_pregrado.fecha]
        dictLinks = [dict(header='Descargar', body=lambda row: A('Código', _href=URL('codigo_pregrado','detalles',
                                                                 args=[row.id]),        
                                                         _class='btn btn-info'))]
        grid = SQLFORM.grid((db.codigo_pregrado.id_solicitud_pregrado==db.solicitud_pregrado.id)&((db.solicitud_pregrado.id_usuario==auth.user.id) | (db.solicitud_pregrado.ci==auth.user.ci)), fields=lista,  create=False,deletable=False, user_signature=False, details=False, editable=False, paginate=True, csv=False, 
                        links=dictLinks, searchable=False)
 
    
    return locals()

def codigosadmin():
    if auth.has_membership('Administrador') or auth.has_membership('Técnico'):
        contar=db(db.codigo_pregrado).count()
        return locals()
    else:
        redirect(URL('default','index'))
def verificar():    
    # form = crud.create(db.auth_user, db.auth_membership)
    codigo= request.vars["codigo"] or redirect(URL('default', 'index'))
    consultac=db(db.codigo_pregrado.codigo==codigo).select().first() or redirect(URL('default', 'index',  args="error"))

    session.codigos=consultac 
    consulta=db((consultac.id_solicitud_pregrado==db.solicitud_pregrado.id)).select().first()
    consulta3=db(db.secretaria_general).select().first()
    foto=consulta3.firma
    url=consulta3.url
    consulta2=db((consulta.tomo_secretaria==db.graduado_pregrado.tomo_secretaria)&(consulta.folio_secretaria==db.graduado_pregrado.folio_secretaria)&(consulta.numero_secretaria==db.graduado_pregrado.numero_secretaria)&(consulta.ci==db.graduado_pregrado.ci)).select().first()        
    listac=crearCodigo(consultac.codigo,foto,url,consultac.fecha) 
    session.verificado="Verificado"    
    return locals()


def detalles():
    # form = crud.create(db.auth_user, db.auth_membership)
    codigo= request.args(0) or redirect(URL('default', 'index'))    
    consultac=db(db.codigo_pregrado.id==codigo).select().first() or redirect(URL('default', 'index'))
    if consultac is None:            
        response.flash = 'El código no está registrado'
        redirect(URL('default', 'index')) 
    else: 
        session.codigos=consultac 
        consulta=db((consultac.id_solicitud_pregrado==db.solicitud_pregrado.id)).select().first()       
        consulta3=db(db.secretaria_general).select().first()
        foto=consulta3.firma
        url=consulta3.url
        consulta2=db((consulta.tomo_secretaria==db.graduado_pregrado.tomo_secretaria)&(consulta.folio_secretaria==db.graduado_pregrado.folio_secretaria)&(consulta.numero_secretaria==db.graduado_pregrado.numero_secretaria)&(consulta.ci==db.graduado_pregrado.ci)).select().first()        
        listac=crearCodigo(consultac.codigo,foto,url,consultac.fecha)    
    return locals()
def detalles2():
    # form = crud.create(db.auth_user, db.auth_membership)
    codigo= request.args(0) or redirect(URL('default', 'index'))
      
    consultac=db(db.codigo_pregrado.id_solicitud_pregrado==codigo).select().first() or redirect(URL('default', 'index'))
    if consultac is None:            
        response.flash = 'El código no está registrado'
        redirect(URL('default', 'index')) 
    else: 
        session.codigos=consultac 
        consulta=db((consultac.id_solicitud_pregrado==db.solicitud_pregrado.id)).select().first()       
        consulta3=db(db.secretaria_general).select().first()
        foto=consulta3.firma
        url=consulta3.url
        consulta2=db((consulta.tomo_secretaria==db.graduado_pregrado.tomo_secretaria)&(consulta.folio_secretaria==db.graduado_pregrado.folio_secretaria)&(consulta.numero_secretaria==db.graduado_pregrado.numero_secretaria)&(consulta.ci==db.graduado_pregrado.ci)).select().first()        
        listac=crearCodigo(consultac.codigo,foto,url,consultac.fecha)    
    return locals()

def GenerateCodigo(ci):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=1,
    )
    qr.add_data(ci)
    qr.make(fit=True)
    # img = qrcode.make(ci)
    img = qr.make_image(fill_color="black", back_color="white")
   
    return img.resize((160, 160))

def crearCodigo(codigo,foto,url, fecha):    
    codigoLbl = url+"codigo_pregrado/verificar?codigo="+codigo
    
    url = os.path.join(request.folder, "static/images/etiqueta.png")
    etiqueta = Image.open(url)
    qrImg = GenerateCodigo(codigoLbl)
    
    urlfoto = os.path.join(request.folder, "uploads/"+foto)
    
    new_imagen= Image.open(urlfoto)
    perfilImg = new_imagen.resize((250,130))

    final = Image.new("RGB", (etiqueta.size[0], etiqueta.size[1]), "black")

    final.paste(etiqueta, (0, 0))
    if len(codigoLbl)<=10:
        final.paste(qrImg, (30, 40))
    else:
        final.paste(qrImg, (40, 40))
    final.paste(perfilImg, (380, 50))

    draw = ImageDraw.Draw(final)
    tipoFont = os.path.join(request.folder, "static/fonts/arial.ttf") 
    tipoFont2 = os.path.join(request.folder, "static/fonts/ALGER.TTF") 
    tipoFont3 = os.path.join(request.folder, "static/fonts/CalibriLI.TTF")     
    fontCodigo = ImageFont.truetype(tipoFont, 30)
    fontValido = ImageFont.truetype(tipoFont2, 25) 
    draw.text((45, 200), codigo, (0, 2, 7), font=fontCodigo)
    draw.text((100, 270), "Válido solo para el territorio nacional", (0, 2, 7), font=fontValido)
    draw.text((250, 10), fecha, (0, 2, 7), font=fontCodigo)

    output = open("./applications/unilegal/static/codigos/"+codigo+".png", "wb")
    final.save(output)
    

    # return final.show()

@auth.requires_login()
def descargarpdf():  
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
            pluviometers = db((db.codigo_pregrado.id > 0) &
                              (db.codigo_pregrado.codigo.contains(search))).select(
                        orderby=f'{db.codigo_pregrado[order_column]} {order_dir}',
                        limitby=(start, start+limit)).as_list()

            count_query = db.codigo_pregrado.id.count()
            count = db((db.codigo_pregrado.id > 0) &
                        (db.codigo_pregrado.codigo.contains(search))).select(count_query,
                                                                       cache=(cache.ram, None),cacheable=True).first()[count_query]
            
        except Exception as e:
            print(e)

        data = {
            'length': count,
            'pluvs': pluviometers
        }
        
        return data

    return locals()
def exportarpdf():
    # fecha= request.vars["fecha"] or redirect(URL('default', 'index'))
   
    

    response.title = "Universidad de Ciego de Ávila Máximo Gómez Báez"   

   

    
    fechad=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
    head = THEAD(TR(TH("No", _width="8%"), 
                    TH("Código", _width="10%"),
                    TH("Nombre", _width="10%"),
                    TH("Apellidos", _width="20%"),
                    TH("CI", _width="8%"),
                    TH("Tomo SG", _width="7%"),
                    TH("Folio SG", _width="7%"),
                    TH("Número SG", _width="8%"),
                    TH("Año Graduación", _width="10%"),
                    TH("Fecha generado", _width="10%"),
                    # TH("Hora", _width="8%"),
                    # TH("Ip", _width="8%"),
                    # TH("Tamaño (MB)", _width="8%"),
                    # TH("Tipo", _width="8%"),
                    # TH("Comportamiento", _width="12%"), 
                    _bgcolor="#A0A0A0"))
    
    # reclamaciones=db(db.reclamacion).select()
    
    contar=db((db.codigo_pregrado.id_solicitud_pregrado==db.solicitud_pregrado.id)&(db.solicitud_pregrado.id_usuario==db.auth_user.id)).count()
    class MyFPDF(FPDF, HTMLMixin):
        def header(self):
            """
            define doc header
            """
            # self.image('logo.png', 10, 8, 33)
            self.set_font('Arial', 'B', 15)
            self.cell(0, 8, response.title, ln=1, align="C")
            # self.cell(0, 10, f"<img src="+"{{=URL('static','images/logo.png')}}"+" alt="+"John Doe" +"/>", align="C", ln=1)
            self.cell(
                0, 8, f"Fecha: {fechad}", align="C", ln=1)
            self.cell(
                0, 8, f"Total de códigos de pregrado generados: {contar}", align="C", ln=1)
            
           
    pdf = MyFPDF()
    pdf.add_page(orientation='L') 
    codigos=db((db.codigo_pregrado.id_solicitud_pregrado==db.solicitud_pregrado.id)&(db.solicitud_pregrado.id_usuario==db.auth_user.id)).select()
    cont=0
    
    rows = []  
    for i in codigos:
        cont=cont+1                    
        rows.append(TR(
                TD(cont),
                TD(i.codigo_pregrado.codigo),
                TD(i.auth_user.first_name),
                TD(i.auth_user.last_name),
                TD(i.solicitud_pregrado.ci),
                TD(i.solicitud_pregrado.tomo_secretaria),
                TD(i.solicitud_pregrado.folio_secretaria),
                TD(i.solicitud_pregrado.numero_secretaria),
                TD(i.solicitud_pregrado.graduacionyear),
                TD(i.codigo_pregrado.fecha),
                # TD(i.hora),
                # TD(i.ip),
                # TD(i.tamano),
                # TD(i.tipo),
                # TD(i.comportamiento),
                _bgcolor="#F0F0F0"))
                # pdf.cell(0, 8,  f"{cont} {i.id_estudiante.nombre_apellidos} {i.id_estudiante.ci} {i.id_estudiante.centro} {i.nota}", 0, ln=2)
          
    
        # pdf.cell(0, 8,  f"{cont} {i.id_estudiante.nombre_apellidos} {i.id_estudiante.ci} {i.id_estudiante.centro} {i.nota}", 0, ln=2)

    body = TBODY(*rows)
    table = TABLE(*[head, body], 
                _border="1", _align="center", _width="100%", _style="font-size:6px")
    
    
    
    # pdf.write_html(str(XML(table, sanitize=False)))
    pdf.write_html('<font size="9">' + table.xml().decode('utf-8') + '</font>')
    pdf.ln(5)      


    response.headers['Content-Type'] = 'application/pdf'
    return pdf.output(dest='S') 