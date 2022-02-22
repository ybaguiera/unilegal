import datetime
import time


class Validators:
    """Clase especializada en el cálculo de la Norma Parcial Neta"""

    def __init__(self):
        pass

    def is_valid_ci(self, value):
        try:
            int(value)
        except:
            raise SyntaxError("El valor entrado no es un número")
        if (len(str(value)) != 11) and (len(str(value)) != 6):
            raise ValueError("El valor proporcionado no es válido (en Cuba los CI solo tienen 6 u 11 dígitos)")
        # if len(str(value)) == 11:
        #     value = str(value)
        #     fecha_cumple = value[:6]
        #     format = '%y%m%d'
        #     val = 0
        #     try:
        #         val = time.strptime(fecha_cumple, format)
        #     except:
        #         raise ValueError('El CI no tiene el formato correcto (fecha incorrecta)')
        #     # (y, m, d, hh, mm, ss, t0, t1, t2) = val
        #     edad=str(datetime.date.today().year - val.tm_year)
        #     if (datetime.date.today().year - val.tm_year) < 20:
        #         raise ValueError('El CI no tiene el formato correcto (edad incorrecta) 2'+edad)
        return None
