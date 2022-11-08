import time
from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.authtoken.models import Token

from auth_app.serializers import RegisterSerializer, LoginSerializer


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get("phone_number")
        password = request.data.get("password")

        if username is None or password is None:
            return Response({'error': 'Please provide both phone number and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        response = Response()
        response.set_cookie(
            key="access_token",
            value=token.key,
            expires=datetime.now() + timedelta(days=1),
        )
        return response


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


@api_view(['GET'])
def check_token(request, token=None):
    if token is not None:
        try:
            Token.objects.get(key=token)
            return Response(status=HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
    return Response(status=HTTP_404_NOT_FOUND)
