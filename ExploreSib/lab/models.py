from django.db import models
from viewflow.fields import CompositeKey
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import User
# Create your models here.

# class Users(models.Model):
#     ID_User = models.IntegerField(primary_key=True)
#     Is_Super = models.BooleanField(default=False)
#     Username = models.CharField(max_length=50, help_text='Input username')
#     Login = models.CharField(max_length=50, help_text='Input login')
#     Password = models.CharField(max_length=50, help_text='Input password')
#     def __str__(self):
#         return self.Username
class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Is_Super = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
class Object(models.Model):
    ID_Object = models.IntegerField(primary_key=True)
    Name_Obj = models.CharField(max_length=100,help_text='Input name obj')
    Region = models.CharField(max_length=100,help_text='Input name region')
    Year = models.IntegerField(default=1800,help_text='Input year opening')
    Opener = models.CharField(max_length=100,help_text='Input name opener')
    
    status = [
        ('del','Удален'),
        ('ope','Действует'),
    ]
    Status = models.CharField(max_length=3, choices=status, default='ope', help_text='Status Obj')
    Image_Url = models.ImageField(upload_to='img/',blank=True, editable=True)
    def __str__(self):
        return self.Name_Obj     
class Expedition(models.Model):
    ID_Expedition = models.AutoField(primary_key=True)
    Name_Exp  = models.CharField(max_length=150, help_text='Input name expedition',default='Название экспедиции')
    DateStart = models.DateTimeField(default=datetime.now,help_text='Дата начала экспедиции')
    DateEnd = models.DateTimeField(default=datetime.now, help_text='Дата конца экспедиции',null=True,blank=True)
    DateApproving = models.DateTimeField(default=datetime.now,help_text='Дата утверждения экспедиции',null=True,blank=True)
    status = [
        ('in','Введён'),
        ('wo','В работе'),
        ('en','Завершён'),
        ('ca','Отменён'),
        ('de','Удалён'),
    ]
    Status = models.CharField(max_length=2, choices=status, default='in', help_text='Status Expedition')
    Leader = models.CharField(max_length=100,help_text='Input name leader',default='ФИО Лидера')
    Moderator = models.ForeignKey(Users,related_name='Moderator', on_delete=models.CASCADE,default=1)
    ID_Creator = models.ForeignKey(Users,related_name='ID_Author', on_delete=models.CASCADE, default=1)
    Describe = models.CharField(max_length=400, null=True,default='...')
    Objects = models.ManyToManyField(Object,through='Programm')
    def __str__(self):
        return self.Name_Exp
    



class Programm(models.Model):
    ID_OE = CompositeKey(columns=['ID_Exp', 'ID_Obj'])
    ID_Exp = models.ForeignKey(Expedition, on_delete=models.CASCADE, db_column='ID_Exp')
    ID_Obj = models.ForeignKey(Object, on_delete=models.CASCADE, db_column='ID_Obj')
    Number = models.IntegerField(null=True, help_text='Порядковый номер',default=1)
    def __str__(self):  
        return (self.ID_Obj.Name_Obj+" - "+self.ID_Exp.Name_Exp)
    class Meta:
        manage: False


class Programm1(models.Model):
    ID_Exp = models.ForeignKey(Expedition, on_delete=models.CASCADE, db_column='ID_Exp')
    ID_Obj = models.ForeignKey(Object, on_delete=models.CASCADE, db_column='ID_Obj')
    Number = models.IntegerField(null=True, help_text='Порядковый номер')
    def __str__(self):  
        return (self.ID_Obj.Name_Obj+" - "+self.ID_Exp.Name_Exp)
    class Meta:
        manage: False