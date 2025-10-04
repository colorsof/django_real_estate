import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

logger = logging.getLogger(__name__) 

def set_auth_cookies(
    response: Response, access_token: str, refresh_token: Optional[str] = None
    ) -> None:  
    access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
    cookie_settings = {
        'httponly': settings.COOKIE_HTTPONLY,
        'secure': settings.COOKIE_SECURE,
        'samesite': settings.COOKIE_SAMESITE,
        'path': settings.COOKIE_PATH,
        'max_age': access_token_lifetime,
    }

    # Set access token cookie
    response.set_cookie("access", access_token, **cookie_settings)

    # Set refresh token cookie if provided
    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings['max_age'] = refresh_token_lifetime
        response.set_cookie(
            key='refresh',
            value=refresh_token,
            **refresh_cookie_settings
        )
        
    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings['httponly'] = False
    response.set_cookie(
        key='logged_in',
        value='true',
        **logged_in_cookie_settings
    )   
    
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT tokens and set them in HttpOnly cookies.
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        token_res = super().post(request, *args, **kwargs)


        if token_res.status_code == status.HTTP_200_OK:
            access_token = token_res.data.get('access')
            refresh_token = token_res.data.get('refresh')
            
            if access_token and refresh_token:
                set_auth_cookies(
                    token_res, 
                    access_token=access_token, 
                    refresh_token=refresh_token
                    )
                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)
                    
                token_res.data["message"] = "Login successful"
            else:
                token_res.data["message"] = "Login failed"
                logger.error("Access or refresh token missing in response data. ")

        return token_res
    
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to refresh JWT access token and set it in HttpOnly cookies.
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            request.data['refresh'] = refresh_token
            
        refresh_res = super().post(request, *args, **kwargs)
        
        
        if refresh_res.status_code == status.HTTP_200_OK:
            access_token = refresh_res.data.get('access')
            refresh_token = refresh_res.data.get('refresh')

            if access_token and refresh_token:
                set_auth_cookies(
                    refresh_res,
                    access_token=access_token,
                    refresh_token=refresh_token
                )
                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)

                refresh_res.data["message"] = "Access token refresh successful"
            else:
                refresh_res.data["message"] = (
                    "Access or refresh tokens missing in response data."
                )
                logger.error("Access or refresh token missing in response data.")

        return refresh_res
        
class CustomProviderAuthView(ProviderAuthView):
    """
    Custom view to handle social authentication and set JWT tokens in HttpOnly cookies.
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        provider_res = super().post(request, *args, **kwargs)

        if provider_res.status_code == status.HTTP_201_CREATED:
            access_token = provider_res.data.get('access')
            refresh_token = provider_res.data.get('refresh')

            if access_token and refresh_token:
                set_auth_cookies(
                    provider_res,
                    access_token=access_token,
                    refresh_token=refresh_token
                )
                provider_res.data.pop("access", None)
                provider_res.data.pop("refresh", None)

                provider_res.data["message"] = "Social login successful"
            else:
                provider_res.data["message"] = "Social login failed"
                logger.error("Access or refresh token missing in provider response data.")

        return provider_res
        
class LogoutView(APIView):
    """
    View to handle user logout by clearing authentication cookies.
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)

        # Clear authentication cookies
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")

        return response