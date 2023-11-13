

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .serializers import UsersSerializer

@csrf_exempt
@api_view(['POST'])
def RRegister(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse({'message': 'User registered successfully'})
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['POST'])
def LLogin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'message': 'Invalid login credentials'}, status=401)

@csrf_exempt
@api_view(['POST'])
def LLogout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})
