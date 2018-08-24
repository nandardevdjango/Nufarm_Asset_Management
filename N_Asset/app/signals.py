from django.dispatch import Signal

logevent = Signal(providing_args=['models', 'activity', 'user', 'data'])
