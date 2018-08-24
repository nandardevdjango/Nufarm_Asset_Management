from django.apps import AppConfig


class NAAppConfig(AppConfig):
    name = 'app'

    def ready(self):
        from . import signals
