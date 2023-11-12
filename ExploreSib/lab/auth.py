
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view


from .serializers import UsersSerializer

@api_view(['POST'])
def register(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = Users.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        return Response({'message': 'User registered successfully'}, status=201)
    return Response(serializer.errors, status=400)
