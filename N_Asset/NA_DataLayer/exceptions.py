import re
from NA_DataLayer.common import Data, Message


class NAError(Exception):
    def __init__(self, error_code, message, *args, **kwargs):
        super(NAError, self).__init__(message)
        self.error_code = error_code
        self.message = message
        self.args = args
        self.kwargs = kwargs


class NAErrorConstant(object):
    """
    Error Code
    """

    DATA_EXISTS = 'Data-Exist'
    DATA_HAS_REF = 'Data-Has-Ref'


class NAErrorHandler(object):
    @staticmethod
    def get_form_error_message(form_error):
        form_error = form_error.as_data()
        if isinstance(form_error, list):
            return form_error[0].message
        for k, v in form_error.items():
            return v[0].message

    @staticmethod
    def retrieve_integrity_column(err):
        err = err.args[1]
        if re.match(r'Duplicate', err):
            result = err.split(' ')[-1]
            if "'" in result:
                result = result.replace("'", '')
            elif '"' in result:
                result = result.replace('"', '')
            return result

    @staticmethod
    def retrieve_integrity_field(column, model):
        if column == 'PRIMARY':
            return model._meta.pk.name
        fields_db = []
        fields_model = []
        for field_ in model._meta.fields:
            fields_db.append(field_.db_column)
            fields_model.append(field_.name)

        return fields_model[fields_db.index(column)]

    @staticmethod
    def handle_data_exists(err):
        instance = err.kwargs.get('instance')
        error_column = NAErrorHandler.retrieve_integrity_column(err=err.message)
        error_field = NAErrorHandler.retrieve_integrity_field(
            column=error_column,
            model=instance._meta.model
        )
        field_display = instance.log_display.get(error_field)
        data = (Data.Exists, Message.get_specific_exists(
            table=instance._meta.model.FORM_NAME,
            column=field_display,
            data=getattr(instance, error_field)
        ))
        return data