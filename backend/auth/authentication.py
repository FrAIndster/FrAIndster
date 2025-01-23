from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
from .models import User
import jwt

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        try:
            # Get the token
            token = auth_header.split(' ')[1]
            
            # Decode token
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
            
            # Get user
            user = User.objects.get(id=payload['user_id'])
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return None
            
        try:
            user = User.objects.get(api_key=api_key)
            return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid API key') 