# auth/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from .serializers import UsersSerializer
@api_view(['POST'])
def register(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)    
        response = Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        response.set_cookie(key='user_id', value=user.id)  # Установка куки с user_id
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def RRegister(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Вход в систему после успешной регистрации
        # login(request, user)

        # Установка сессии в куки
        request.session.save()

        response = Response({'message': 'User registered and logged in successfully'}, status=status.HTTP_201_CREATED)
        return response
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
