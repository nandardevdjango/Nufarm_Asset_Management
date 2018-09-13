from django_mysql.models import JSONField as DefaultJSONField


class JSONField(DefaultJSONField):
    def _check_mysql_version(self):
        return []
