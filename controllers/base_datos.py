# -*- coding: utf-8 -*-
import csv
import os
import datetime
import locale
# import openpyxl
import sys
# from business_calendar import Calendar, MO, TU, WE, TH, FR
# import xlrd

def transform_roman_numeral_to_number(roman_numeral):
    roman_char_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    res = 0
    for i in range(0, len(roman_numeral)):
        if i == 0 or roman_char_dict[roman_numeral[i]] <= roman_char_dict[roman_numeral[i - 1]]:
            res += roman_char_dict[roman_numeral[i]]
        else:
            res += roman_char_dict[roman_numeral[i]] - 2 * roman_char_dict[roman_numeral[i - 1]]
    return res

def transform_folio(cadena):        
    picar = cadena[0:len(cadena)]  
    aux=""    
    for i in range(0, len(picar)):        
        if picar[i]=="O":            
            aux += "0"
        else:
            aux += picar[i]        
    return aux

@auth.requires_membership('Administrador')
def importar_pregrado():
    """
    Es el controlador principal donde el
    usuario importa el archivo csv.
    :return: locals
    """
     
    lista = []
    
    form = FORM(DIV(SPAN("Delimitador del fichero csv:"),
                    SELECT(OPTION('Punto y coma', _value='punto_coma'), OPTION(
                        'Coma', _value='coma'), _name="delimitador", _class="form-control"),' '),
                      
                 DIV(SPAN("Cambios en el excel:"),SELECT(OPTION('No', _value='no'), OPTION('Si', _value='si'), _name="cambios", _class="form-control")),
               DIV(SPAN("Seleccione el archivo excel para importar:")), 
                DIV(     
                    INPUT(_type='file', _name='csvfile', _style="display: block; margin-top: 15px;",
                          requires=IS_NOT_EMPTY(T('Seleccione un fichero'))),
                    INPUT(_type='submit', _value=T('Importar'), _class="btn btn-primary",
                          _style="display: block; margin-top: 15px;"),
                    _class="col-md-4", _style="padding-left:0px!important;")
                )

    if form.process().accepted:
        try:
            # cargo el archivo
            file = form.vars.csvfile.file
            cambios = form.vars.cambios  
            # __copia_seguridad_bd()
            # __truncate()           
            # proceso el csv
            if form.vars.delimitador == "punto_coma":            
                lista = __procesar_pregrado(file,cambios)             
            else:
                lista = __procesar_pregrado_coma(file,cambios)

        except Exception as e:
            # Si ocurre un error, lo muestro, y cambio el estado de actualizacion
            # db(db.verificar_actualizacion.id > 0).update(actualizando=False)
            # db.commit()
            # __restaurar_bd()
            response.flash = T('Error importando el archivo csv. ')
        else:
            response.flash = "El archivo ha sido cargado con éxito!!!"

    return locals()

def __cargar(file, delimitador, **kwargs):
    """
    Este metodo carga el archivo csv
    :param ruta: Ruta del archivo
    :param kwargs: Argumentos opcionales de formato del csv
    :return: Un iterable con cada linea leida
    """
    # delimiter = kwargs.get('delimiter', ';')
    delimiter = kwargs.get('delimiter', delimitador)
    quotechar = kwargs.get('quotechar', '"')
    quoting = kwargs.get('quoting', csv.QUOTE_MINIMAL)

    # archivo = open(ruta, 'rb')
    # print(file)
    import codecs, io
    StreamReader = codecs.getreader('latin1')
    wrapper = StreamReader(file)
    reader = csv.reader(wrapper, delimiter=delimiter,
                        quotechar=quotechar, quoting=quoting)

    # StreamReader = codecs.getreader('latin1')
    # wrapper = StreamReader(file)    
    # reader = xlrd.open_workbook(wrapper)
    # print(reader)
    return reader

def __procesar_pregrado(file,cambios):
    # -*- coding: utf-8 -*-
    """
    Este método procesa los datos del archivo csv.
    Primero se carga el archivo y luego se recorre cada linea
    según el formato sugerido.

    A medida que se analiza cada linea se guarda en una lista que
    contiene  una clase Tabla donde se guarda el responsable, su
    area y una lista con sus medios. Esta lista se procesa luego
    para insertar en la base de datos y guardar los cambios con respecto
    a la base de datos anterior.
    """
    reader = __cargar(file, ";")    
    # documento = xlrd.open_workbook('./applications/prueba4o.xlsx')
   
    # carrera = documento.sheet_by_index(0)
    
    print(cambios)
    listaTabla = []
    if cambios == "no":
        print("No")
        try:
            for line in reader: #Ignoramos la primera fila, que indica los campos              
                try:
                    ci = int(line[6]) and len(line[6]) == 11
                except:
                    ci = 0
                if ci: 
                                
                    grad=db(db.graduado_pregrado.ci==line[6]).select().first()                
                    if line[2]=="":
                        aux=" "
                    else:
                        aux=line[2]                
                
                    if (type(line[11]) is 'str'):
                        tomo=int(line[11])
                    else:
                        tomo=transform_roman_numeral_to_number(line[11])  
                    cadena=transform_folio(line[12])           
                    if grad:                   
                        
                        db(db.graduado_pregrado.ci==line[6]).update(nombre1=line[1],nombre2=aux,apellido1=line[3],apellido2=line[4],tomo_secretaria=tomo,fecha_graduado=line[9],folio_secretaria=cadena,numero_secretaria=line[14],pais=line[15],modalidad=line[16],carrera=line[13])
                        # print(line)
                    else:
                        
                        db.graduado_pregrado.insert(nombre1=line[1],nombre2=aux,apellido1=line[3],apellido2=line[4],ci=line[6],tomo_secretaria=tomo,fecha_graduado=line[9],folio_secretaria=cadena,numero_secretaria=line[14],pais=line[15],modalidad=line[16],carrera=line[13])
                
            pass   
        except csv.Error as e:
            raise SystemError('El fichero seleccionado no es válido.')   
    else:
        try:
            print("Si")
            for line in reader: #Ignoramos la primera fila, que indica los campos              
                try:
                    ci = int(line[6]) and len(line[6]) == 11
                except:
                    ci = 0
                if ci: 
                                
                    grad=db(db.graduado_pregrado.ci==line[6]).select().first()                
                    if line[2]=="":
                        aux=" "
                    else:
                        aux=line[2]                
                
                    if (type(line[10]) is 'str'):
                        tomo=int(line[10])
                    else:
                        tomo=transform_roman_numeral_to_number(line[10])  
                    cadena=transform_folio(line[9])           
                    if grad:                   
                        
                        db(db.graduado_pregrado.ci==line[6]).update(nombre1=line[1],nombre2=aux,apellido1=line[3],apellido2=line[4],tomo_secretaria=tomo,fecha_graduado=line[17],folio_secretaria=cadena,numero_secretaria=line[11],pais=line[12],modalidad=line[13],carrera=line[8])
                        # print(line)
                    else:
                        
                        db.graduado_pregrado.insert(nombre1=line[1],nombre2=aux,apellido1=line[3],apellido2=line[4],ci=line[6],tomo_secretaria=tomo,fecha_graduado=line[17],folio_secretaria=cadena,numero_secretaria=line[11],pais=line[12],modalidad=line[13],carrera=line[8])
                
            pass   
        except csv.Error as e:
            raise SystemError('El fichero seleccionado no es válido.')   
    pass
    return listaTabla

def __procesar_pregrado_coma(file,cambios):
    # -*- coding: utf-8 -*-
    """
    Este método procesa los datos del archivo csv.
    Primero se carga el archivo y luego se recorre cada linea
    según el formato sugerido.

    A medida que se analiza cada linea se guarda en una lista que
    contiene  una clase Tabla donde se guarda el responsable, su
    area y una lista con sus medios. Esta lista se procesa luego
    para insertar en la base de datos y guardar los cambios con respecto
    a la base de datos anterior.
    """
    reader = __cargar(file, ",")    
    # documento = xlrd.open_workbook('./applications/prueba4o.xlsx')
   
    # carrera = documento.sheet_by_index(0)
    
    
    listaTabla = []

    try:
        for line in reader: #Ignoramos la primera fila, que indica los campos              
            try:
                ci = int(line[6]) and len(line[6]) == 11
            except:
                ci = 0
            if ci:                
                grad=db(db.graduado_pregrado.ci==line[6]).select().first()                
                if line[2]=="":
                    aux=" "
                else:
                    aux=line[2]                
                if grad:
                    db(db.graduado_pregrado.ci==line[6]).update(nombre1=line[1],nombre2=aux,apellido1=line[3],apellido2=line[6],tomo_secretaria=line[11],fecha_graduado=line[9],folio_secretaria=line[12],numero_secretaria=line[14],pais=line[15],modalidad=line[16])
                    print(line)
                else:
                    db.graduado_pregrado.insert(nombre1=line[1],nombre2=aux,apellido1=line[3],apellido2=line[4],ci=line[6],tomo_secretaria=line[11],fecha_graduado=line[9],folio_secretaria=line[12],numero_secretaria=line[14],pais=line[15],modalidad=line[16])
              
        pass   
    except csv.Error as e:
        raise SystemError('El fichero seleccionado no es válido.')   
   

    return listaTabla





def __copia_seguridad_bd():
    """
    guardo en un csv una salva de la anterior base de datos
    en caso de que necesite restaurarla
    :return:
    """
    url = os.path.join(request.folder, "static/database_save/restore.csv")
    db.export_to_csv_file(open(url, 'wb'))


def __restaurar_bd():
    """
    en caso de que necesite restaurar la base de datos, importo el csv de restauracion
    :return:
    """
    __truncate()
    url = os.path.join(request.folder, "static/database_save/restore.csv")
    db.import_from_csv_file(open(url, 'rb'), restore=True)


def __truncate():
    db.notas.truncate()
    db.estudiante.truncate()
    db.tipo_examen.truncate()
    db.asignatura.truncate()
    db.curso.truncate()
    db.fechas.truncate()
    pass


