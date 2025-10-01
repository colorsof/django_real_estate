import logging
from typing import Optional, Tuple
from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import Token

logger = logging.getLogger(__name__)

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that retrieves the token from a cookie.
    """

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        """
        Authenticate the request by extracting the JWT token from a cookie.
        """
        header = self.get_header(request)
        raw_token = None
        
        if header is not None:
            # If the token is provided in the Authorization header, use it
            raw_token = self.get_raw_token(header)
        elif settings.COOKIE_NAME in request.COOKIES:
            raw_token = request.COOKIES.get(settings.COOKIE_NAME)
            
        if raw_token is not None:
            try:
                validated_token = self.get_validated_token(raw_token)
                user = self.get_user(validated_token)
                return (user, validated_token)
            except TokenError as e:
                logger.warning(f"Token error: {e}")
                return None
            except Exception as e:
                logger.error(f"Authentication error: {e}")
                return None

        return None