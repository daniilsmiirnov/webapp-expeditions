
# from .models import *
# from rest_framework.response import Response
# from .serializers import *
# from rest_framework.decorators import api_view
# from django.contrib.auth import authenticate, login, logout
# from rest_framework import status
# from .serializers import UsersSerializer


# @api_view(['POST'])
# def register(request):
#     serializer = UsersSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         login(request, user)    
#         response = Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         response.set_cookie(key='user_id', value=user.id)  # Установка куки с user_id
#         return response
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # @api_view(['POST'])
# # def custom_register(request):
# #     serializer = UsersSerializer(data=request.data)
# #     if serializer.is_valid():
# #         user = serializer.save()
# #         login(request, user)
# #         return Response({'message': 'User registered and logged in successfully'}, status=status.HTTP_201_CREATED)
# #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
    
#     user = authenticate(request, username=username, password=password)

#     if user is not None:
#         login(request, user)
#         response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#         response.set_cookie(key='user_id', value=user.id)  # Установка куки с user_id
#         return response
#     else:
#         return Response({'message': 'Invalid login'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def logout(request):
#     logout(request)
#     response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
#     response.delete_cookie('user_id')  # Удаление куки при выходе
#     return response
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from .serializers import UsersSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def LLogin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        #response.set_cookie(key='access_token', value=access_token, httponly=True)  # Установка куки с access_token
        return response
    else:
        return Response({'message': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
@csrf_exempt
@api_view(['POST'])
def LLogout(request):
    logout(request)
    response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    #response.delete_cookie('access_token')  # Удаление куки при выходе
    return response
@csrf_exempt
@api_view(['POST'])
def RRegister(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({'message': 'User registered and logged in successfully'}, status=status.HTTP_201_CREATED)
        # response.set_cookie(key='access_token', value=access_token, httponly=True)  # Установка куки с access_token
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
