from django.urls import path 
from lab import views 
from lab import views1
from lab import auth_session
from .views1 import *
urlpatterns = [
    # path('admin/', admin.site.urls),

    # API objects
    path(r'object/', views.get_objects), #список всех объектов +
    path(r'object/create/', views.create_object), # создание объекта +
    # path(r'object/<int:id>/', views1.object),
    path(r'object/<int:id>/',ObjectView.as_view() ),

    # API Exp
    path(r'expedition/', views.get_exps), #список всех экспедиций +
    path(r'expedition/update_user/', views.put_user), # изменение статуса юзером +
    path(r'expedition/<int:id>/update_mod/', views.put_mod), # изменение статуса модератором +
    path(r'expedition/update_async/', views.put_async), # изменение статуса модератором +
    # path(r'expedition/<int:id>/', views1.exp), # одна экспедиция +    
    path(r'expedition/<int:id>/', ExpView.as_view()), 
    path(r'expedition/<int:id>/delete_exp/<int:id2>', views.del_object_exp),   #удаление объекта из заявки +

    # API Exp_Obj
    path(r'Programm/<str:id>/', views.get_pro) , #получение списка  м-м +
    
    # path(r'user/', views.us),
    path('auth/register/', auth_session.register, name='register'),
    path('auth/login/', auth_session.login, name='login'),
    path('auth/', auth_session.user, name='logout'),
    path(r'auth/logout/', auth_session.logout, name='logout'),
    # path(r'login/', auth.LLogin, name='login'),
    # path(r'logout/', auth.LLogout, name='logout'),

     
    

] 