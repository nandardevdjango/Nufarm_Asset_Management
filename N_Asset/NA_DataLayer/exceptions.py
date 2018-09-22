import re
from NA_DataLayer.common import Data, Message


class NAError(Exception):
    def __init__(self, error_code, message=None, *args, **kwargs):
        super(NAError, self).__init__(message)
        self.error_code = error_code
        self.message = message
        self.args = args
        self.kwargs = kwargs

        if not message:
            self.message = error_code


class NAErrorConstant(object):
    """
    Error Code
    """

    DATA_EXISTS = 'Data-Exist'
    DATA_HAS_REF = 'Data-Has-Ref'
    DATA_LOST = 'Data-Lost'

    UNCAUGHT_ERROR = 'Uncaught-Error'


class NAErrorHandler(object):

    @classmethod
    def handle(cls, err):
        result = None
        if err.error_code == NAErrorConstant.DATA_EXISTS:
            result = NAErrorHandler.handle_data_exists(err=err)
        elif err.error_code == NAErrorConstant.DATA_LOST:
            result = NAErrorHandler.handle_data_lost(**err.kwargs)
        elif err.error_code == NAErrorConstant.DATA_HAS_REF:
            result = cls.handle_data_hasref()

        if result:
            return result
        raise Exception('Unhandled error')

    @staticmethod
    def get_form_error_message(form_error):
        form_error = form_error.as_data()
        if isinstance(form_error, list):
            return form_error[0].message
        for k, v in form_error.items():
            return v[0].message.title()

    @staticmethod
    def retrieve_integrity_column(err):
        """
        :param err:     -- error message
        :return:        -- column name in database
        """

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
        """
        :param column:  -- column name in database
        :param model:   -- models in django
        :return:        -- field in models
        """

        if column == 'PRIMARY':
            return model._meta.pk.name
        fields_db = []
        fields_model = []
        for field_ in model._meta.fields:
            fields_db.append(field_.db_column)
            fields_model.append(field_.name)

        return fields_model[fields_db.index(column)]

    @classmethod
    def handle_data_exists(cls, err):
        """
        only for Django ORM
        :param err:     -- instance of NAError
        :return:        -- tuple of Data and Message error for user
        """

        instance = err.kwargs.get('instance')
        error_column = cls.retrieve_integrity_column(err=err.message)
        error_field = cls.retrieve_integrity_field(
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

    @staticmethod
    def handle_data_hasref():
        raise NotImplementedError

    @staticmethod
    def handle_data_lost(model, pk=None, **kwargs):
        """
        only for Django ORM
        :param model:   -- models Name
        :param pk:      -- primary key of models
        :param kwargs:  -- other lookup for filter query
        :return:        -- tuple of Data and Message error for user
        """

        return Data.Lost, Message.get_lost_info(model=model, pk=pk, **kwargs)

    @classmethod
    def handle_form_error(cls, form_error):
        result = cls.get_form_error_message(form_error)
        return Data.ValidationError, result
