from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
from .perm import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt, datetime
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
import requests
@api_view(['Get'])
@isModerator
# @permission_classes([IsAuthenticated])
def us(request, format=None):

    users = Users.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)   







@swagger_auto_schema(
    method='GET',
    operation_summary='Возвращает список объектов',
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description='Поле Имя географического объекта для фильтрации', type=openapi.TYPE_STRING),
        openapi.Parameter('year', openapi.IN_QUERY, description='Поле Год создания для фильтрации', type=openapi.TYPE_INTEGER),
        openapi.Parameter('opener', openapi.IN_QUERY, description='Поле Открыватель для фильтрации', type=openapi.TYPE_STRING),
    ],
    responses={200: ObjSerializer(many=True)}
)
@api_view(['GET'])
def get_objects(request, format=None):
    """
    Возвращает список объектов
    """
    Field1 = request.GET.get('name')
    Field2 = request.GET.get('year')
    Field3 = request.GET.get('opener')

    data = Object.objects.filter(Status='ope')

    if Field1:
        data = data.filter(Name_Obj=Field1)
    if Field2:
        data = data.filter(Year=Field2)
    if Field3:
        data = data.filter(Opener=Field3)

    serializer = ObjSerializer(data, many=True)
    return Response(serializer.data)

# @api_view(['Get'])
# def get_objects(request, format=None):
#     """
#     Возвращает список объектов
#     """
#     cache.set('mykey', '123143242', timeout=None)
#     value = cache.get('mykey')
#     print(value)
#     # print('Done!!!!!')
#     Field1= request.GET.get('name')
#     Field2 = request.GET.get('year')
#     Field3 = request.GET.get('opener')
#     if  Field1 :
#         data = Object.objects.filter(Name_Obj=Field1) & Object.objects.filter(Status='ope')
#         serializer = ObjSerializer(data,many=True)
#         return Response(serializer.data)
#     if Field2 :
#         data = Object.objects.filter(Year=Field2) & Object.objects.filter(Status='ope')
#         serializer = ObjSerializer(data,many=True)
#         return Response(serializer.data)
#     if Field3:
#         data = Object.objects.filter(Opener=Field3) & Object.objects.filter(Status='ope')
#         serializer = ObjSerializer(data,many=True)
#         return Response(serializer.data)
#     else:
#         objs = Object.objects.all()
#         o = objs;
#         print(o.values())
#         serializer = ObjSerializer(objs, many=True)
#         print(serializer.data)
#         return Response(serializer.data)




@swagger_auto_schema(
    method='POST',
    operation_summary='Добавляет объект',
    request_body=ObjSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description='Объект успешно добавлен',
            schema=ObjSerializer
        ),
        status.HTTP_400_BAD_REQUEST: 'Ошибка при добавлении объекта'
    }
)
@api_view(['Post'])
@isModerator
def create_object(request,format=None):
    """
    Добавляет объект
    """
    serializer = ObjSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#########################################

@api_view(['Get'])

def get_exps(request, format=None):
    """
    Возвращает список экспедиций
    """
    Field1= request.GET.get('status')
    Date1 = request.GET.get('DateFormStart')
    Date2 = request.GET.get('DateFormEnd')
    if  Field1:
        data = Expedition.objects.filter(Status=Field1)
        serializer = ExpSerializer(data,many=True)
        da= data
        print(da.values())
        return Response(serializer.data)
    if Date2 and Date1:
        date1 = datetime.strptime(Date1, "%Y-%m-%d %H:%M:%S")
        date2 = datetime.strptime(Date2, "%Y-%m-%d %H:%M:%S")
        objects = Expedition.objects.all()
        set = Expedition.objects.none()
        for obj in objects:
                if (obj.DateEnd<date2 and obj.DateStart>date1):
                    set |= Expedition.objects.filter(ID_Expedition=obj.ID_Expedition)
                    s=set
                    print(s.values())
        n=set
        print('---------',n.values())
        serializer = ExpSerializer(set, many=True)
        return Response(serializer.data)
    if Date2:
        date2 = datetime.strptime(Date2, "%Y-%m-%d %H:%M:%S")
        objects = Expedition.objects.all()
        set = Expedition.objects.none()
        for obj in objects:
                if obj.DateEnd<date2:
                    set |= Expedition.objects.filter(ID_Expedition=obj.ID_Expedition)
                    s=set
                    print(s.values())
        n=set
        print('---------',n.values())
        serializer = ExpSerializer(set, many=True)
        return Response(serializer.data)
    if Date1:
        date1 = datetime.strptime(Date1, "%Y-%m-%d %H:%M:%S")
        objects = Expedition.objects.all()
        set = Expedition.objects.none()
        for obj in objects:
                if obj.DateStart>date1:
                    set |= Expedition.objects.filter(ID_Expedition=obj.ID_Expedition)
                    s=set
                    print(s.values())
        n=set
        print('---------',n.values())
        serializer = ExpSerializer(set, many=True)
        return Response(serializer.data)
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
    if user.Is_Super:
        status=["ca","en","wo","de"]
        objs = Expedition.objects.filter(Status__in=status)
        serializer = ExpSerializer(objs, many=True)
        return Response(serializer.data)
    if not user.Is_Super:
        objs = Expedition.objects.filter(ID_Creator=user)
        serializer = ExpSerializer(objs, many=True)
        return Response(serializer.data)
    return Response({'message': 'Экспедиций нет'})
@api_view(['Get'])
def get_exp(request,id,format=None):
    """
    Возвращает экспедицию
    """
    if request.method == 'GET':
        obj = get_object_or_404(Expedition, ID_Expedition=id)
        #obj = City_Obj.objects.get(ID_Object=id)
        print(obj)
        serializer = ExpSerializer(obj)
    return Response(serializer.data)

@api_view(['Get'])
# @isAuth
def put_user(request,format=None):
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

    try:
        exp = Expedition.objects.get(ID_Creator=user, Status='in')
    except Expedition.DoesNotExist:
        return Response({'message': 'У вас нет экспедиции.'})
    
    exp.Status='wo'
    exp.DateEnd=timezone.now()
    try:
        exp_id = exp.ID_Expedition  # Получаем идентификатор экспедиции
        token_go = '4321'  # Ваш константный ключ
        url = 'http://localhost:8088/archive'


        data = {
            'exp_id': exp_id,
            'token': token_go
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            print("done success")
            exp.Archive = "Запрошена справка в архиве!"
        else:
            exp.Archive = "Не удалось запросить справку из архива!"
            
    except requests.exceptions.RequestException as e:
        print('error:', e)
    exp.save()
    
    serializer = ExpSerializer(exp)
        #if serializer.is_valid():
         #   serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
def put_async(request, format=None):
    """
    Обновляет данные экспедиции асинхронно
    """
    expected_token = '4321'

    # Проверка метода запроса (должен быть PUT)
    if request.method != 'PUT':
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exp_id = request.data.get('exp_id')
    result = request.data.get('result')
    token = request.data.get('token')

    # Проверка наличия всех необходимых параметров
    if not exp_id or not result or not token:
        return Response({'error': 'Отсутствуют необходимые данные'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка токена
    if token != expected_token:
        return Response({'error': 'Недопустимый токен'}, status=status.HTTP_403_FORBIDDEN)

    try:
        exp = Expedition.objects.get(ID_Expedition=exp_id)
    except Expedition.DoesNotExist:
        return Response({'error': 'Экспедиция не найдена'}, status=status.HTTP_404_NOT_FOUND)

    exp.Archive = result
    exp.save()
    serializer = ExpSerializer(exp)
    print(serializer.data)
    return Response(serializer.data)
    
    
@swagger_auto_schema(
    method='put',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="ID of the expedition"),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'Status': openapi.Schema(type=openapi.TYPE_STRING, description='New status (ca or en)'),
        },
        required=['Status']
    ),
    responses={
        200: openapi.Response(description='Successful response'),
        403: openapi.Response(description='Access denied'),
        # Другие возможные коды ответа
    },
    operation_summary="Update expedition status",
)
@api_view(['Put'])
@isModerator
def put_mod(request,id,format=None):
    token_head = request.headers.get('Authorization')
    if token_head:
        token = token_head.split(' ')[1]  # Получение токена из заголовка
        print('token',token); 
            # Далее обработка токена
    else:
        token = request.COOKIES.get('jwt')
        print('token cok',token); 
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user_id = payload.get('id')
    user = Users.objects.filter(id=user_id, Is_Super=True).first()
    exp = Expedition.objects.get(ID_Expedition=id)
    status = request.data["Status"]
    print(status)
    if exp.Status in ["ca","en","in"]:
        if status in ["ca","en"]:
            exp.Status=status
            exp.DateApproving=timezone.now()
            exp.DateEnd=timezone.now()
            exp.Moderator=user
            exp.save()
            serializer = ExpSerializer(exp)
        # if serializer.is_valid():
            #    serializer.save()
            return Response(serializer.data) 
    else:
        return Response("Заявка недоступна для изменения статуса!")

@api_view(['Put'])
def put_exp(request,id,format=None):
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

@api_view(['Put'])
def put_exp(request,id,format=None):
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

@api_view(['Delete'])
def del_exp1(request, id, format=None):    
    """
    Удаляет экспедицию
    """
    obj = get_object_or_404(Expedition, ID_Expedition=id)
    print('ob',obj)
    obj.delete() 

    # exp = Expedition.objects.all()
    # serializer = ExpSerializer(exp, many=True)
    return Response()
@api_view(['Delete'])
@isAuth
def del_object_exp(request, id,id2, format=None):    
    """
    Удаляет объект из экспедиции
    """
    exp = Expedition.objects.get(ID_Expedition=id)
    pro = Programm.objects.get(ID_Exp=id, ID_Obj=id2)
    print('pro',pro)
    pro.delete()
    
    print('exp')
    #print(Object.objects.get(ID_Object=id2))
    #exp.Objects.remove(Object.objects.get(ID_Object=id2))
    
    #exp.save()
    
    serializer = ExpSerializer(exp)
    return Response(serializer.data)

@api_view(['Delete'])
def del_exp(request, id, format=None):    
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









#####################################################

@api_view(['Get'])
def get_pros(request, format=None):
 
    objs = Programm.objects.all()
    
    pr= objs
    
    print('ob',pr.values())
    serializer = objSerializer(objs, many=True)
    print(serializer)
    return Response(serializer.data)

@api_view(['Get'])
def get_pro(request,id, format=None):
 
    print('id',id[0],id[1])
    obj = get_object_or_404(Programm, ID_Exp=id[0], ID_Obj=id[1])
    pr= obj
    
    print('ob',pr)
    serializer = objSerializer(obj)
    print(serializer)
    return Response(serializer.data)    


@api_view(['Put'])
def put_pro(request,id,format=None):
    print('id',id[0],id[1])
    
    obj = get_object_or_404(Programm, ID_Exp=id[0], ID_Obj=id[1])
    print('obj',obj)
    #print(request.data)
    serializer = objSerializer(obj,data=request.data)
    print('se',serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['Delete'])

def del_pro(request, id, format=None):    
    obj = get_object_or_404(Programm, ID_Exp=id[0], ID_Obj=id[1])
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Get'])
def filter_exp(request,format=None):
    """
    фильтр объекта
    """
    Field1= request.GET.get('status')

    if  Field1 :
        data = Expedition.objects.filter(Status=Field1)
        serializer = ExpSerializer(data,many=True)
        da= data
        print(da.values())
        return Response(serializer.data)


    else:
        return Response('Фильтр неверный')


