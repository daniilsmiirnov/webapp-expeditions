
from .models import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .perm import *
from rest_framework.views import APIView

class ObjectView(APIView):
    @swagger_auto_schema(
        responses={200: 'Successful response', 403: 'Доступ запрещен: Токен отсутствует'},
        operation_summary="Получение объекта по ID",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="ID"),
        ],
    )
    def get(self, request, id, format=None):
        token_head = request.headers.get('Authorization')
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            print('token',token); 
            # Далее обработка токена
        else:
            token = request.COOKIES.get('jwt')
            print('token cok',token); 
        if not token:
            return Response({'message': 'Доступ запрещен: Токен отсутствует'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Доступ запрещен: Истек срок действия токена'}, status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return Response({'message': 'Доступ запрещен: Недействительный токен'}, status=status.HTTP_403_FORBIDDEN)

        user_id = payload.get('id')
        if not user_id:
            return Response({'message': 'Доступ запрещен: Неверные данные в токене'}, status=status.HTTP_403_FORBIDDEN)

        user = Users.objects.filter(id=user_id).first()
        if not user:
            return Response({'message': 'Доступ запрещен: Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)
        """
        Возвращает объект
        """
        if not Object.objects.filter(ID_Object=id).exists():
            return Response(f"Объекта с таким id нет")
        obj = get_object_or_404(Object, ID_Object=id)
        #obj = City_Obj.objects.get(ID_Object=id)
        print(obj)
        serializer = ObjSerializer(obj)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: 'Successful response', 403: 'Доступ запрещен: Токен отсутствует'},
        operation_summary="Добавить объект в экспедицию",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="ID of the object"),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={

            },
        ),
    )
    def post(self, request, id, format=None):

        # token_head = request.headers.get('Authorization')
        # print('token',token_head);  
        # token = request.COOKIES.get('jwt')
        token_head = request.headers.get('Authorization')
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            print('token',token); 
            # Далее обработка токена
        else:
            token = request.COOKIES.get('jwt')
            print('token cok',token); 


        if not token:
            return Response({'message': 'Доступ запрещен: Токен отсутствует'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Доступ запрещен: Истек срок действия токена'}, status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return Response({'message': 'Доступ запрещен: Недействительный токен'}, status=status.HTTP_403_FORBIDDEN)

        user_id = payload.get('id')
        if not user_id:
            return Response({'message': 'Доступ запрещен: Неверные данные в токене'}, status=status.HTTP_403_FORBIDDEN)

        user = Users.objects.filter(id=user_id).first()
        
        if not user:
            return Response({'message': 'Доступ запрещен: Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)
        """
        Добавляет объект в заявку 
        """

        if not Object.objects.filter(ID_Object=id).exists():
            return Response(f"Объекта с таким id нет")
        obj = Object.objects.get(ID_Object = id)
        print('ob', obj)
        exp = Expedition.objects.filter(Status='in', ID_Creator=user).last()
        
        print('exp',exp)
        if exp is None:
            exp = Expedition.objects.create(ID_Creator = user)
        print('exp',exp)
        exp.Objects.add(obj)
        exp.save()

        serializer = ExpSerializer(exp)
        return Response(serializer.data)
    @swagger_auto_schema(
        responses={200: 'Successful response', 400: 'Bad request'},
        operation_summary="Update object",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="ID of the object"),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={

            },
        ),
    )
    def put(self, request, id, format=None):
        token_head = request.headers.get('Authorization')
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            print('token',token); 
            # Далее обработка токена
        else:
            token = request.COOKIES.get('jwt')
            print('token cok',token); 
        if not token:
            return Response({'message': 'Доступ запрещен: Токен отсутствует'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Доступ запрещен: Истек срок действия токена'}, status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return Response({'message': 'Доступ запрещен: Недействительный токен'}, status=status.HTTP_403_FORBIDDEN)

        user_id = payload.get('id')
        if not user_id:
            return Response({'message': 'Доступ запрещен: Неверные данные в токене'}, status=status.HTTP_403_FORBIDDEN)

        user = Users.objects.filter(id=user_id, Is_Super=True).first()
        if not user:
            return Response({'message': 'Доступ запрещен: Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)
        """
        Обновляет объект
        """
        obj = get_object_or_404(Object, ID_Object=id)
        #print('hi',obj)
        serializer = ObjSerializer(obj,data=request.data)
        print('se',serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        responses={204: 'Object deleted successfully', 403: 'Доступ запрещен: Токен отсутствует'},
        operation_summary="Delete object",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="ID of the object"),
        ],
    )
    def delete(self, request, id, format=None):
        token_head = request.headers.get('Authorization')
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            print('token',token); 
            # Далее обработка токена
        else:
            token = request.COOKIES.get('jwt')
            print('token cok',token); 
        if not token:
            return Response({'message': 'Доступ запрещен: Токен отсутствует'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Доступ запрещен: Истек срок действия токена'}, status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return Response({'message': 'Доступ запрещен: Недействительный токен'}, status=status.HTTP_403_FORBIDDEN)

        user_id = payload.get('id')
        if not user_id:
            return Response({'message': 'Доступ запрещен: Неверные данные в токене'}, status=status.HTTP_403_FORBIDDEN)

        user = Users.objects.filter(id=user_id, Is_Super=True).first()
        if not user:
            return Response({'message': 'Доступ запрещен: Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)
        """
        Удаляет объект
        """
        obj = get_object_or_404(Object, ID_Object=id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
        
@swagger_auto_schema(
    methods=['GET'],
    operation_summary='Возвращает объект',
    responses={
        200: ObjSerializer,
        404: 'Объекта с таким id нет'
    }
)
@swagger_auto_schema(
    methods=['PUT'],
    operation_summary='Обновляет объект',
    request_body=ObjSerializer,
    responses={
        200: ObjSerializer,
        400: 'Ошибка при обновлении объекта'
    }
)
@swagger_auto_schema(
    methods=['POST'],
    operation_summary='Добавляет объект в заявку',
    responses={
        200: ExpSerializer,  # Или ваш сериализатор Expedition, если это он
        404: 'Объекта с таким id нет'
    }
)
@swagger_auto_schema(
    methods=['DELETE'],
    operation_summary='Удаляет объект',
    responses={
        204: 'Объект успешно удален'
    }
)
@api_view(['Get', 'Post', 'Delete','Put'])

def object(request,id,format=None):
    """
    Возвращает объект
    """
    if request.method == 'GET':
        if not Object.objects.filter(ID_Object=id).exists():
            return Response(f"Объекта с таким id нет")
        obj = get_object_or_404(Object, ID_Object=id)
        #obj = City_Obj.objects.get(ID_Object=id)
        print(obj)
        serializer = ObjSerializer(obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        
        """
        Обновляет объект
        """
        obj = get_object_or_404(Object, ID_Object=id)
        #print('hi',obj)
        serializer = ObjSerializer(obj,data=request.data)
        print('se',serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        """
        Добавляет объект в заявку 
        """

        if not Object.objects.filter(ID_Object=id).exists():
            return Response(f"Объекта с таким id нет")
        obj = Object.objects.get(ID_Object = id)
        print('ob', obj)
        exp = Expedition.objects.filter(Status='in').last()
        print('exp',exp)
        if exp is None:
            exp = Expedition.objects.create()
        print('exp',exp)
        exp.Objects.add(obj)
        exp.save()

        serializer = ExpSerializer(exp)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        """
        Удаляет объект
        """
        obj = get_object_or_404(Object, ID_Object=id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return HttpResponse('error')    
    
class ExpView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="ID of the expedition"),
        ],
        operation_summary="Get expedition",
        responses={200: 'Successful response', 404: 'Expedition not found'}
    )
    def get(self, request, id, format=None):
        token_head = request.headers.get('Authorization')
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            print('token',token); 
            # Далее обработка токена
        else:
            token = request.COOKIES.get('jwt')
            print('token cok',token); 
        if not token:
            return Response({'message': 'Доступ запрещен: Токен отсутствует'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Доступ запрещен: Истек срок действия токена'}, status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return Response({'message': 'Доступ запрещен: Недействительный токен'}, status=status.HTTP_403_FORBIDDEN)

        user_id = payload.get('id')
        if not user_id:
            return Response({'message': 'Доступ запрещен: Неверные данные в токене'}, status=status.HTTP_403_FORBIDDEN)

        user = Users.objects.filter(id=user_id).first()
        if not user:
            return Response({'message': 'Доступ запрещен: Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)
        """
        Возвращает экспедицию
        """
        try:
            obj = Expedition.objects.get(ID_Expedition=id, ID_Creator=user)
        except Expedition.DoesNotExist:
            return Response({'message': 'Доступ запрещен: Нет доступа к этой заявке'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ExpSerializer(obj)
        return Response(serializer.data)

    @swagger_auto_schema(

        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="ID of the expedition"),
        ],
        operation_summary="Update expedition",
         request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={

            },),
        responses={200: 'Successful response', 400: 'Bad request'}
    )
    def put(self, request, id, format=None):
        token_head = request.headers.get('Authorization')
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            print('token',token); 
            # Далее обработка токена
        else:
            token = request.COOKIES.get('jwt')
            print('token cok',token); 
        if not token:
            return Response({'message': 'Доступ запрещен: Токен отсутствует'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Доступ запрещен: Истек срок действия токена'}, status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return Response({'message': 'Доступ запрещен: Недействительный токен'}, status=status.HTTP_403_FORBIDDEN)

        user_id = payload.get('id')
        if not user_id:
            return Response({'message': 'Доступ запрещен: Неверные данные в токене'}, status=status.HTTP_403_FORBIDDEN)

        user = Users.objects.filter(id=user_id).first()
        if not user:
            return Response({'message': 'Доступ запрещен: Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)
        """
        Обновляет экспедицию
        """
        try:
            obj = Expedition.objects.get(ID_Expedition=id, ID_Creator=user)
        except Expedition.DoesNotExist:
            return Response({'message': 'Доступ запрещен: Нет доступа к этой заявке'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ExpSerializer(obj, data=request.data)
        print('puuut',request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="ID of the expedition"),
        ],
        operation_summary="Delete expedition",
        responses={200: 'Successful response', 404: 'Expedition not found'}
    )
    def delete(self, request, id, format=None):
        token_head = request.headers.get('Authorization')
        if token_head:
            token = token_head.split(' ')[1]  # Получение токена из заголовка
            print('token',token); 
            # Далее обработка токена
        else:
            token = request.COOKIES.get('jwt')
            print('token cok',token); 
        if not token:
            return Response({'message': 'Доступ запрещен: Токен отсутствует'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Доступ запрещен: Истек срок действия токена'}, status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return Response({'message': 'Доступ запрещен: Недействительный токен'}, status=status.HTTP_403_FORBIDDEN)

        user_id = payload.get('id')
        if not user_id:
            return Response({'message': 'Доступ запрещен: Неверные данные в токене'}, status=status.HTTP_403_FORBIDDEN)

        user = Users.objects.filter(id=user_id).first()
        if not user:
            return Response({'message': 'Доступ запрещен: Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)
        """
        Удаляет экспедицию
        """
        try:
            obj = Expedition.objects.get(ID_Expedition=id, ID_Creator=user)
        except Expedition.DoesNotExist:
            return Response({'message': 'Доступ запрещен: Нет доступа к этой заявке'}, status=status.HTTP_403_FORBIDDEN)

        obj.Status = 'de'
        obj.save()

        # exp = Expedition.objects.all()
        serializer = ExpSerializer(obj, many=False)
        return Response(serializer.data)    
    
@api_view(['Get', 'Post', 'Delete','Put'])
def exp(request,id,format=None):
    
    if request.method == 'GET':
        """
        Возвращает экспедицию
        """
        if request.method == 'GET':
            obj = get_object_or_404(Expedition, ID_Expedition=id)
            #obj = City_Obj.objects.get(ID_Object=id)
            print(obj)
            serializer = ExpSerializer(obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        """
        Обновляет экспедицию
        """
        obj = get_object_or_404(Expedition, ID_Expedition=id)
        print('ob',obj)
        serializer = ExpSerializer(obj,data=request.data)
        print('se',serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        return HttpResponse('error no post') 
    elif request.method == 'DELETE':
        """
        Удаляет экспедицию
        """
    obj = get_object_or_404(Expedition, ID_Expedition=id)
    print('ob', obj)
    obj.Status = 'de'
    print(obj.Status)
    obj.save()

    exp = Expedition.objects.all()
    serializer = ExpSerializer(exp, many=True)
    return Response(serializer.data)
    #     """
    #     Удаляет экспедицию
    #     """
    #     obj = get_object_or_404(Expedition, ID_Expedition=id)
    #     print('ob',obj)
    #     obj.delete() 

    #     exp = Expedition.objects.all()
    #     serializer = ExpSerializer(exp, many=True)
    #     return Response(serializer.data)
    # else:
    #     return HttpResponse('error')    
