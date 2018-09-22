from datetime import datetime

from django.utils.functional import cached_property
from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession, BaseSessionManager
from django.db import models


class NASessionManager(BaseSessionManager):
    use_in_migrations = True


class NASession(AbstractBaseSession):
    user_id = models.IntegerField(null=True, db_index=True, db_column='user_id')
    objects = NASessionManager()

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

    @cached_property
    def is_expired(self):
        return self.expire_date < datetime.now()

    class Meta(AbstractBaseSession.Meta):
        db_table = 'n_a_session'
        managed = True


class SessionStore(DBStore):

    @classmethod
    def get_model_class(cls):
        return NASession

    def create_model_instance(self, data):
        obj = super(SessionStore, self).create_model_instance(data)
        try:
            user_id = int(data.get('_auth_user_id'))
        except (ValueError, TypeError):
            user_id = None
        obj.user_id = user_id
        return obj

    @classmethod
    def encode_session(cls, data):
        return cls().encode(session_dict=data)
