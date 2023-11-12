from lab.models import *
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Users
        fields = '__all__'
class ObjSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Object
        fields = '__all__'
        
        
class ExpSerializer(serializers.ModelSerializer):
    class Meta:
        #obj = ObjSerializer(read_only=True)
        # Модель, которую мы сериализуем
        model = Expedition
        fields ='__all__'
        depth = 1
class ProgrammSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programm
        fields =  ['ID_Exp', "ID_Obj", "Number"]
        
class objSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programm
        fields =  ["ID_Obj",'ID_Exp', "Number"]
 
