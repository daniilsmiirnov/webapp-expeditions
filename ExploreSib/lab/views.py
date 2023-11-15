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

from django.conf import settings
from django.core.cache import cache

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
@api_view(['Get'])
def get_objects(request, format=None):
    """
    Возвращает список объектов
    """
    cache.set('mykey', '123143242', timeout=None)
    value = cache.get('mykey')
    print(value)
    # print('Done!!!!!')
    Field1= request.GET.get('name')
    Field2 = request.GET.get('year')
    Field3 = request.GET.get('opener')
    if  Field1 :
        data = Object.objects.filter(Name_Obj=Field1) & Object.objects.filter(Status='ope')
        serializer = ObjSerializer(data,many=True)
        return Response(serializer.data)
    if Field2 :
        data = Object.objects.filter(Year=Field2) & Object.objects.filter(Status='ope')
        serializer = ObjSerializer(data,many=True)
        return Response(serializer.data)
    if Field3:
        data = Object.objects.filter(Opener=Field3) & Object.objects.filter(Status='ope')
        serializer = ObjSerializer(data,many=True)
        return Response(serializer.data)
    else:
        objs = Object.objects.all()
        o = objs;
        print(o.values())
        serializer = ObjSerializer(objs, many=True)
        print(serializer.data)
        return Response(serializer.data)




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
@isModerator
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


    objs = Expedition.objects.all()
    print(objs)
    serializer = ExpSerializer(objs, many=True)
    return Response(serializer.data)

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

@api_view(['Put'])
@isAuth
def put_user(request,id,format=None):
    ID_User=1
    exp = Expedition.objects.get(ID_Expedition=id)
    print (exp.ID_Creator.ID_User)
    if exp.ID_Creator.ID_User!=ID_User:
        return Response('У вас нет доступа к этой заявке')
    status = request.data["Status"]
    print (status)
    if status in ["wo","de"]:
        exp.Status=status
        exp.save()
        serializer = ExpSerializer(exp)
        #if serializer.is_valid():
         #   serializer.save()
        return Response(serializer.data)
    
    else:
        return Response("доступ запрещен!")
    
@api_view(['Put'])
@isModerator
def put_mod(request,id,format=None):
    exp = Expedition.objects.get(ID_Expedition=id)
    status = request.data["Status"]
    print (status)
    if status in ["de","ca","en"]:
        exp.Status=status
        exp.save()
        serializer = ExpSerializer(exp)
       # if serializer.is_valid():
        #    serializer.save()
        return Response(serializer.data) 
    else:
        return Response("доступ запрещен!")
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


