from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PINOrPasswordBackend(BaseBackend):
    """
    Custom backend: authenticate with (phone + PIN) or (email/phone + password).
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 🔍 Try finding user by email or phone
            user = User.objects.filter(email=username).first() or \
                   User.objects.filter(phone_number=username).first()
            if not user:
                return None

            # ✅ Check password
            if user.check_password(password):
                return user

            # ✅ Check PIN
            if user.check_pin(password):   # 👈 Here password param = raw PIN
                return user
        except Exception:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None