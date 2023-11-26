from lab.models import *
from rest_framework import serializers

# class UsersSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = Users
#         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'Is_Super','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'Is_Super']

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            Is_Super=validated_data.get('Is_Super', False)
        )
        return user
      
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
 
