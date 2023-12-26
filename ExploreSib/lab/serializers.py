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
    # user_id = serializers.IntegerField(write_only=True)
    # exp = Expedition.objects.filter(Status='in', ID_Creator=user_id).last()
    class Meta:
        # Модель, которую мы сериализуем
        model = Object
        fields = '__all__'
# class ObjSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Object
#         fields = ('ID_Object', 'Name_Obj', 'Region', 'Year', 'Opener', 'Status', 'Image_Url')

#     def to_representation(self, instance):
#         user_id = self.context.get('user_id')

#         # Получаем объекты пользователя с нужным статусом экспедиции
#         exp = Expedition.objects.filter(Status='in', ID_Creator=user_id).last()

#         # Если экспедиция найдена, возвращаем ID объекта и ID экспедиции
#         if exp:
#             return {
#                 'expedition_id': exp.ID_Expedition,
#                 'objects': {
#                     'ID_Object': instance.ID_Object,
#                     'Name_Obj': instance.Name_Obj,
#                     'Region': instance.Region,
#                     'Year': instance.Year,
#                     'Opener': instance.Opener,
#                     'Status': instance.Status,
#                     'Image_Url': instance.Image_Url.url if instance.Image_Url else None
#                 }
#             }

#         # Если экспедиция не найдена, возвращаем только ID объекта
#         return {
#             'expedition_id': 0,
#             'objects': {
#                 'ID_Object': instance.ID_Object
#             }
#         }

class UsertestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username']
class ExpSerializer(serializers.ModelSerializer):
    Moderator = UsertestSerializer(read_only=True)
    ID_Creator = UsertestSerializer(read_only=True)
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
 
