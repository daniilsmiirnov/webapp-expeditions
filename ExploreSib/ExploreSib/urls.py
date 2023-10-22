"""
URL configuration for ExploreSib project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from lab import views
from lab import views1
from rest_framework import routers


router = routers.DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),

    # API objects
    path(r'object/', views.get_objects), #список всех объектов +
    path(r'object/create/', views.create_object), # создание объекта +
    path(r'object/<int:id>/', views1.object),
    # path(r'object/<int:id>/', views.get_object), # один объект +
    # path(r'object/<int:id>/post/', views.post_object) , #добавление объекта в заявку +
    # path(r'object/<int:id>/put/', views.put_object) , #обновление     объекта +
    # path(r'object/<int:id>/delete/', views.del_object),   #удаление объекта +
    
    # path(r'object/filter/', views.filter_object), # фильтр +
    # path(r'expedition/filter_exp/', views.filter_exp), # фильтр +
    # API Exp
    path(r'expedition/', views.get_exps), #список всех экспедиций +
    path(r'expedition/<int:id>/update_user/', views.put_user), # изменение статуса юзером +
    path(r'expedition/<int:id>/update_mod/', views.put_mod), # изменение статуса модератором +
    path(r'expedition/<int:id>/', views1.exp), # одна экспедиция +       
    path(r'expedition/<int:id>/delete_exp/<int:id2>', views.del_object_exp),   #удаление объекта из заявки +
    # path(r'expedition/<int:id>/', views.get_exp), # одна экспедиция +       
    # path(r'expedition/<int:id>/put/', views.put_exp) , #обновление  экспедиции +
    # path(r'expedition/<int:id>/delete/', views.del_exp), # удаление экспедиции +
    #path(r'expedition/<int:id>/delete1/', views.del_exp1), # удаление экспедиции +
    # API Exp_Obj
    path(r'Programm/<str:id>/', views.get_pro) , #получение списка  м-м +
    path(r'Programm/<str:id>/put/', views.put_pro), #обновление объекта +
    #path(r'Programm/', views.get_pros) , #получение списка  м-м +
    #path(r'Programm/<str:id>/delete/', views.del_pro), #удаление объекта +
    

]   
