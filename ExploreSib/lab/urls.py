from django.urls import path 
from lab import views 
from lab import views1
from lab import auth

urlpatterns = [
    # path('admin/', admin.site.urls),

    # API objects
    path(r'object/', views.get_objects), #список всех объектов +
    path(r'object/create/', views.create_object), # создание объекта +
    path(r'object/<int:id>/', views1.object),

    # API Exp
    path(r'expedition/', views.get_exps), #список всех экспедиций +
    path(r'expedition/<int:id>/update_user/', views.put_user), # изменение статуса юзером +
    path(r'expedition/<int:id>/update_mod/', views.put_mod), # изменение статуса модератором +
    path(r'expedition/<int:id>/', views1.exp), # одна экспедиция +       
    path(r'expedition/<int:id>/delete_exp/<int:id2>', views.del_object_exp),   #удаление объекта из заявки +

    # API Exp_Obj
    path(r'Programm/<str:id>/', views.get_pro) , #получение списка  м-м +
    
    path(r'user/', views.us),
    path(r'register/', auth.register),
     
    

] 