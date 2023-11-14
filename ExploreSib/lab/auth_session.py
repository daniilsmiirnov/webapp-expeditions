

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from rest_framework.decorators import api_view

from .serializers import UsersSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import Users
import jwt, datetime

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'User registered successfully',
                'data': serializer.data
                                 })
        return JsonResponse(serializer.errors, status=400)


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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'Login successfull',
            'jwt': token
        }
        return response


@api_view(['GET'])
def user(request):
    if request.method == 'GET':
        token = request.COOKIES.get('jwt')

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


@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Вы вышли из системы!'
        }
        return response


