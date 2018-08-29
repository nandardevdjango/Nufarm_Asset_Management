import re


class NAErrorConstant(object):

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
            return err.split(' ')[-1]

    @staticmethod
    def retrieve_integrity_field(column, model):
        fields_db = []
        fields_model = []
        for field_ in model._meta.fields:
            fields_db.append(field_.db_column)
            fields_model.append(field_.name)

        return fields_model[fields_db.index(column)]