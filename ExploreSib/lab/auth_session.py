

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .serializers import *
from rest_framework.decorators import api_view
from .perm import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import Users
import jwt, datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            # Добавьте другие поля, если необходимо
        },
    ),
    responses={
        200: openapi.Response(
            description='User registered successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT),  # Замените на реальные поля пользователя
                },
            ),
        ),
        400: 'Invalid input',  # Пример для ошибочного запроса
    },
)
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'User registered successfully',
                'data': serializer.data
                                 })
        return JsonResponse(serializer.errors, status=400)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password']
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'jwt': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        400: "Bad Request: Invalid input data",
        401: "Unauthorized: Invalid username or password",
        # Define other possible response codes and schemas here
    }
)
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        # user = authenticate(request,username=username, password=password)
        user = Users.objects.filter(username=username).first()

        if user is None:
            return JsonResponse({'message': 'Пользователя не существует!'})

        if not user.check_password(password):
            return JsonResponse({'message': 'Пароль неверный!'})

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        # response.set_cookie(key='jwt', value=token)
        response.set_cookie(key='jwt', value=token, httponly=True, secure=True)
        serializer = UserSerializer(user)
        response.data = {
            'message': 'Успешная авторизация!',
            'jwt': token,
            'user':serializer.data
        }
        return response

@api_view(['GET'])
def user(request):
    if request.method == 'GET':
        token_head = request.headers.get('Authorization')
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            print('token',token); 
            # Далее обработка токена
        else:
            token = request.COOKIES.get('jwt')
            print('token cok',token); 
            

        if not token:
            raise AuthenticationFailed('Аутентификация не пройдена!')
        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Аутентификация не пройдена!')

        user = Users.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return JsonResponse({'message': 'Аутентификация успешна',
                             'user':serializer.data
                             })


# @api_view(['POST'])
# @isAuth
# def logout(request):
#     if request.method == 'POST':
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data = {
#             'message': 'Вы вышли из системы!'
#         }
#         return response
from django_redis import get_redis_connection

@api_view(['POST'])
@isAuth
def logout(request):
    if request.method == 'POST':
        token_head = request.headers.get('Authorization')
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
        else:
            token = request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({'message': 'Токен не найден'})

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Токен недействителен'})

        user_id = payload.get('id')
        user_token = f"token:{user_id}:{token}"

        # Сохранение токена в Redis при logout
        redis_connection = get_redis_connection("default")
        redis_connection.set(user_token, 'used', ex=10000)  # Или установите необходимое время жизни токена

        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'Вы вышли из системы!'}
        return response



