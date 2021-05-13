from .models import User
import jwt
import datetime
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

def generate_auth_token(user):
    payload = {
        'user_id': user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('auth_token')
        if not token: 
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Invalid Token")

        user = User.objects.filter(id=payload['user_id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed("No user found")

        return (user, None)