from lab.models import *
from rest_framework import serializers


class ObjSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = City_Obj
        fields = '__all__'
        
