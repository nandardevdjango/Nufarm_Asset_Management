from django.conf import settings
from django.contrib.auth.hashers import check_password
from NA_Models.models import NAPrivilege as User


class NA_AuthBackend(object):

    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return None
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
