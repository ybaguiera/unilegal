import Validators

class IS_CORRECT_CI(object):
    def __init__(self, error_message=T("Año incorrecto")):
        self.validator = Validators.Validators()
        self.error_message = error_message

    def __call__(self, value):
        error = None
        try:
            self.validator.is_valid_ci(value)
        except Exception as ex:
            error = ex
        return value, error

