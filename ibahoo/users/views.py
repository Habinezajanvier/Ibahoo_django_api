from rest_framework.views import APIView
from .authentication import JWTAuthentication, generate_auth_token
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from .serializers import UserSerializers
from .models import User

# Create your views here.
@api_view(['POST'])
def register(request):
    data = request.data
    serializer = UserSerializers(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)



class AthenticatedUser(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializers(request.user)

        return Response({
            "data": serializer.data
        })


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('email or password is incorrect')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('password or email is incorrect')

    response = Response()
    token = generate_auth_token(user)
    response.data = {
        'auth_token': token
    }

    return response
