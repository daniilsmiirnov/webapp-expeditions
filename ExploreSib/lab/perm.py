from functools import wraps
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied
import jwt, datetime
from .models import Users

def isAuth(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Аутентификация не пройдена!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Аутентификация не пройдена!')

        # Проверка успешной аутентификации
        user = Users.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed('Аутентификация не пройдена!')

        return view_func(request, *args, **kwargs)
    return wrap
def isModerator(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')

        if not token:
            raise PermissionDenied('Доступ запрещен: Токен отсутствует.')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise PermissionDenied('Доступ запрещен: Истек срок действия токена.')
        except jwt.InvalidTokenError:
            raise PermissionDenied('Доступ запрещен: Недействительный токен.')

        user_id = payload.get('id')
        if not user_id:
            raise PermissionDenied('Доступ запрещен: Неверные данные в токене.')

        user = Users.objects.filter(id=user_id, Is_Super=True).first()
        if not user:
            raise PermissionDenied('Доступ запрещен: Недостаточно прав для выполнения операции.')

        return view_func(request, *args, **kwargs)
    return wrap
