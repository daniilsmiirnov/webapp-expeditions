
from .models import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
from django.http import HttpResponse



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
        print('ob',obj)
        obj.delete() 

        exp = Expedition.objects.all()
        serializer = ExpSerializer(exp, many=True)
        return Response(serializer.data)
    else:
        return HttpResponse('error')    
