# accounts/auth_backends.py
from django.contrib.auth.backends import BaseBackend
from accounts.models.global_user import GlobalUser

# accounts/auth_backends.py
from django.contrib.auth.backends import BaseBackend
from accounts.models.global_user import GlobalUser

class GlobalUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = GlobalUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except GlobalUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return GlobalUser.objects.get(pk=user_id)
        except GlobalUser.DoesNotExist:
            return None
